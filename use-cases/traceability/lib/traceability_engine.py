"""Traceability Engine — maps wet → RegelSpraak → JREM → API → database → test → audit."""
import hashlib
import json
from pathlib import Path


def _stable_hash(data: dict) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(payload.encode()).hexdigest()


def _test_refs_for_rule(base_dir: Path, domain: str, rule_id: str) -> list[str]:
    test_file = base_dir / "use-cases" / domain / "tests" / f"test_{domain.replace('-', '_')}.py"
    if not test_file.exists():
        return []

    refs = []
    lines = test_file.read_text().splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("def test_"):
            continue
        context = "\n".join(lines[i:i + 20])
        if rule_id in context:
            refs.append(stripped.split("def ", 1)[1].split("(", 1)[0])
    return refs


def _acceptance_status(jrem: dict) -> dict:
    metadata = jrem.get("metadata", {})
    accordering = metadata.get("juristAccordering")
    acceptatie_type = metadata.get("acceptatieType", "draft")
    if accordering and acceptatie_type != "draft":
        jurist_status = "accepted"
    elif acceptatie_type == "draft":
        jurist_status = "missing"
    else:
        jurist_status = "review-required"
    return {
        "acceptatieType": acceptatie_type,
        "juristStatus": jurist_status,
    }


def build_evidence_envelope(
    *,
    base_dir: Path,
    domain: str,
    rule: dict,
    jrem: dict,
    source_refs: list[dict],
    api_endpoint: str,
    port: int,
    db_constraint: str,
    test_reference: str,
) -> dict:
    test_refs = _test_refs_for_rule(base_dir, domain, rule["ruleId"])
    implementation = {
        "constraint": {
            "sql": db_constraint if db_constraint.startswith("CHECK ") else None,
            "status": "generated" if db_constraint.startswith("CHECK ") else "not-applicable",
        },
        "testFile": test_reference,
        "tests": test_refs,
    }
    identity = {
        "domain": domain,
        "ruleSetId": jrem.get("ruleSetId", domain),
        "ruleId": rule["ruleId"],
        "jremVersion": jrem.get("version", ""),
        "sourceRefs": source_refs,
        "apiEndpoint": api_endpoint,
        "dbConstraint": db_constraint,
        "testReference": test_reference,
    }
    return {
        "envelopeId": _stable_hash(identity),
        "domain": domain,
        "ruleSetId": jrem.get("ruleSetId", domain),
        "ruleId": rule["ruleId"],
        "jremVersion": jrem.get("version", ""),
        "maturityLevel": jrem.get("maturityLevel", ""),
        "sourceRefs": source_refs,
        "api": {
            "endpoint": api_endpoint,
            "port": port,
        },
        "decision": {
            "outcome": rule.get("outcome", {}),
            "manualReviewRequired": rule.get("outcome", {}).get("manualReviewRequired", False),
        },
        "implementation": implementation,
        "acceptance": _acceptance_status(jrem),
    }

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
                
                domain = d["domain"]
                port = port_map.get(domain, 8500)
                api_endpoint = f"POST /v1/{domain}/calculate"
                test_reference = f"tests/test_{domain.replace('-','_')}.py"
                entry = {
                    "ruleId": rule["ruleId"], "ruleName": rule.get("name",""), "domain": d["domain"],
                    "port": port, "wetBron": sources, "conditions": conditions,
                    "outcome": rule.get("outcome",{}).get("category",""), "jremFile": jf.name,
                    "jremVersion": jrem.get("version",""), "legalStatus": rule.get("legalStatus",""),
                    "dbConstraint": db_constraint, "apiEndpoint": api_endpoint,
                    "testReference": test_reference,
                    "auditTrail": "GET /v1/audit/{calculationId}",
                }
                entry["evidenceEnvelope"] = build_evidence_envelope(
                    base_dir=base_dir,
                    domain=domain,
                    rule=rule,
                    jrem=jrem,
                    source_refs=sources,
                    api_endpoint=api_endpoint,
                    port=port,
                    db_constraint=db_constraint,
                    test_reference=test_reference,
                )
                matrix.append(entry)
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
