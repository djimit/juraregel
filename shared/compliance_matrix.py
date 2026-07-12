"""Multi-framework compliance matrix — alle domeinen in één overzicht."""
import json
from pathlib import Path
from typing import Optional

def get_compliance_matrix(base_dir: Path) -> dict:
    """Retourneer compliance scores over alle use cases."""
    from registry import list_domains
    domains = list_domains(base_dir / "use-cases")
    
    matrix = []
    for d in domains:
        # Load JREM to get rule count and categories
        jrem_dir = base_dir / "use-cases" / d["domain"] / "jrem" / "exports"
        versions = d.get("versions", [])
        rule_count = d.get("ruleCount", 0)
        
        # Determine framework
        framework_map = {
            "griffierecht": "Rechtspraak",
            "procesreglement": "Rechtspraak",
            "classificatie": "Rechtspraak",
            "publicatie": "Rechtspraak/Privacy",
            "bio2": "Informatiebeveiliging",
            "forumstandaardisatie": "Interoperabiliteit",
            "overheidsstandaarden": "Technische standaarden",
            "nora": "Architectuur",
            "eu-ai-act": "AI Regulering",
            "avg-gdpr": "Privacy",
            "ncsc": "Cybersecurity",
        }
        
        framework = framework_map.get(d["domain"], "Onbekend")
        
        matrix.append({
            "domein": d["domain"],
            "framework": framework,
            "regels": rule_count,
            "acceptatie": d.get("hasAcceptatie", False),
            "versies": len(versions),
            "complianceScore": 0.0,  # Would be calculated from actual checks
            "status": "Production" if rule_count >= 15 or d["domain"] in ["griffierecht","bio2","forumstandaardisatie","overheidsstandaarden","nora","ncsc","publicatie"] else "PoC"
        })
    
    return {
        "matrix": matrix,
        "totaal": {
            "domeinen": len(matrix),
            "regels": sum(m["regels"] for m in matrix),
            "geaccepteerd": sum(1 for m in matrix if m["acceptatie"]),
            "productie": sum(1 for m in matrix if m["status"] == "Production"),
            "poc": sum(1 for m in matrix if m["status"] == "PoC"),
        },
        "perFramework": _group_by_framework(matrix),
    }

def _group_by_framework(matrix: list) -> dict:
    from collections import defaultdict
    grouped = defaultdict(lambda: {"domeinen": 0, "regels": 0})
    for m in matrix:
        grouped[m["framework"]]["domeinen"] += 1
        grouped[m["framework"]]["regels"] += m["regels"]
    return dict(grouped)
