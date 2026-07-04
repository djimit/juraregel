"""Overheidsstandaarden Compliance Rule API."""
import sys
from pathlib import Path
from fastapi import Query
from typing import Optional

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app, load_jrem

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("overheidsstandaarden", JREM_DIR, 8496)

@app.get("/v1/os/standaarden")
def get_standaarden(categorie: Optional[str] = Query(None), bron: Optional[str] = Query(None)):
    """Lijst van alle overheidsstandaarden."""
    jrem = load_jrem(JREM_DIR, "2025.1")
    standaarden = []
    for rule in jrem.get("rules", []):
        cat = rule["outcome"].get("category", "").replace("os_", "")
        src = rule["sourceRefs"][0].get("title", "").split(" — ")[0] if rule.get("sourceRefs") else ""
        if categorie and categorie.lower() not in cat.lower(): continue
        if bron and bron.lower() not in src.lower(): continue
        standaarden.append({
            "standaardId": rule["ruleId"],
            "naam": rule["name"],
            "categorie": cat,
            "bron": src,
            "url": rule["sourceRefs"][0].get("url", "") if rule.get("sourceRefs") else ""
        })
    return {"standaarden": standaarden, "totaal": len(standaarden)}

@app.get("/v1/os/rapport/{org_id}")
def get_rapport(org_id: str):
    """Compliance rapport per API of service."""
    jrem = load_jrem(JREM_DIR, "2025.1")
    from collections import defaultdict
    per_cat = defaultdict(lambda: {"totaal": 0, "onbekend": 0})
    for rule in jrem.get("rules", []):
        cat = rule["outcome"].get("category", "onbekend").replace("os_", "")
        per_cat[cat]["totaal"] += 1
        per_cat[cat]["onbekend"] += 1
    return {
        "organisatieId": org_id,
        "versie": jrem["version"],
        "totaalStandaarden": len(jrem["rules"]),
        "perCategorie": dict(per_cat),
        "bronnen": ["logius", "forumstandaardisatie", "developer.overheid.nl"]
    }

if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="127.0.0.1", port=8496)
