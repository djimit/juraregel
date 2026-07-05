#!/usr/bin/env python3
"""
JREM Schema Migration Tool v2.0.

Migreert JREM exports tussen schema versies.
Ondersteunt: v1.0.0 -> v1.1.0 (core + interpretatie metadata)

Usage:
  python3 tools/jrem-migrate.py [--check-only] [--add-interpretation]
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

MIGRATIONS = {
    "1.0.0": {"1.1.0": "migrate_v1_0_to_v1_1"},
    "unknown": {"1.1.0": "migrate_v1_0_to_v1_1"},
}


def migrate_v1_0_to_v1_1(data: dict, add_interpretation: bool = False) -> dict:
    """Migrate JREM v1.0.0/unknown to v1.1.0."""
    data["schemaVersion"] = "1.1.0"

    # Add interpretation metadata if requested
    if add_interpretation:
        for rule in data.get("rules", []):
            if "interpretatieMethode" not in rule:
                rule["interpretatieMethode"] = "handmatig"
            if "interpretatieOpmerking" not in rule:
                rule["interpretatieOpmerking"] = "Geen opmerking"

    # Add source version info if missing
    for rule in data.get("rules", []):
        for ref in rule.get("sourceRefs", []):
            if "bronVersie" not in ref:
                ref["bronVersie"] = data.get("validFrom", "unknown")
            if "bronDatum" not in ref:
                ref["bronDatum"] = data.get("validFrom", "unknown")

    return data


def validate_migration(data: dict) -> list[str]:
    """Validate migrated JREM export. Returns list of issues."""
    issues = []

    if data.get("schemaVersion") != "1.1.0":
        issues.append(f"schemaVersion should be 1.1.0, got {data.get(schemaVersion)}")

    for rule in data.get("rules", []):
        # Check sourceRefs have required fields
        for ref in rule.get("sourceRefs", []):
            if ref.get("type") == "wet" and not ref.get("bwbId"):
                issues.append(f"Rule {rule[ruleId]}: wet-type sourceRef missing bwbId")
            if not ref.get("bronVersie"):
                issues.append(f"Rule {rule[ruleId]}: sourceRef missing bronVersie")

    return issues


def migrate_file(filepath: Path, dry_run: bool = False, add_interpretation: bool = False) -> dict:
    """Migrate a single JREM export file."""
    data = json.loads(filepath.read_text())
    version = data.get("schemaVersion", "unknown")

    if version in ("1.0.0", "unknown"):
        if dry_run:
            return {"file": str(filepath), "from": version, "to": "1.1.0", "dry_run": True}

        migrated = migrate_v1_0_to_v1_1(data, add_interpretation)
        issues = validate_migration(migrated)

        if issues and not add_interpretation:
            print(f"  WARN {filepath.name}: {len(issues)} issues")
            for issue in issues[:3]:
                print(f"    - {issue}")

        filepath.write_text(json.dumps(migrated, indent=2, ensure_ascii=False))
        return {"file": str(filepath), "from": version, "to": "1.1.0", "migrated": True, "issues": len(issues)}

    return {"file": str(filepath), "version": version, "migrated": False}


if __name__ == "__main__":
    check_only = "--check-only" in sys.argv
    add_interpretation = "--add-interpretation" in sys.argv
    jrem_files = list((REPO_ROOT / "use-cases").glob("*/jrem/exports/*.json"))

    results = []
    for f in sorted(jrem_files):
        result = migrate_file(f, dry_run=check_only, add_interpretation=add_interpretation)
        results.append(result)

    need_migration = sum(1 for r in results if r.get("from") in ("1.0.0", "unknown"))
    already_latest = sum(1 for r in results if r.get("version") == "1.1.0")
    total_issues = sum(r.get("issues", 0) for r in results)

    print(f"Checked {len(results)} JREM exports")
    print(f"  Already v1.1.0: {already_latest}")
    print(f"  Need migration: {need_migration}")
    print(f"  Total issues: {total_issues}")

    if not check_only:
        migrated = sum(1 for r in results if r.get("migrated"))
        print(f"  Migrated: {migrated}")

    # Exit with error code if issues found
    sys.exit(1 if total_issues > 0 and not check_only else 0)
