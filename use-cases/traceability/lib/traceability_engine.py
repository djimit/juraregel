"""Traceability Engine — maps wet → RegelSpraak → JREM → API → database → test → audit."""
import ast
import hashlib
import json
from pathlib import Path


def _stable_hash(data: dict) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(payload.encode()).hexdigest()


def _test_files(base_dir: Path, domain: str) -> list[Path]:
    return sorted((base_dir / "use-cases" / domain / "tests").glob("test_*.py"))


def _test_refs_for_rule(base_dir: Path, domain: str, rule_id: str) -> list[str]:
    refs = []
    for test_file in _test_files(base_dir, domain):
        tree = ast.parse(test_file.read_text())
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or not node.name.startswith("test_"):
                continue
            literals = {
                child.value for child in ast.walk(node)
                if isinstance(child, ast.Constant) and isinstance(child.value, str)
            }
            if rule_id in literals:
                refs.append(f"{test_file.relative_to(base_dir)}::{node.name}")
    return refs


def _acceptance_status(jrem: dict) -> dict:
    metadata = jrem.get("metadata", {})
    approval = jrem.get("approval") or {}
    accordering = metadata.get("juristAccordering") or approval
    acceptatie_type = metadata.get("acceptatieType", "draft")
    independent = approval.get("type") in {"peer-review", "legal-team", "external"}
    if accordering and independent and acceptatie_type != "draft":
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
        "status": "observed" if test_refs else "unverified",
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
        "rulesetHash": _stable_hash(jrem),
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
    from registry import can_calculate, list_domains
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
        "toeslagen": 8514, "omgevingswet": 8515, "basisregistraties": 8516,
        "participatiewet": 8517,
        "judicial-ai-assurance": 8521,
        "itgc-kader": 8522,
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
                db_constraint = "-- not materialized"
                
                domain = d["domain"]
                port = port_map.get(domain)
                api_endpoint = f"POST /v1/{domain}/calculate" if can_calculate(domain) else None
                test_files = _test_files(base_dir, domain)
                test_reference = str(test_files[0].relative_to(base_dir)) if test_files else None
                entry = {
                    "ruleId": rule["ruleId"], "ruleName": rule.get("name",""), "domain": d["domain"],
                    "port": port, "wetBron": sources, "conditions": conditions,
                    "outcome": rule.get("outcome",{}).get("category",""), "jremFile": jf.name,
                    "jremVersion": jrem.get("version",""), "legalStatus": rule.get("legalStatus",""),
                    "dbConstraint": db_constraint, "apiEndpoint": api_endpoint,
                    "testReference": test_reference,
                    "auditTrail": "GET /v1/audit/{calculationId}" if api_endpoint else None,
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
        "affectedAPIs": sorted({e["apiEndpoint"] for e in affected if e["apiEndpoint"]}),
        "affectedTests": sorted({e["testReference"] for e in affected if e["testReference"]}),
        "affectedDBConstraints": [e["dbConstraint"] for e in affected],
        "details": affected,
    }
