"""Forum Standaardisatie Compliance Rule API."""
import sys
from pathlib import Path
from fastapi import Query
from typing import Optional

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app, load_jrem

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("forumstandaardisatie", JREM_DIR, 8495)

@app.get("/v1/fs/standaarden")
def get_standaarden(categorie: Optional[str] = Query(None), status: Optional[str] = Query(None)):
    """Lijst van alle verplichte en streefbeeld standaarden."""
    jrem = load_jrem(JREM_DIR, "2025.1")
    standaarden = []
    for rule in jrem.get("rules", []):
        rid = rule["ruleId"].replace("FS-FS-", "FS-")
        cat = rule["outcome"].get("category", "").replace("fs_", "")
        parts = cat.split("_") if "_" in cat else [cat, ""]
        cat_name = parts[0] if len(parts) > 0 else cat
        stat = parts[1] if len(parts) > 1 else ""
        if categorie and categorie.lower() not in cat_name.lower():
            continue
        if status and status.lower() not in stat.lower():
            continue
        standaarden.append({
            "standaardId": rid,
            "naam": rule["name"],
            "categorie": cat_name,
            "status": stat,
            "url": rule["sourceRefs"][0].get("url", "") if rule.get("sourceRefs") else ""
        })
    return {"standaarden": standaarden, "totaal": len(standaarden)}

@app.get("/v1/fs/rapport/{org_id}")
def get_rapport(org_id: str):
    """Monitor Open Standaarden aligned compliance rapport."""
    jrem = load_jrem(JREM_DIR, "2025.1")
    from collections import defaultdict
    per_cat = defaultdict(lambda: {"verplicht": 0, "streefbeeld": 0, "onbekend": 0})
    for rule in jrem.get("rules", []):
        cat = rule["outcome"].get("category", "onbekend").replace("fs_", "")
        parts = cat.split("_")
        cat_name = parts[0] if len(parts) > 0 else cat
        stat = parts[1] if len(parts) > 1 else ""
        if stat == "verplicht":
            per_cat[cat_name]["verplicht"] += 1
        elif stat == "streefbeeld":
            per_cat[cat_name]["streefbeeld"] += 1
        per_cat[cat_name]["onbekend"] += 1
    totaal = sum(v["verplicht"] + v["streefbeeld"] for v in per_cat.values())
    return {
        "organisatieId": org_id,
        "monitorVersie": jrem["version"],
        "totaalStandaarden": totaal,
        "perCategorie": dict(per_cat),
        "bron": "forumstandaardisatie.nl"
    }

if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="127.0.0.1", port=8495)
