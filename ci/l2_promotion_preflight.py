#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from acceptance_metadata import validate_acceptance


TARGETS = [
    {
        "ruleSetId": "decentrale-regelcheck",
        "jrem": "use-cases/decentrale-regelcheck/jrem/exports/decentrale-regelcheck-2026.1.json",
        "template": "docs/acceptance-templates/decentrale-regelcheck-l2.acceptance.json",
    },
    {
        "ruleSetId": "woo-publicatieplicht-preflight",
        "jrem": "use-cases/woo-publicatieplicht-preflight/jrem/exports/woo-publicatieplicht-preflight-2026.1.json",
        "template": "docs/acceptance-templates/woo-publicatieplicht-preflight-l2.acceptance.json",
    },
    {
        "ruleSetId": "sttr-preflight",
        "jrem": "use-cases/sttr-preflight/jrem/exports/sttr-preflight-2026.1.json",
        "template": "docs/acceptance-templates/sttr-preflight-l2.acceptance.json",
    },
]

REQUIRED_TEMPLATE_FIELDS = (
    "ruleSetId",
    "version",
    "maturityTarget",
    "reviewer.geaccondeerdDoor",
    "reviewer.rol",
    "reviewer.organisatie",
    "review.datum",
    "review.geldigTot",
    "review.scope",
    "review.bronSnapshot",
    "review.verklaring",
    "review.beperkingen",
    "sourceSnapshotRefs",
    "scenarioAcceptance",
)


def load_json(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def get_path(data: dict, dotted: str):
    value = data
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def has_placeholder(value) -> bool:
    if isinstance(value, str):
        return "__" in value
    if isinstance(value, list):
        return any(has_placeholder(item) for item in value)
    if isinstance(value, dict):
        return any(has_placeholder(item) for item in value.values())
    return False


def missing_template_fields(template: dict) -> list[str]:
    missing = []
    for field in REQUIRED_TEMPLATE_FIELDS:
        value = get_path(template, field)
        if value in (None, "", []):
            missing.append(field)
    return missing


def source_snapshot_reasons(template: dict) -> list[str]:
    refs = template.get("sourceSnapshotRefs")
    if not isinstance(refs, list) or not refs:
        return ["sourceSnapshotRefs ontbreekt"]

    reasons = []
    for index, ref in enumerate(refs):
        if not isinstance(ref, dict):
            reasons.append(f"sourceSnapshotRefs[{index}] is ongeldig")
            continue
        for field in ("name", "url", "checkedAt"):
            if not ref.get(field):
                reasons.append(f"sourceSnapshotRefs[{index}].{field} ontbreekt")
    return reasons


def scenario_reasons(template: dict) -> list[str]:
    scenarios = template.get("scenarioAcceptance")
    if not isinstance(scenarios, list) or not scenarios:
        return ["scenarioAcceptance ontbreekt"]

    reasons = []
    for index, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict):
            reasons.append(f"scenarioAcceptance[{index}] is ongeldig")
            continue
        if not scenario.get("scenario"):
            reasons.append(f"scenarioAcceptance[{index}].scenario ontbreekt")
        if scenario.get("accepted") is not True:
            reasons.append(f"scenarioAcceptance[{index}].accepted is niet true")
    return reasons


def template_accordering(template: dict) -> dict:
    reviewer = template.get("reviewer") or {}
    review = template.get("review") or {}
    return {
        "geaccondeerdDoor": reviewer.get("geaccondeerdDoor"),
        "rol": reviewer.get("rol"),
        "organisatie": reviewer.get("organisatie"),
        "datum": review.get("datum"),
        "geldigTot": review.get("geldigTot"),
        "versie": template.get("version"),
        "scope": review.get("scope"),
        "bronSnapshot": review.get("bronSnapshot"),
        "verklaring": review.get("verklaring"),
        "beperkingen": review.get("beperkingen"),
    }


def template_acceptance_status(template: dict, jrem: dict) -> tuple[str, str]:
    data = {
        "version": jrem.get("version", ""),
        "maturityLevel": "L2-pilot",
        "metadata": {
            "acceptatieType": "full",
            "juristAccordering": template_accordering(template),
        },
    }
    return validate_acceptance(data, require_extended=True)


def evaluate_target(root: Path, target: dict) -> dict:
    reasons = []
    blocking = False
    jrem_path = root / target["jrem"]
    template_path = root / target["template"]

    if not jrem_path.exists():
        return {
            "ruleSetId": target["ruleSetId"],
            "ready": False,
            "blocking": True,
            "reasons": [f"JREM export ontbreekt: {target['jrem']}"],
        }
    if not template_path.exists():
        return {
            "ruleSetId": target["ruleSetId"],
            "ready": False,
            "blocking": True,
            "reasons": [f"L2 acceptance template ontbreekt: {target['template']}"],
        }

    jrem = load_json(jrem_path)
    template = load_json(template_path)

    missing = missing_template_fields(template)
    if missing:
        reasons.extend(f"{field} ontbreekt" for field in missing)

    if template.get("ruleSetId") != jrem.get("ruleSetId"):
        reasons.append("template ruleSetId komt niet overeen met JREM")

    if template.get("maturityTarget") != "L2-pilot":
        reasons.append("maturityTarget moet L2-pilot zijn")

    if has_placeholder(template):
        reasons.append("template bevat placeholders")

    reasons.extend(source_snapshot_reasons(template))
    reasons.extend(scenario_reasons(template))

    status, message = template_acceptance_status(template, jrem)
    if status != "PASS":
        reasons.append(message)

    maturity = jrem.get("maturityLevel", "")
    if maturity.startswith(("L2-", "L3-")):
        if (jrem.get("approval") or {}).get("type") == "self":
            reasons.append(f"JREM is self-approved at {maturity}")
            blocking = True
        jrem_status, jrem_message = validate_acceptance(jrem, require_extended=True)
        if jrem_status != "PASS":
            reasons.append(jrem_message)
            blocking = True

    return {
        "ruleSetId": target["ruleSetId"],
        "ready": not reasons,
        "blocking": blocking,
        "templateStatus": "missing-fields" if missing else "template-ready",
        "jremMaturity": maturity,
        "reasons": reasons,
    }


def main() -> int:
    root = Path.cwd()
    results = [evaluate_target(root, target) for target in TARGETS]
    output = {
        "summary": {
            "targets": len(results),
            "ready": sum(1 for result in results if result["ready"]),
            "blocking": sum(1 for result in results if result["blocking"]),
        },
        "results": results,
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 1 if output["summary"]["blocking"] else 0


if __name__ == "__main__":
    sys.exit(main())
