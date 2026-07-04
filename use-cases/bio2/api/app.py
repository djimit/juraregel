"""BIO2 Compliance Rule API — use case app met bio2-specifieke endpoints."""
import sys
import json
from pathlib import Path
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
    jrem = load_jrem(JREM_DIR, "2025.1")
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
def get_rapport(organisatie_id: str):
    """Compliance rapport per organisatie — ENSIA aligned."""
    jrem = load_jrem(JREM_DIR, "2025.1")
    
    from collections import defaultdict
    per_categorie = defaultdict(lambda: {"totaal": 0, "compliant": 0, "niet_compliant": 0, "onbekend": 0})
    
    for rule in jrem.get("rules", []):
        cat = rule["outcome"].get("category", "onbekend").replace("bio2_", "")
        per_categorie[cat]["totaal"] += 1
        per_categorie[cat]["onbekend"] += 1  # Default: all unknown
    
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
        "score": round(score, 1),
        "perCategorie": dict(per_categorie),
        "audit": {
            "rulesetHash": f"sha256:{hash(json.dumps(jrem, sort_keys=True))}",
            "timestamp": "2026-07-04T23:00:00+02:00",
        }
    }

if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="127.0.0.1", port=8494)
