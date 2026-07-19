"""COBIT 2019 Rule API — IT Governance."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("cobit", JREM_DIR, 8539)


@app.get("/v1/cobit/domains")
def domains():
    return {"governance": ["EDM"], "management": ["APO", "BAI", "DSS", "MEA"]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8539)
