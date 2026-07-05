#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

def migrate_v1_0_to_v1_1(data: dict) -> dict:
    data["schemaVersion"] = "1.1.0"
    domain = data.get("domain", "")
    eu_domains = ["eu-ai-act", "avg-gdpr", "nis2"]
    gemeente_domains = ["participatiewet", "wmo"]
    if domain in eu_domains:
        data["governanceLevel"] = "eu"
    elif domain in gemeente_domains:
        data["governanceLevel"] = "gemeente"
    else:
        data["governanceLevel"] = "rijk"
    for ref in data.get("rules", []):
        for source in ref.get("sourceRefs", []):
            title = source.get("title", "")
            if "Toeslagenwet" in title:
                source.setdefault("bwbId", "BWBR0005291")
            elif "Participatiewet" in title:
                source.setdefault("bwbId", "BWBR0015703")
    return data

def migrate_file(filepath: Path, dry_run: bool = False) -> dict:
    data = json.loads(filepath.read_text())
    version = data.get("schemaVersion", "unknown")
    if version in ("1.0.0", "unknown"):
        if dry_run:
            return {"file": str(filepath), "from": version, "to": "1.1.0", "dry_run": True}
        migrated = migrate_v1_0_to_v1_1(data)
        filepath.write_text(json.dumps(migrated, indent=2, ensure_ascii=False))
        return {"file": str(filepath), "from": version, "to": "1.1.0", "migrated": True}
    return {"file": str(filepath), "version": version, "migrated": False}

if __name__ == "__main__":
    check_only = "--check-only" in sys.argv
    jrem_files = list((REPO_ROOT / "use-cases").glob("*/jrem/exports/*.json"))
    results = []
    for f in sorted(jrem_files):
        result = migrate_file(f, dry_run=check_only)
        results.append(result)
    need_migration = sum(1 for r in results if r.get("from") in ("1.0.0", "unknown"))
    print(f"Checked {len(results)} JREM exports: {need_migration} need migration")
    if not check_only:
        migrated = sum(1 for r in results if r.get("migrated"))
        print(f"Migrated {migrated} exports to v1.1.0")
    sys.exit(0)
