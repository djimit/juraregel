"""NCSC Cybersecurity Rule API."""
import sys
from pathlib import Path
from fastapi import Query
from typing import Optional
SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app, load_jrem
JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("ncsc", JREM_DIR, 8500)

@app.get("/v1/ncsc/richtlijnen")
def get_richtlijnen(categorie: Optional[str] = Query(None)):
    """Lijst van alle NCSC richtlijnen."""
    jrem = load_jrem(JREM_DIR, "2025.1")
    richtlijnen = []
    for rule in jrem.get("rules", []):
        cat = rule["outcome"].get("category", "").replace("ncsc_", "")
        if categorie and categorie.lower() not in cat.lower(): continue
        richtlijnen.append({"regelId": rule["ruleId"], "naam": rule["name"], "categorie": cat,
            "url": rule["sourceRefs"][0].get("url", "") if rule.get("sourceRefs") else ""})
    return {"richtlijnen": richtlijnen, "totaal": len(richtlijnen)}

@app.get("/v1/ncsc/rapport/{org_id}")
def get_rapport(org_id: str):
    """NCSC compliance rapport per organisatie."""
    jrem = load_jrem(JREM_DIR, "2025.1")
    from collections import defaultdict
    per_cat = defaultdict(lambda: {"totaal": 0, "onbekend": 0})
    for rule in jrem.get("rules", []):
        cat = rule["outcome"].get("category", "onbekend").replace("ncsc_", "")
        per_cat[cat]["totaal"] += 1
        per_cat[cat]["onbekend"] += 1
    return {"organisatieId": org_id, "versie": jrem["version"], "totaalRichtlijnen": len(jrem["rules"]),
            "perCategorie": dict(per_cat), "bron": "ncsc.nl"}

if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="127.0.0.1", port=8500)
