"""ISO 27701 API — Privacy Information Management System."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("iso27701", JREM_DIR, 8531)


@app.get("/v1/iso27701/rollen")
def rollen():
    """Toont de twee rollen in ISO 27701."""
    return {
        "PII Controller": {
            "description": "Bepaalt doel en middelen van verwerking",
            "verplichtingen": [
                "Privacy policy",
                "Consent management",
                "Data subject rights",
                "DPIA",
                "Breach notification",
            ],
            "avg_basis": "Art. 4(7), 5-22",
        },
        "PII Processor": {
            "description": "Verwerkt PII in opdracht van controller",
            "verplichtingen": [
                "DPA",
                "Sub-processing",
                "Security measures",
                "Breach notification",
            ],
            "avg_basis": "Art. 4(8), 28",
        },
    }


@app.get("/v1/iso27701/avg-mapping")
def avg_mapping():
    """Toont de mapping tussen ISO 27701 en AVG artikelen."""
    return {
        "description": "ISO 27701 operationaliseert de AVG door middel van beheersmaatregelen",
        "mapping": [
            {
                "iso27701": "7.2.2",
                "avg": "Art. 13-14",
                "onderwerp": "Transparantie en informatie",
            },
            {
                "iso27701": "7.2.4",
                "avg": "Art. 5.1c",
                "onderwerp": "Data minimalisatie",
            },
            {"iso27701": "7.2.5", "avg": "Art. 6-7", "onderwerp": "Toestemming"},
            {
                "iso27701": "7.2.6",
                "avg": "Art. 12-22",
                "onderwerp": "Betrokkenenrechten",
            },
            {"iso27701": "7.2.7", "avg": "Art. 35", "onderwerp": "DPIA"},
            {"iso27701": "7.2.8", "avg": "Art. 35.3", "onderwerp": "DPIA hoog risico"},
            {
                "iso27701": "7.2.9",
                "avg": "Art. 44-49",
                "onderwerp": "Internationale doorgifte",
            },
            {"iso27701": "7.2.10", "avg": "Art. 33-34", "onderwerp": "Datalek melding"},
            {
                "iso27701": "7.2.11",
                "avg": "Art. 5.1e, 17",
                "onderwerp": "Bewaartermijn + wissing",
            },
            {
                "iso27701": "7.3.2",
                "avg": "Art. 28",
                "onderwerp": "Verwerkersovereenkomst",
            },
        ],
    }


@app.post("/v1/iso27701/pii-rol-bepaling")
def pii_rol_bepaling(
    beschikt_over_doel: bool,
    beschikt_over_middelen: bool,
    opdracht_van: str | None = None,
):
    """Bepaal of je PII Controller of Processor bent."""
    if beschikt_over_doel and beschikt_over_middelen:
        return {
            "rol": "PII Controller",
            "uitleg": "Jullie bepalen het doel en de middelen van de verwerking",
            "belangrijkste_verplichtingen": [
                "Privacy policy publiceren (Art. 13-14 AVG)",
                "Toestemming beheren (Art. 6-7 AVG)",
                "Betrokkenenrechten faciliteren (Art. 12-22 AVG)",
                "DPIA uitvoeren bij hoog risico (Art. 35 AVG)",
                "Datalek melden binnen 72u (Art. 33 AVG)",
            ],
            "iso27701_secties": [
                "7.2.2",
                "7.2.3",
                "7.2.4",
                "7.2.5",
                "7.2.6",
                "7.2.7",
                "7.2.8",
                "7.2.10",
            ],
        }
    elif opdracht_van:
        return {
            "rol": "PII Processor",
            "uitleg": f"Jullie verwerken PII in opdracht van {opdracht_van}",
            "belangrijkste_verplichtingen": [
                "Verwerkersovereenkomst afsluiten (Art. 28 AVG)",
                "Sub-processing managen (Art. 28.3 AVG)",
                "Beveiligingsmaatregelen implementeren (Art. 32 AVG)",
                "Datalek melden aan controller (Art. 33 AVG)",
            ],
            "iso27701_secties": ["7.3.2", "7.3.3", "7.3.4"],
        }
    else:
        return {
            "rol": "Onbepaald",
            "uitleg": "Onvoldoende informatie — neem contact op met een privacy-expert",
            "tip": "Bij twijfel: je bent waarschijnlijk Controller",
        }


@app.get("/v1/iso27701/certificering-pad")
def certificering_pad():
    """Toont het pad naar ISO 27701-certificering."""
    return {
        "stappen": [
            {
                "stap": 1,
                "actie": "ISO 27001 certificering behalen (vereiste)",
                "duur": "6-12 maanden",
            },
            {"stap": 2, "actie": "PIMS gap-analyse uitvoeren", "duur": "2-4 weken"},
            {
                "stap": 3,
                "actie": "Privacy by design implementeren",
                "duur": "4-8 weken",
            },
            {"stap": 4, "actie": "DPIA-proces opzetten", "duur": "2-4 weken"},
            {"stap": 5, "actie": "Documentatie + procedures", "duur": "4-6 weken"},
            {"stap": 6, "actie": "Interne audit", "duur": "2-4 weken"},
            {"stap": 7, "actie": "Certificeringsaudit", "duur": "2-4 weken"},
        ],
        "totaal_geschat": "9-18 maanden",
        "kosten_geschat": "€15.000-€75.000 (afhankelijk van organisatiegrootte)",
        "voordelen": [
            "Internationale erkenning (ISO-norm)",
            "AVG-compliance aantoonbaar",
            "Concurrentievoordeel bij aanbestedingen",
            "Verlaagd boeterisico",
            "Vertrouwen van burgers en partners",
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8531)
