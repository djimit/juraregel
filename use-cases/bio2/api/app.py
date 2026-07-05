"""BIO2 Compliance Rule API — use case app met bio2-specifieke endpoints."""
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from fastapi import Query
from typing import Optional

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app
from api_base import load_jrem, list_versions

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("bio2", JREM_DIR, 8494)

# BIO2-specific endpoints
@app.get("/v1/bio2/maatregelen")
def get_maatregelen(categorie: Optional[str] = Query(None)):
    """Lijst van alle BIO2 maatregelen met id, categorie, isoRef, beschrijving."""
    jrem = load_jrem(JREM_DIR, "2026.1")
    maatregelen = []
    for rule in jrem.get("rules", []):
        rid = rule["ruleId"].replace("BIO2-", "")
        cat = rule["outcome"].get("category", "").replace("bio2_", "")
        iso_ref = ""
        for ref in rule.get("sourceRefs", []):
            if "ISO 27002" in ref.get("title", ""):
                iso_ref = ref.get("section", "")
                break
        if categorie and categorie.lower() not in cat.lower():
            continue
        maatregelen.append({
            "maatregelId": rid,
            "categorie": cat,
            "isoRef": iso_ref,
            "beschrijving": rule["name"][:120],
        })
    return {"maatregelen": maatregelen, "totaal": len(maatregelen)}

@app.get("/v1/bio2/rapport/{organisatie_id}")
def get_rapport(organisatie_id: str, evidence: Optional[str] = Query(None)):
    """Evidence-based compliance rapport. Evidence als JSON string."""
    import hashlib
    from collections import defaultdict
    from datetime import datetime, timezone
    
    jrem = load_jrem(JREM_DIR, "2026.1")
    
    # Parse evidence input
    evidence_map = {}
    if evidence:
        try:
            ev_data = json.loads(evidence)
            for item in ev_data:
                evidence_map[item.get("maatregelId", "")] = item
        except (json.JSONDecodeError, TypeError):
            pass
    
    per_categorie = defaultdict(lambda: {"totaal": 0, "compliant": 0, "niet_compliant": 0, "onbekend": 0, "geen_evidence": 0})
    
    for rule in jrem.get("rules", []):
        cat = rule["outcome"].get("category", "onbekend").replace("bio2_", "")
        rid = rule["ruleId"].replace("BIO2-", "")
        per_categorie[cat]["totaal"] += 1
        
        ev = evidence_map.get(rid, {})
        status = ev.get("status", "geen_evidence")
        
        if status == "compliant":
            per_categorie[cat]["compliant"] += 1
        elif status == "niet_compliant":
            per_categorie[cat]["niet_compliant"] += 1
        elif status == "onbekend":
            per_categorie[cat]["onbekend"] += 1
        else:
            per_categorie[cat]["geen_evidence"] += 1
    
    totaal = sum(v["totaal"] for v in per_categorie.values())
    compliant = sum(v["compliant"] for v in per_categorie.values())
    score = compliant / max(totaal, 1) * 100
    
    return {
        "organisatieId": organisatie_id,
        "bioVersie": jrem["version"],
        "totaalMaatregelen": totaal,
        "compliant": compliant,
        "nietCompliant": sum(v["niet_compliant"] for v in per_categorie.values()),
        "onbekend": sum(v["onbekend"] for v in per_categorie.values()),
        "geenEvidence": sum(v["geen_evidence"] for v in per_categorie.values()),
        "score": round(score, 1),
        "perCategorie": dict(per_categorie),
        "audit": {
            "rulesetHash": hashlib.sha256(json.dumps(jrem, sort_keys=True).encode()).hexdigest(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "evidenceCount": len(evidence_map),
        }
    }

@app.post("/v1/bio2/evidence")
def submit_evidence(evidence: list):
    """Submit evidence for compliance assessment."""
    processed = []
    for item in evidence:
        processed.append({
            "maatregelId": item.get("maatregelId"),
            "status": item.get("status", "onbekend"),
            "evidenceType": item.get("evidenceType", "onbekend"),
            "hash": hashlib.sha256(json.dumps(item, sort_keys=True).encode()).hexdigest(),
            "receivedAt": datetime.now(timezone.utc).isoformat(),
        })
    return {"received": len(processed), "evidence": processed}

if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="127.0.0.1", port=8494)
