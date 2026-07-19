"""Algoritmeregister + FRIA Rule API."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("algoritmeregister-fria", JREM_DIR, 8545)


@app.get("/v1/algoritmeregister/fria-checklist")
def fria_checklist():
    return {
        "fria_steps": [
            "Doel beschrijven",
            "Rechten/vrijheden identificeren",
            "Kwetsbare groepen beoordelen",
            "Mitigerende maatregelen",
            "Goedkeuring",
            "Publiceren",
        ]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8545)
