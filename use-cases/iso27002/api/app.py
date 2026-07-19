"""ISO 27002 API — Security Controls with BIO2 mapping."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("iso27002", JREM_DIR, 8530)

# ─── BIO2 → ISO 27002 Mapping ──────────────────────────────
BIO2_TO_ISO27002 = {
    "A.5-6": ["A.5.1", "A.5.7", "A.5.9", "A.5.12"],
    "A.7": ["A.6.1", "A.6.2", "A.6.3", "A.6.5", "A.6.6"],
    "A.8": ["A.5.9", "A.5.12", "A.5.33", "A.5.34"],
    "A.9": ["A.5.14"],
    "A.10": ["A.8.24"],
    "B.3": ["A.8.9", "A.8.8", "A.8.28"],
    "B.4": ["A.8.11", "A.8.12"],
    "B.5": ["A.8.1", "A.8.2", "A.8.3", "A.8.5"],
    "B.6": ["A.8.23"],
    "B.7": ["A.7.1", "A.7.4", "A.7.9"],
    "B.8": ["A.8.16"],
    "B.9": ["A.8.16"],
    "B.10": ["A.8.15"],
    "B.11": ["A.7.11"],
    "B.12": ["A.8.16"],
    "B.13": ["A.7.11"],
    "C.4": ["A.8.15", "A.8.16"],
    "C.6-7": ["A.8.16", "A.8.12"],
}


# ─── ISO 27002 → BIO2 Reverse Mapping ─────────────────────
def get_bio2_mapping(iso_control: str) -> list[str]:
    """Geef BIO2-maatregelen die horen bij een ISO 27002 control."""
    result = []
    for bio2, iso_list in BIO2_TO_ISO27002.items():
        if iso_control in iso_list:
            result.append(bio2)
    return result


@app.get("/v1/iso27002/bio2-mapping")
def bio2_mapping():
    """Toont de volledige BIO2 → ISO 27002 mapping."""
    return {
        "description": "BIO2 (Baseline Informatiebeveiliging Overheid) is gebaseerd op ISO 27002",
        "mapping": BIO2_TO_ISO27002,
        "total_bio2_controls": len(BIO2_TO_ISO27002),
        "total_iso_controls_mapped": len(
            set(c for controls in BIO2_TO_ISO27002.values() for c in controls)
        ),
        "note": "Elke BIO2-maatregel kan worden herleid tot ISO 27002-compliantie",
    }


@app.get("/v1/iso27002/controls-by-category")
def controls_by_category():
    """Geef controls gegroepeerd per categorie."""
    return {
        "organizational": {
            "theme": "A.5",
            "count": 36,
            "focus": "Beleid, rollen, classificatie, privacy",
        },
        "people": {
            "theme": "A.6",
            "count": 8,
            "focus": "Screening, training, vertrouwelijkheid",
        },
        "physical": {
            "theme": "A.7",
            "count": 14,
            "focus": "Perimeters, monitoring, utilities",
        },
        "technological": {
            "theme": "A.8",
            "count": 35,
            "focus": "Access, crypto, coding, monitoring",
        },
        "total": 93,
    }


@app.get("/v1/iso27002/compliance-gap/{org_id}")
def compliance_gap(org_id: str):
    """Analyseer gaten tussen BIO2 en ISO 27002."""
    return {
        "org_id": org_id,
        "analysis": "BIO2-compliance impliceert ~85% ISO 27002-compliantie",
        "gaps": [
            {
                "control": "A.5.7",
                "description": "Threat intelligence",
                "bio2_coverage": "partial",
            },
            {
                "control": "A.8.8",
                "description": "Vulnerability management",
                "bio2_coverage": "partial",
            },
            {
                "control": "A.8.28",
                "description": "Secure coding",
                "bio2_coverage": "minimal",
            },
        ],
        "recommendation": "BIO2-certificatie als basis, ISO 27002 als uitbreiding voor technische controls",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8530)
