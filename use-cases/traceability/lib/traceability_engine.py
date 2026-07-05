"""Traceability Engine — maps wet → RegelSpraak → JREM → API → database → test → audit."""
import json
from pathlib import Path
from typing import Optional

def build_traceability_matrix(base_dir: Path) -> dict:
    """Build a full traceability matrix across all use cases."""
    import sys
    sys.path.insert(0, str(base_dir / "shared"))
    from registry import list_domains
    domains = list_domains(base_dir / "use-cases")
    
    port_map = {
        "griffierecht": 8490, "procesreglement": 8491, "classificatie": 8492,
        "publicatie": 8493, "bio2": 8494, "forumstandaardisatie": 8495,
        "overheidsstandaarden": 8496, "nora": 8497, "eu-ai-act": 8498,
        "avg-gdpr": 8499, "ncsc": 8500, "nis2": 8501, "btw-tarieven": 8502,
        "ww-uitkering": 8503, "ind-verblijfsregels": 8504, "wmo": 8505,
        "gegevensdelingsbeleid": 8506, "dpia-model": 8507,
        "algoritmeregister": 8508, "data-overheid-dcat": 8509, "api-registratie": 8510,
        "traceability": 8511, "compliance-debt": 8512, "regulatory-impact": 8513,
    }
    
    matrix = []
    for d in domains:
        jrem_dir = base_dir / "use-cases" / d["domain"] / "jrem" / "exports"
        if not jrem_dir.exists(): continue
        for jf in sorted(jrem_dir.glob("*.json")):
            with open(jf) as f: jrem = json.load(f)
            for rule in jrem.get("rules", []):
                sources = [{"title": ref.get("title",""), "section": ref.get("section",""), "url": ref.get("url","")} for ref in rule.get("sourceRefs", [])]
                conditions = rule.get("conditions", {})
                parts = []
                for field, cond in conditions.items():
                    if isinstance(cond, list):
                        parts.append(f"{field} IN ({','.join(repr(v) for v in cond)})")
                    elif isinstance(cond, dict):
                        for op, val in cond.items():
                            sql_op = {"gt": ">", "gte": ">=", "lt": "<", "lte": "<="}.get(op, op)
                            parts.append(f"{field} {sql_op} {val}")
                db_constraint = f"CHECK ({' AND '.join(parts)})" if parts else "-- no conditions"
                
                matrix.append({
                    "ruleId": rule["ruleId"], "ruleName": rule.get("name",""), "domain": d["domain"],
                    "port": port_map.get(d["domain"], 8500), "wetBron": sources, "conditions": conditions,
                    "outcome": rule.get("outcome",{}).get("category",""), "jremFile": jf.name,
                    "jremVersion": jrem.get("version",""), "legalStatus": rule.get("legalStatus",""),
                    "dbConstraint": db_constraint, "apiEndpoint": f"POST /v1/{d['domain']}/calculate",
                    "testReference": f"tests/test_{d['domain'].replace('-','_')}.py",
                    "auditTrail": "GET /v1/audit/{calculationId}",
                })
    return {"matrix": matrix, "totalRules": len(matrix), "totalDomains": len(domains)}

def get_impact_analysis(base_dir: Path, changed_source: str) -> dict:
    """Regulatory impact analysis: which rules are affected by a change in a source?"""
    matrix = build_traceability_matrix(base_dir)
    affected = []
    for entry in matrix["matrix"]:
        for src in entry["wetBron"]:
            if changed_source.lower() in src.get("title","").lower() or changed_source.lower() in src.get("section","").lower():
                affected.append(entry); break
    return {
        "changedSource": changed_source, "affectedRules": len(affected),
        "affectedDomains": list(set(e["domain"] for e in affected)),
        "affectedAPIs": list(set(e["apiEndpoint"] for e in affected)),
        "affectedTests": list(set(e["testReference"] for e in affected)),
        "affectedDBConstraints": [e["dbConstraint"] for e in affected],
        "details": affected,
    }
