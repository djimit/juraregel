"""Wet Digitale Overheid Rule API."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("wdo", JREM_DIR, 8528)


@app.get("/v1/wdo/linked-frameworks")
def linked_frameworks():
    """Toont welke bestaande use cases gekoppeld zijn aan Wdo."""
    return {
        "wdo_rules": 17,
        "linked_frameworks": [
            {
                "id": "forumstandaardisatie",
                "port": 8495,
                "koppeling": "Wdo Art. 2.1 — Open standaarden",
            },
            {
                "id": "overheidsstandaarden",
                "port": 8496,
                "koppeling": "Wdo Art. 2.2 — API Design Rules",
            },
            {
                "id": "bio2",
                "port": 8494,
                "koppeling": "Wdo Art. 5.1 — Veilige dienstverlening",
            },
            {"id": "nis2", "port": 8501, "koppeling": "Wdo Art. 5.1 — Beveiliging"},
            {
                "id": "eidas",
                "port": 8523,
                "koppeling": "Wdo Art. 5.2 — Identiteitsvoorziening",
            },
            {
                "id": "dpia-generator",
                "port": 8525,
                "koppeling": "Wdo Art. 6.2 — DPIA verplicht",
            },
            {"id": "nora", "port": 8497, "koppeling": "Wdo Art. 7.1 — Architectuur"},
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8528)
