"""ISO 9001 API — Quality Management System."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("iso9001", JREM_DIR, 8534)


@app.get("/v1/iso9001/pdca")
def pdca():
    """Toont het PDCA-cyclus model van ISO 9001."""
    return {
        "standard": "ISO 9001:2015",
        "model": "Plan-Do-Check-Act",
        "phases": [
            {
                "phase": "Plan",
                "clauses": "4-6",
                "activities": [
                    "Context",
                    "Leadership",
                    "Risk & opportunities",
                    "Quality objectives",
                ],
            },
            {
                "phase": "Do",
                "clauses": "7-8",
                "activities": ["Resources", "Competence", "Operation", "Control"],
            },
            {
                "phase": "Check",
                "clauses": "9",
                "activities": ["Monitoring", "Internal audit", "Management review"],
            },
            {
                "phase": "Act",
                "clauses": "10",
                "activities": ["Corrective action", "Continual improvement"],
            },
        ],
    }


@app.post("/v1/iso9001/maturity")
def maturity(scores: dict):
    """Bepaal QMS maturity niveau."""
    avg = sum(scores.values()) / len(scores) if scores else 0
    if avg >= 90:
        level, description = "Optimized", "Continual improvement volwassen"
    elif avg >= 75:
        level, description = "Managed", "Gemeten en beheersbaar"
    elif avg >= 60:
        level, description = "Defined", "Gestandaardiseerd en gedocumenteerd"
    elif avg >= 40:
        level, description = "Developing", "Basisprocessen aanwezig"
    else:
        level, description = "Initial", "Ad-hoc, ongestructureerd"

    return {
        "overall_score": round(avg, 1),
        "maturity_level": level,
        "description": description,
        "next_steps": [
            "Verbeter laagste scores eerst"
            if min(scores.values()) < 60
            else "Focus op continual improvement",
            "Interne audit plannen"
            if scores.get("internal_audit", 0) < 70
            else "Audit-resultaten monitoren",
        ],
    }


@app.get("/v1/iso9001/iso-combinatie")
def iso_combinatie():
    """Toont hoe ISO 9001 combineert met andere ISO-normen."""
    return {
        "description": "ISO 9001 is de basis voor geïntegreerde managementsystemen",
        "combinaties": [
            {
                "combo": "ISO 9001 + ISO 27001",
                "name": "Quality + Information Security",
                "voordeel": "Gedeelde PDCA-cyclus, risico-gedreven",
            },
            {
                "combo": "ISO 9001 + ISO 14001",
                "name": "Quality + Environment",
                "voordeel": "Gedeelde processen, duurzaamheid",
            },
            {
                "combo": "ISO 9001 + ISO 22301",
                "name": "Quality + Business Continuity",
                "voordeel": "Kwaliteit tijdens disruptie",
            },
            {
                "combo": "ISO 9001 + ISO 25010",
                "name": "Quality + Software Quality",
                "voordeel": "Productkwaliteit meetbaar",
            },
            {
                "combo": "ISO 9001 + ISO 31000",
                "name": "Quality + Risk",
                "voordeel": "Risico-gedreven kwaliteitsverbetering",
            },
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8534)
