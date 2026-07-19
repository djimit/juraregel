"""PCI DSS v4.0 Rule API — Payment Card Security."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("pci-dss", JREM_DIR, 8538)


@app.get("/v1/pci-dss/requirements")
def requirements():
    return {
        "total": 12,
        "categories": [
            "Network",
            "Data protection",
            "Vulnerability",
            "Access",
            "Monitoring",
            "Policy",
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8538)
