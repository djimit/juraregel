"""ISO 27001 ISMS Rule API + Statement of Applicability Generator."""

import json
import sys
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("iso27001", JREM_DIR, 8526)

# ─── BIO2 → ISO 27001 Annex A Mapping ──────────────────────
BIO2_TO_ISO = {
    "A.5-6": ["A.5.1.1", "A.6.1.1", "A.6.1.2"],
    "A.8": ["A.8.1", "A.8.2", "A.8.3"],
    "A.10": ["A.8.24", "A.8.11"],
    "A.11": ["A.7.1", "A.7.4", "A.8.16"],
    "B.3": ["A.8.28", "A.8.9"],
    "C.6-7": ["A.8.16", "A.8.12"],
}

# ─── SoA Generator ──────────────────────────────────────────


@app.post("/v1/iso27001/soa/generate")
def generate_soa(assets: list[dict] | None = None):
    """Genereert Statement of Applicability uit asset register + BIO2 compliance."""
    jrem_path = JREM_DIR / "iso27001-2026.1.json"
    with open(jrem_path) as f:
        jrem = json.load(f)

    soa_controls = [r for r in jrem["rules"] if r["outcome"].get("control")]

    soa = {
        "document": "Statement of Applicability",
        "standard": "ISO/IEC 27001:2022 Annex A",
        "generated_at": date.today().isoformat(),
        "version": "1.0",
        "controls": [],
    }

    for control in soa_controls:
        entry = {
            "control_id": control["outcome"]["control"],
            "name": control["name"],
            "applicable": True,
            "implementation_status": "pending",
            "justification": "",
            "linked_bio2": BIO2_TO_ISO.get(control["outcome"]["control"], []),
        }
        soa["controls"].append(entry)

    soa["total_controls"] = len(soa["controls"])
    soa["applicable"] = sum(1 for c in soa["controls"] if c["applicable"])

    return soa


@app.get("/v1/iso27001/soa/template")
def soa_template():
    """Geeft lege SoA-template conform ISO 27001:2022."""
    return {
        "document": "Statement of Applicability Template",
        "standard": "ISO/IEC 27001:2022 Annex A",
        "sections": [
            {"id": "A.5", "name": "Organizational controls", "controls": 37},
            {"id": "A.6", "name": "People controls", "controls": 8},
            {"id": "A.7", "name": "Physical controls", "controls": 14},
            {"id": "A.8", "name": "Technological controls", "controls": 34},
        ],
        "total": 93,
        "fields_per_control": [
            "control_id",
            "control_name",
            "applicable",
            "implementation_status",
            "justification",
            "linked_policy",
            "responsible",
            "bio2_mapping",
        ],
        "implementation_status_options": [
            "not_applicable",
            "planned",
            "in_progress",
            "implemented",
            "not_implemented",
        ],
    }


@app.post("/v1/iso27001/risico/behandeling")
def risicobehandeling(risico_score: int):
    """Bepaalt risicobehandelingsstrategie conform ISO 27001:2022 6.1.3."""
    if risico_score <= 4:
        return {
            "strategie": "accepteeren",
            "actie": "Risico is acceptabel",
            "score": risico_score,
        }
    elif risico_score <= 14:
        return {
            "strategie": "verminderen",
            "actie": "Implementeer maatregelen",
            "score": risico_score,
        }
    else:
        return {
            "strategie": "vermijden",
            "actie": "Stop verwerking of zware maatregelen",
            "score": risico_score,
        }


@app.get("/v1/iso27001/isms/documenten")
def isms_documenten():
    """Lijst van 7 verplichte ISMS-documenten conform ISO 27001:2022."""
    return {
        "standard": "ISO/IEC 27001:2022",
        "verplichte_documenten": [
            {
                "id": "isms-4.3",
                "naam": "Scope van het ISMS",
                "clausule": "4.3",
                "status": "template_available",
            },
            {
                "id": "isms-5.2",
                "naam": "Beleid voor informatiebeveiliging",
                "clausule": "5.2",
                "status": "template_available",
            },
            {
                "id": "isms-6.1.2",
                "naam": "Risicoanalyse",
                "clausule": "6.1.2",
                "status": "template_available",
            },
            {
                "id": "isms-6.1.3",
                "naam": "Risicobehandelingsplan",
                "clausule": "6.1.3",
                "status": "rule_based",
            },
            {
                "id": "isms-6.1.3d",
                "naam": "Statement of Applicability",
                "clausule": "6.1.3d",
                "status": "generator_available",
            },
            {
                "id": "isms-6.2",
                "naam": "Doelstellingen voor informatiebeveiliging",
                "clausule": "6.2",
                "status": "template_available",
            },
            {
                "id": "isms-8.2",
                "naam": "Rapport van de beoordeling van de risico's",
                "clausule": "8.2",
                "status": "template_available",
            },
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8526)
