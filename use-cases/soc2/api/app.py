"""SOC 2 Rule API — Service Organization Controls."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("soc2", JREM_DIR, 8540)


@app.get("/v1/soc2/trust-services")
def trust_services():
    return {
        "criteria": [
            "Common Criteria (CC)",
            "Availability (A)",
            "Processing Integrity (PI)",
            "Confidentiality (C)",
            "Privacy (P)",
        ]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8540)
