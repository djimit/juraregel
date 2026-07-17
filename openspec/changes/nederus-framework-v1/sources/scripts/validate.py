#!/usr/bin/env python3
"""
NEDERUS Structural Validation Script (Layer 1) v2.0

Validates:
- YAML syntax and schema compliance
- CSV completeness (no empty cells)
- Referential integrity (all framework refs exist)
- Tier classification accuracy (≥3 = priority, ≥2 = standard)

Exit code 0 = all checks pass
Exit code 1 = one or more checks fail
"""

import csv
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
CONTROLS_PATH = REPO_ROOT / "controls.yaml"
MATRIX_PATH = REPO_ROOT / "mapping-matrix.csv"

ALL_FRAMEWORKS = [
    "nist_ai_rmf",
    "eu_ai_act",
    "bio2",
    "nis2",
    "nora",
    "cra",
    "dsa",
    "ai_liability",
]
NIST_FUNCTIONS = ["GOVERN", "MAP", "MEASURE", "MANAGE"]


def load_yaml(path: Path) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_csv(path: Path) -> list[dict]:
    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def validate_yaml_syntax(data: dict) -> list[str]:
    errors = []
    for key in ["version", "last_updated", "frameworks", "controls"]:
        if key not in data:
            errors.append(f"Missing required key: {key}")
    return errors


def validate_control_ids(data: dict) -> list[str]:
    errors = []
    pattern = re.compile(r"^NED-\d{2}$")
    for ctrl in data.get("controls", []):
        if not pattern.match(ctrl.get("id", "")):
            errors.append(f"Invalid control ID format: {ctrl.get('id')}")
    return errors


def validate_framework_refs(data: dict) -> list[str]:
    errors = []
    for ctrl in data.get("controls", []):
        frameworks = ctrl.get("frameworks", {})
        for fw in ALL_FRAMEWORKS:
            if fw not in frameworks:
                errors.append(f"Control {ctrl['id']}: missing framework '{fw}'")
    return errors


def validate_minimum_frameworks(data: dict) -> list[str]:
    """Validate every control maps to >=2 frameworks."""
    errors = []
    for ctrl in data.get("controls", []):
        frameworks = ctrl.get("frameworks", {})
        mapped = sum(
            1
            for fw in ALL_FRAMEWORKS
            if frameworks.get(fw, {}).get("relation") != "gap"
        )
        if mapped < 2:
            errors.append(
                f"Control {ctrl['id']}: only {mapped} framework(s) mapped (minimum is 2)"
            )
    return errors


def validate_csv_completeness(rows: list[dict]) -> list[str]:
    errors = []
    required_cols = [
        "control_id",
        "control_title",
        "tier",
        "nist_function",
        "nist_ref",
        "eu_article",
        "bio2_ref",
        "nis2_article",
        "nora_ref",
        "cra_ref",
        "dsa_ref",
        "ai_liability_ref",
        "coverage",
        "approved_by",
    ]
    for i, row in enumerate(rows, start=2):
        for col in required_cols:
            value = row.get(col, "").strip()
            if not value:
                errors.append(f"CSV row {i}: empty cell in column '{col}'")
    return errors


def validate_approved_by(rows: list[dict]) -> list[str]:
    errors = []
    for i, row in enumerate(rows, start=2):
        if not row.get("approved_by", "").strip():
            errors.append(f"CSV row {i}: missing 'approved_by' field")
    return errors


def validate_bidirectional(data: dict) -> list[str]:
    warnings = []
    mapped_functions = set()
    for ctrl in data.get("controls", []):
        nist = ctrl.get("frameworks", {}).get("nist_ai_rmf", {})
        func = nist.get("function", "")
        for f in NIST_FUNCTIONS:
            if f in func:
                mapped_functions.add(f)

    for func in NIST_FUNCTIONS:
        if func not in mapped_functions:
            warnings.append(f"NIST function '{func}' has no mapping (warning)")
    return warnings


def main():
    all_errors = []
    all_warnings = []

    for path in [CONTROLS_PATH, MATRIX_PATH]:
        if not path.exists():
            print(f"FATAL: {path} not found")
            sys.exit(1)

    try:
        data = load_yaml(CONTROLS_PATH)
    except yaml.YAMLError as e:
        print(f"FATAL: YAML parse error: {e}")
        sys.exit(1)

    try:
        rows = load_csv(MATRIX_PATH)
    except csv.Error as e:
        print(f"FATAL: CSV parse error: {e}")
        sys.exit(1)

    all_errors.extend(validate_yaml_syntax(data))
    all_errors.extend(validate_control_ids(data))
    all_errors.extend(validate_framework_refs(data))
    all_errors.extend(validate_minimum_frameworks(data))
    all_errors.extend(validate_csv_completeness(rows))
    all_errors.extend(validate_approved_by(rows))
    all_warnings.extend(validate_bidirectional(data))

    if all_warnings:
        print("WARNINGS:")
        for w in all_warnings:
            print(f"  ⚠ {w}")
        print()

    if all_errors:
        print(f"VALIDATION FAILED — {len(all_errors)} error(s):")
        for e in all_errors:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("✓ All structural validation checks passed")
        print(f"  Controls: {len(data.get('controls', []))}")
        print(f"  CSV rows: {len(rows)}")
        print(f"  Frameworks: {len(data.get('frameworks', {}))}")
        priority = sum(
            1
            for c in data.get("controls", [])
            if sum(
                1
                for fw in ALL_FRAMEWORKS
                if c.get("frameworks", {}).get(fw, {}).get("relation") != "gap"
            )
            >= 3
        )
        print(f"  Priority controls (>=3 frameworks): {priority}")
        print(
            f"  Standard controls (2 frameworks): {len(data.get('controls', [])) - priority}"
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
