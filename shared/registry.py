"""JREM Registry — indexeert alle JREM exports per domein."""
import json
from pathlib import Path
from typing import Optional

def list_domains(base_dir: Path = None) -> list[dict]:
    """List all domains with their versions."""
    if base_dir is None:
        base_dir = Path(__file__).parent.parent / "use-cases"
    domains = []
    for uc_dir in sorted(base_dir.iterdir()):
        if not uc_dir.is_dir():
            continue
        jrem_dir = uc_dir / "jrem" / "exports"
        if not jrem_dir.exists():
            continue
        versions = list_versions(jrem_dir)
        if versions:
            domains.append({
                "domain": uc_dir.name,
                "versions": versions,
                "ruleCount": sum(v["ruleCount"] for v in versions),
                "hasAcceptatie": any(v["hasAcceptatie"] for v in versions),
            })
    return domains

def list_versions(jrem_dir: Path) -> list[dict]:
    """List versions for a domain."""
    versions = []
    for filepath in sorted(jrem_dir.glob("*.json")):
        with open(filepath) as f:
            data = json.load(f)
        versions.append({
            "version": data["version"],
            "validFrom": data["validFrom"],
            "validUntil": data["validUntil"],
            "ruleCount": len(data.get("rules", [])),
            "scenarioCount": len(data.get("scenarios", [])),
            "hasAcceptatie": bool(data.get("metadata", {}).get("juristAccordering", {}).get("geaccondeerdDoor")),
        })
    return versions

def get_domain_status(domain: str, base_dir: Path = None) -> Optional[dict]:
    """Get status for a specific domain."""
    if base_dir is None:
        base_dir = Path(__file__).parent.parent / "use-cases"
    uc_dir = base_dir / domain
    if not uc_dir.exists():
        return None
    jrem_dir = uc_dir / "jrem" / "exports"
    versions = list_versions(jrem_dir) if jrem_dir.exists() else []
    return {
        "domain": domain,
        "versions": versions,
        "ruleCount": sum(v["ruleCount"] for v in versions),
        "scenarioCount": sum(v["scenarioCount"] for v in versions),
        "hasAcceptatie": any(v["hasAcceptatie"] for v in versions),
        "acceptatieType": [json.load(open(f)).get("metadata", {}).get("acceptatieType", "unknown") for f in jrem_dir.glob("*.json")] if jrem_dir.exists() else [],
    }
