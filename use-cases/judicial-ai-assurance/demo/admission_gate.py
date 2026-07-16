#!/usr/bin/env python3
"""Build a deterministic, non-scoring judicial-AI evidence demo."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PROFILE = ROOT / "use-cases/judicial-ai-assurance/jrem/exports/judicial-ai-assurance-2026.1.json"
DEFAULT_SCENARIOS = Path(__file__).with_name("scenarios.json")
DEFAULT_OUTPUT = ROOT / "playground/judicial-ai-demo.json"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(payload.encode()).hexdigest()


def normalise_evidence(groups: list[dict]) -> list[dict]:
    records = []
    for index, group in enumerate(groups, 1):
        record = {**group, "id": group.get("id", f"E-{index:03d}")}
        record["recordHash"] = canonical_hash({
            key: value for key, value in record.items() if key != "recordHash"
        })
        records.append(record)
    return records


def evaluate_control(rule: dict, evidence: list[dict]) -> dict:
    assurance = rule["outcome"]["assurance"]
    required = assurance["evidenceRequired"]
    by_type: dict[str, list[dict]] = {item: [] for item in required}
    for record in evidence:
        for artifact_type in record["artifactTypes"]:
            if artifact_type in by_type:
                by_type[artifact_type].append(record)

    missing = [item for item, records in by_type.items() if not records]
    failed = [
        item for item, records in by_type.items()
        if any(record["status"] == "failed" for record in records)
    ]
    evidence_refs = sorted({
        record["id"] for records in by_type.values() for record in records
    })

    hard_stop = assurance["controlClass"] == "hard-stop"
    if hard_stop and (missing or failed):
        status = "blocked"
    else:
        status = "review-required"

    return {
        "controlId": rule["ruleId"],
        "name": rule["name"],
        "controlClass": assurance["controlClass"],
        "status": status,
        "missingEvidence": missing,
        "failedEvidence": failed,
        "evidenceRefs": evidence_refs,
    }


def evaluate_scenario(profile: dict, common: list[dict], scenario: dict) -> dict:
    evidence = normalise_evidence(common + scenario.get("evidence", []))
    controls = [evaluate_control(rule, evidence) for rule in profile["rules"]]
    blocked = [item["controlId"] for item in controls if item["status"] == "blocked"]
    incomplete = [
        item["controlId"] for item in controls
        if item["missingEvidence"] or item["failedEvidence"]
    ]
    decision = scenario.get("humanDecision")
    valid_approval = bool(
        decision
        and decision.get("decision") == "approved"
        and decision.get("profileVersion") == profile["version"]
        and all(decision.get(field) for field in ("actor", "role", "reason"))
    )

    if blocked or (decision and decision.get("decision") == "rejected"):
        status = "blocked"
    elif valid_approval and not incomplete:
        status = "conditionally-admissible"
    else:
        status = "review-required"

    return {
        "scenarioId": scenario["scenarioId"],
        "title": scenario["title"],
        "summary": scenario["summary"],
        "expectedBoundary": scenario["expectedBoundary"],
        "status": status,
        "blockedControls": blocked,
        "humanDecision": decision,
        "controls": controls,
        "evidence": evidence,
    }


def build_demo(profile_path: Path, scenarios_path: Path) -> dict:
    profile = read_json(profile_path)
    scenarios = read_json(scenarios_path)
    result = {
        "schemaVersion": "1.0.0",
        "profile": {
            "domain": profile["domain"],
            "version": profile["version"],
            "status": profile["maturityLevel"],
            "ruleCount": len(profile["rules"]),
            "hardStopCount": sum(
                rule["outcome"]["assurance"]["controlClass"] == "hard-stop"
                for rule in profile["rules"]
            ),
            "sourceHash": canonical_hash(profile),
        },
        "disclaimer": profile["metadata"]["indicatorDisclaimer"],
        "scenarios": [
            evaluate_scenario(profile, scenarios["commonEvidence"], scenario)
            for scenario in scenarios["scenarios"]
        ],
    }
    result["bundleHash"] = canonical_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--scenarios", type=Path, default=DEFAULT_SCENARIOS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = build_demo(args.profile, args.scenarios)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {args.output} ({result['bundleHash']})")


if __name__ == "__main__":
    main()
