import sys
from pathlib import Path
from fastapi import Query
from typing import Optional
SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app
JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("dpia-model", JREM_DIR, 8507)

@app.get("/v1/dpia/vereist")
def dpia_vereist(verwerkingType: str = Query(...), persoonsgegevensType: str = Query("regulier"), monitoring: str = Query("nee"), automatisering: str = Query("nee")):
    """DPIA beslisboom — is een DPIA vereist voor deze verwerking?"""
    vereist = False
    reden = ""
    if verwerkingType == "grootschalig" and persoonsgegevensType == "bijzonder":
        vereist = True; reden = "AVG art. 35 lid 1b: grootschalige verwerking van bijzondere persoonsgegevens"
    elif monitoring == "ja":
        vereist = True; reden = "AVG art. 35 lid 1c: systematische en uitgebreide monitoring"
    elif automatisering == "ja":
        vereist = True; reden = "AVG art. 35 lid 1a: geautomatiseerde besluitvorming met rechtsgevolgen"
    return {"dpiaVereist": vereist, "reden": reden, "bron": "AVG art. 35", "criteria": {"verwerkingType": verwerkingType, "persoonsgegevensType": persoonsgegevensType, "monitoring": monitoring, "automatisering": automatisering}}

if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="127.0.0.1", port=8507)
