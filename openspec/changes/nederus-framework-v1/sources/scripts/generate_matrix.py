#!/usr/bin/env python3
"""
NEDERUS Mapping Matrix Generator v2.0

Reads controls.yaml and generates mapping-matrix.csv.
The CSV is NEVER hand-edited — always regenerated from YAML.

Usage:
  python scripts/generate_matrix.py          # Regenerate mapping-matrix.csv
  python scripts/generate_matrix.py --check  # Verify CSV is in sync (CI)
  python scripts/generate_matrix.py --stdout # Output to stdout (no file write)
"""

import csv
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
CONTROLS_PATH = REPO_ROOT / "controls.yaml"
MATRIX_PATH = REPO_ROOT / "mapping-matrix.csv"

CSV_COLUMNS = [
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


def load_controls() -> dict:
    with open(CONTROLS_PATH, "r") as f:
        return yaml.safe_load(f)


def extract_ref(fw_data: dict) -> str:
    if not fw_data or fw_data.get("relation") == "gap":
        return "N/A"
    return fw_data.get("reference", "N/A")


def extract_function(fw_data: dict) -> str:
    if not fw_data:
        return "N/A"
    return fw_data.get("function", "N/A")


def determine_tier(ctrl: dict) -> str:
    """Determine tier based on framework count."""
    frameworks = ctrl.get("frameworks", {})
    mapped = sum(
        1 for fw in ALL_FRAMEWORKS if frameworks.get(fw, {}).get("relation") != "gap"
    )
    if mapped >= 3:
        return "priority"
    return "standard"


def determine_coverage(ctrl: dict) -> str:
    """Determine coverage level based on number of frameworks mapped."""
    frameworks = ctrl.get("frameworks", {})
    mapped = sum(
        1 for fw in ALL_FRAMEWORKS if frameworks.get(fw, {}).get("relation") != "gap"
    )
    if mapped >= 6:
        return "full"
    elif mapped >= 3:
        return "partial"
    return "minimal"


def generate_rows(data: dict) -> list[dict]:
    rows = []
    for ctrl in data.get("controls", []):
        frameworks = ctrl.get("frameworks", {})
        nist = frameworks.get("nist_ai_rmf", {})

        rows.append(
            {
                "control_id": ctrl["id"],
                "control_title": ctrl["title"],
                "tier": determine_tier(ctrl),
                "nist_function": extract_function(nist),
                "nist_ref": extract_ref(nist),
                "eu_article": extract_ref(frameworks.get("eu_ai_act", {})),
                "bio2_ref": extract_ref(frameworks.get("bio2", {})),
                "nis2_article": extract_ref(frameworks.get("nis2", {})),
                "nora_ref": extract_ref(frameworks.get("nora", {})),
                "cra_ref": extract_ref(frameworks.get("cra", {})),
                "dsa_ref": extract_ref(frameworks.get("dsa", {})),
                "ai_liability_ref": extract_ref(frameworks.get("ai_liability", {})),
                "coverage": determine_coverage(ctrl),
                "approved_by": "DjimIT (self-reviewed)",
            }
        )
    return rows


def write_csv(rows: list[dict], output_path: Path):
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def write_stdout(rows: list[dict]):
    writer = csv.DictWriter(sys.stdout, fieldnames=CSV_COLUMNS)
    writer.writeheader()
    writer.writerows(rows)


def main():
    args = sys.argv[1:]
    data = load_controls()
    rows = generate_rows(data)

    if "--stdout" in args:
        write_stdout(rows)
        return

    if "--check" in args:
        import io

        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
        generated = buf.getvalue()

        with open(MATRIX_PATH, "r") as f:
            existing = f.read()

        if generated != existing:
            sys.exit(1)
        return

    write_csv(rows, MATRIX_PATH)
    print(f"Generated {MATRIX_PATH} with {len(rows)} rows")


if __name__ == "__main__":
    main()
