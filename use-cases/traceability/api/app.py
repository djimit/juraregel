import sys
from pathlib import Path
from fastapi import Query
SHARED = Path(__file__).parent.parent.parent.parent / "shared"
BASE = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(SHARED))
from api_base import create_app
JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("traceability", JREM_DIR, 8511)

@app.get("/v1/traceability/matrix")
def get_matrix():
    sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
    from traceability_engine import build_traceability_matrix
    return build_traceability_matrix(BASE)

@app.get("/v1/impact/analyze")
def analyze_impact(source: str = Query(...)):
    sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
    from traceability_engine import get_impact_analysis
    return get_impact_analysis(BASE, source)

if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="127.0.0.1", port=8511)
