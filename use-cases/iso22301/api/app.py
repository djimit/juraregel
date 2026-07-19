"""ISO 22301 API — Business Continuity Management System."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("iso22301", JREM_DIR, 8532)


@app.get("/v1/iso22301/bcms-lifecycle")
def bcms_lifecycle():
    """Toont het BCMS levenscyclus model."""
    return {
        "standard": "ISO 22301:2018",
        "phases": [
            {
                "id": "plan",
                "name": "Plan",
                "activities": [
                    "Context",
                    "Leadership",
                    "Policy",
                    "Risk assessment",
                    "BIA",
                    "Strategy",
                ],
            },
            {
                "id": "do",
                "name": "Do",
                "activities": [
                    "BCP implementation",
                    "Procedures",
                    "Roles",
                    "Communication",
                ],
            },
            {
                "id": "check",
                "name": "Check",
                "activities": ["Exercise", "Testing", "Audit", "Management review"],
            },
            {
                "id": "act",
                "name": "Act",
                "activities": ["Corrective action", "Continual improvement"],
            },
        ],
    }


@app.post("/v1/iso22301/rto-adviseer")
def rto_adviseer(proces_impact: str, afnemers: int = 0):
    """Adviseer RTO op basis van proces-impact."""
    advies = {
        "kritiek": {
            "rto": 4,
            "rpo": 1,
            "strategie": "Hot standby + failover",
            "investering": "Hoog",
        },
        "aanzienlijk": {
            "rto": 8,
            "rpo": 4,
            "strategie": "Warm standby",
            "investering": "Gemiddeld",
        },
        "beperkt": {
            "rto": 24,
            "rpo": 8,
            "strategie": "Cold standby",
            "investering": "Laag",
        },
        "verwaarloosbaar": {
            "rto": 72,
            "rpo": 24,
            "strategie": "Manual recovery",
            "investering": "Minimaal",
        },
    }
    result = advies.get(proces_impact, advies["beperkt"])
    result["afnemers_betrokken"] = afnemers
    result["jaarlijkse_test_verplicht"] = proces_impact in ["kritiek", "aanzienlijk"]
    return result


@app.get("/v1/iso22301/bia-bcp-koppeling")
def bia_bcp_koppeling():
    """Toont de koppeling tussen BIA-BIV-DPIA en ISO 22301."""
    return {
        "bia_input_voor_bcms": [
            {
                "bia_output": "Kritieke processen lijst",
                "bcms_gebruik": "BIA scope + prioritering",
            },
            {"bia_output": "Impact classificatie", "bcms_gebruik": "RTO/RPO bepaling"},
            {"bia_output": "Afhankelijkheden", "bcms_gebruik": "BCP strategie"},
            {"bia_output": "Hersteltijden", "bcms_gebruik": "RTO validatie"},
        ],
        "bcms_extra_tov_bia": [
            {
                "bcms_element": "BCP documentatie",
                "meerwaarde": "Stappenplan bij uitval",
            },
            {"bcms_element": "Exercise programme", "meerwaarde": "Testen van plan"},
            {
                "bcms_element": "Communicatieprocedures",
                "meerwaarde": "Intern/extern bij incident",
            },
            {
                "bcms_element": "Rollen & verantwoordelijkheden",
                "meerwaarde": "Wie doet wat bij crisis",
            },
        ],
        "koppeling": "BIA = analyse fase (wat is kritiek?), BCP = response fase (wat doen we bij uitval?)",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8532)
