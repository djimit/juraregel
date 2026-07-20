"""ADR ITGC-kader v1.1 — brongebonden catalogus-API."""

import sys
from pathlib import Path
from typing import Optional

from fastapi import Query


SHARED = Path(__file__).parents[3] / "shared"
sys.path.insert(0, str(SHARED))

from api_base import create_app, load_jrem


JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("itgc-kader", JREM_DIR, 8522)


@app.get("/v1/itgc-kader/maatregelen")
def get_maatregelen(doelstelling: Optional[str] = Query(None)):
    """Geef maatregelen en toetsingscriteria terug; nooit een compliance-score."""
    rules = load_jrem(JREM_DIR, "2026.1")["rules"]
    if doelstelling:
        prefix = doelstelling.upper().rstrip(".") + "."
        rules = [rule for rule in rules if rule["ruleId"].removeprefix("ITGC-").startswith(prefix)]
    maatregelen = [rule["outcome"]["itgc"] for rule in rules]
    return {
        "versie": "2026.1",
        "assessmentStatus": "insufficient_evidence",
        "maatregelen": maatregelen,
        "totaalMaatregelen": len(maatregelen),
        "totaalToetsingscriteria": sum(len(item["testCriteria"]) for item in maatregelen),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8522)
