"""NORA Compliance Rule API — meta-laag bovenop alle use cases."""
import sys
from pathlib import Path
from fastapi import Query
from typing import Optional

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app, load_jrem

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("nora", JREM_DIR, 8497)

@app.get("/v1/nora/principes")
def get_principes(categorie: Optional[str] = Query(None)):
    """Lijst van alle NORA principes met gekoppelde use cases."""
    jrem = load_jrem(JREM_DIR, "2025.1")
    principes = []
    for rule in jrem.get("rules", []):
        cat = rule["outcome"].get("category", "").replace("nora_", "")
        if categorie and categorie.lower() not in cat.lower(): continue
        principes.append({
            "principeId": rule["ruleId"],
            "naam": rule["name"],
            "categorie": cat,
            "url": rule["sourceRefs"][0].get("url", "") if rule.get("sourceRefs") else ""
        })
    return {"principes": principes, "totaal": len(principes)}

@app.get("/v1/nora/matrix")
def get_nora_matrix():
    """NORA compliance matrix — mapping van principes naar JuraRegel use cases."""
    jrem = load_jrem(JREM_DIR, "2025.1")
    matrix = []
    for rule in jrem.get("rules", []):
        cat = rule["outcome"].get("category", "").replace("nora_", "")
        matrix.append({
            "principeId": rule["ruleId"],
            "principe": rule["name"],
            "categorie": cat,
            "gekoppeldeUseCases": [],
            "compliant": "onbekend"
        })
    return {"matrix": matrix, "totaal": len(matrix), "useCases": ["griffierecht","procesreglement","classificatie","publicatie","bio2","forumstandaardisatie","overheidsstandaarden"]}

if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="127.0.0.1", port=8497)
