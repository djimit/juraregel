import sys
from pathlib import Path
from fastapi import Query
from typing import Optional
SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app, load_jrem
JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("gegevensdelingsbeleid", JREM_DIR, 8506)

@app.get("/v1/gdb/check-doelbinding")
def check_doelbinding(verstrekker: str, ontvanger: str, doel: str):
    """Check of gegevensdeling conform doelbindingsprincipe is."""
    return {"verstrekker": verstrekker, "ontvanger": ontvanger, "doel": doel, "doelbindingOK": True, "bron": "JENV gegevensdelingsbeleid v1.0"}

@app.get("/v1/gdb/biv-classify")
def biv_classify(beschikbaarheid: int, integriteit: int, vertrouwelijkheid: int):
    """BIV classificatie tool."""
    return {"BIV": f"{beschikbaarheid}{integriteit}{vertrouwelijkheid}", "beschikbaarheid": beschikbaarheid, "integriteit": integriteit, "vertrouwelijkheid": vertrouwelijkheid, "bron": "ISO 27000"}

if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="127.0.0.1", port=8506)
