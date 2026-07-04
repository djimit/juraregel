#!/usr/bin/env python3
"""
JREM Validator — valideert een JREM-instance tegen het JSON Schema.

Usage:
    python3 validate.py --schema schema.json --instance exports/griffierecht-civiel-2026.1.json
    python3 validate.py --schema schema.json --instance exports/griffierecht-civiel-2026.1.json --strict
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema import Draft202012Validator
except ImportError:
    print("ERROR: jsonschema not installed. Run: pip3 install jsonschema", file=sys.stderr)
    sys.exit(2)


def validate_instance(schema_path: str, instance_path: str, strict: bool = False) -> int:
    """Validate a JREM instance against the schema. Returns exit code."""
    # Load schema
    try:
        with open(schema_path) as f:
            schema = json.load(f)
    except json.JSONDecodeError as e:
        print(f"SCHEMA ERROR: Invalid JSON in schema: {e}", file=sys.stderr)
        return 2
    except FileNotFoundError:
        print(f"SCHEMA ERROR: Schema file not found: {schema_path}", file=sys.stderr)
        return 2

    # Validate schema itself
    try:
        Draft202012Validator.check_schema(schema)
    except jsonschema.SchemaError as e:
        print(f"SCHEMA ERROR: Schema is not valid JSON Schema 2020-12: {e}", file=sys.stderr)
        return 2

    # Load instance
    try:
        with open(instance_path) as f:
            instance = json.load(f)
    except json.JSONDecodeError as e:
        print(f"INSTANCE ERROR: Invalid JSON in instance: {e}", file=sys.stderr)
        return 1
    except FileNotFoundError:
        print(f"INSTANCE ERROR: Instance file not found: {instance_path}", file=sys.stderr)
        return 1

    # Validate instance against schema
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))

    if not errors:
        # Additional checks in strict mode
        if strict:
            extra_errors = check_additional_quality(instance)
            if extra_errors:
                print(f"STRICT VALIDATION FAILED: {len(extra_errors)} quality issue(s)")
                for err in extra_errors:
                    print(f"  - {err}")
                return 1

        rule_count = len(instance.get("rules", []))
        scenario_count = len(instance.get("scenarios", []))
        transition_count = len(instance.get("transitionRules", []))
        print(f"VALID: {instance_path}")
        print(f"  Rules: {rule_count}")
        print(f"  Scenarios: {scenario_count}")
        print(f"  Transition rules: {transition_count}")
        print(f"  Schema: {schema_path}")

        # Check brontraceability
        missing_sources = []
        for rule in instance.get("rules", []):
            if not rule.get("sourceRefs"):
                missing_sources.append(rule.get("ruleId", "unknown"))
        if missing_sources:
            print(f"  WARNING: {len(missing_sources)} rule(s) without sourceRefs: {missing_sources}")
        else:
            print(f"  Brontraceability: OK ({rule_count} rules all have sourceRefs)")

        return 0
    else:
        print(f"VALIDATION FAILED: {len(errors)} error(s)")
        for error in errors:
            path = " -> ".join(str(p) for p in error.path) or "(root)"
            rule_id = ""
            # Try to find ruleId for context
            if error.path and len(error.path) > 1:
                path_parts = list(error.path)
                if "rules" in path_parts:
                    rule_idx = path_parts.index("rules") + 1
                    if rule_idx < len(path_parts) and isinstance(path_parts[rule_idx], int):
                        rule_idx_val = path_parts[rule_idx]
                        if rule_idx_val < len(instance.get("rules", [])):
                            rule_id = instance["rules"][rule_idx_val].get("ruleId", f"index-{rule_idx_val}")
            
            prefix = f"  [{rule_id}] " if rule_id else "  "
            print(f"{prefix}{path}: {error.message}")
        return 1


def check_additional_quality(instance: dict) -> list:
    """Additional quality checks beyond schema validation."""
    issues = []
    
    # Check each rule has valid conditions
    for rule in instance.get("rules", []):
        conditions = rule.get("conditions", {})
        if not conditions:
            issues.append(f"Rule {rule.get('ruleId')}: has no conditions")
        
        # Check outcome has amount
        outcome = rule.get("outcome", {})
        griffierecht = outcome.get("griffierecht", {})
        if griffierecht.get("amount") is None and not outcome.get("manualReviewRequired"):
            issues.append(f"Rule {rule.get('ruleId')}: amount is null but manualReviewRequired is false")
    
    # Check scenarios match rules
    for scenario in instance.get("scenarios", []):
        expected_rules = scenario.get("expected", {}).get("appliedRules", [])
        rule_ids = {r["ruleId"] for r in instance.get("rules", [])}
        for ar in expected_rules:
            if ar not in rule_ids:
                issues.append(f"Scenario {scenario.get('id')}: references unknown rule {ar}")
    
    return issues


def main():
    parser = argparse.ArgumentParser(description="JREM Validator")
    parser.add_argument("--schema", required=True, help="Path to JREM JSON Schema")
    parser.add_argument("--instance", required=True, help="Path to JREM instance to validate")
    parser.add_argument("--strict", action="store_true", help="Additional quality checks")
    args = parser.parse_args()
    
    exit_code = validate_instance(args.schema, args.instance, args.strict)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
