#!/usr/bin/env python3
"""Fail closed on unsupported conditions and executable scenario mismatches."""

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared"))

from registry import can_calculate
from rule_engine import RuleEvaluationError, rule_matches, select_rule


def normalized_facts(data: dict) -> dict:
    facts = dict(data)
    if facts.get("onvermogend"):
        facts["partijType"] = "onvermogend"
    return facts


def validate() -> list[str]:
    errors = []
    for path in sorted(ROOT.glob("use-cases/*/jrem/exports/*.json")):
        data = json.loads(path.read_text())
        domain = path.parents[2].name
        rules = data.get("rules", [])

        for rule in rules:
            try:
                rule_matches(rule, {})
            except RuleEvaluationError as exc:
                errors.append(f"{path}: {rule.get('ruleId')}: {exc}")

        if not can_calculate(domain):
            continue
        if not any(rule.get("conditions") for rule in rules):
            errors.append(f"{path}: executable domain has no executable conditions")

        for scenario in data.get("scenarios", []):
            expected = scenario.get("expected", {})
            expected_rules = expected.get("appliedRules", [])
            if not expected_rules:
                continue
            facts = normalized_facts(scenario.get("input", {}))
            selected = select_rule(rules, facts)
            if selected is None:
                errors.append(f"{path}: {scenario['id']}: no rule matched")
                continue
            if selected["ruleId"] != expected_rules[0]:
                errors.append(
                    f"{path}: {scenario['id']}: expected {expected_rules[0]}, got {selected['ruleId']}"
                )
            same_priority = [
                rule["ruleId"] for rule in rules
                if rule_matches(rule, facts) and rule.get("priority", 0) == selected.get("priority", 0)
            ]
            if len(same_priority) > 1:
                errors.append(f"{path}: {scenario['id']}: ambiguous same-priority rules {same_priority}")

            outcome = selected.get("outcome", {})
            if "category" in expected and outcome.get("category") != expected["category"]:
                errors.append(f"{path}: {scenario['id']}: outcome category mismatch")
            if "griffierecht" in expected:
                amount = outcome.get("griffierecht", {}).get("amount")
                if amount != expected["griffierecht"]:
                    errors.append(f"{path}: {scenario['id']}: expected amount {expected['griffierecht']}, got {amount}")
    return errors


if __name__ == "__main__":
    failures = validate()
    for failure in failures:
        print(f"ERROR: {failure}")
    print(f"Rule semantics: {len(failures)} error(s)")
    raise SystemExit(bool(failures))
