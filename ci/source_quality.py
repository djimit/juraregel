#!/usr/bin/env python3
"""Measure source debt and block L2/L3 rules without reproducible anchors."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGISLATIVE_TYPES = {"wet", "wetsartikel", "besluit"}


def issues_for_rule(rule: dict, ruleset: dict) -> list[str]:
    issues = []
    rule_id = rule.get("ruleId", "?")
    for index, ref in enumerate(rule.get("sourceRefs", [])):
        prefix = f"{rule_id}.sourceRefs[{index}]"
        if not ref.get("url"):
            issues.append(f"{prefix}: missing url")
        if not (ref.get("bronVersie") or ref.get("bronDatum")):
            issues.append(f"{prefix}: missing source version/date")
        if ref.get("section") in (None, "", rule_id):
            issues.append(f"{prefix}: section is not an exact legal anchor")
        if ref.get("type") in LEGISLATIVE_TYPES and not (
            ref.get("bwbId") or ruleset.get("bwbId") or ruleset.get("celexId") or ruleset.get("eli")
        ):
            issues.append(f"{prefix}: missing BWB/CELEX/ELI identifier")
    return issues


def audit(root: Path = ROOT) -> dict:
    debt = []
    blocking = []
    for path in sorted(root.glob("use-cases/*/jrem/exports/*.json")):
        ruleset = json.loads(path.read_text())
        maturity = ruleset.get("maturityLevel", "L0-demo")
        for rule in ruleset.get("rules", []):
            for issue in issues_for_rule(rule, ruleset):
                item = f"{path.relative_to(root)}: {issue}"
                debt.append(item)
                if maturity.startswith(("L2-", "L3-")):
                    blocking.append(item)
    return {"debt": debt, "blocking": blocking}


if __name__ == "__main__":
    result = audit()
    for issue in result["blocking"][:50]:
        print(f"ERROR: {issue}")
    print(f"Source quality: {len(result['debt'])} debt item(s), {len(result['blocking'])} blocking")
    raise SystemExit(bool(result["blocking"]))
