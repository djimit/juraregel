"""ISO 31000 API — Risk Management Framework."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("iso31000", JREM_DIR, 8533)


@app.get("/v1/iso31000/framework")
def framework():
    """Toont het ISO 31000 risicomanagement framework."""
    return {
        "standard": "ISO 31000:2018",
        "name": "Risk Management — Guidelines",
        "principles": [
            "Integrated",
            "Structured and comprehensive",
            "Customized",
            "Inclusive",
            "Dynamic",
            "Best available information",
            "Human and cultural factors",
            "Continual improvement",
        ],
        "process": [
            {"step": 1, "name": "Scope, context, criteria"},
            {"step": 2, "name": "Risk identification"},
            {"step": 3, "name": "Risk analysis"},
            {"step": 4, "name": "Risk evaluation"},
            {"step": 5, "name": "Risk treatment"},
            {"step": 6, "name": "Monitoring and review"},
            {"step": 7, "name": "Recording and reporting"},
        ],
    }


@app.post("/v1/iso31000/risk-score")
def risk_score(impact: int, likelihood: int):
    """Bereken risico-score volgens ISO 31000."""
    score = impact * likelihood
    if score >= 20:
        level = "Extreem"
        treatment = "Vermijden of zware maatregelen"
        color = "red"
    elif score >= 12:
        level = "Hoog"
        treatment = "Verminderen met maatregelen"
        color = "orange"
    elif score >= 6:
        level = "Middel"
        treatment = "Beheersen en monitoren"
        color = "yellow"
    elif score >= 1:
        level = "Laag"
        treatment = "Accepteren en monitoren"
        color = "green"
    else:
        level = "Verwaarloosbaar"
        treatment = "Geen actie"
        color = "gray"

    return {
        "impact": impact,
        "likelihood": likelihood,
        "score": score,
        "max_score": 25,
        "level": level,
        "treatment": treatment,
        "color": color,
    }


@app.get("/v1/iso31000/framework-koppeling")
def framework_koppeling():
    """Toont hoe ISO 31000 gekoppeld is aan andere JuraRegel frameworks."""
    return {
        "description": "ISO 31000 is de fundamentele risicomanagement-norm waar andere frameworks op bouwen",
        "koppelingen": [
            {
                "framework": "ISO 27001:2022",
                "koppeling": "Risicoanalyse (6.1.2) + risicobehandeling (6.1.3) zijn direct gebaseerd op ISO 31000",
                "overlap": "Hoog",
            },
            {
                "framework": "ISO 22301:2018",
                "koppeling": "BIA risico-identificatie gebruikt ISO 31000 proces",
                "overlap": "Hoog",
            },
            {
                "framework": "ISO 27701:2019",
                "koppeling": "Privacy risico-analyse volgt ISO 31000 proces",
                "overlap": "Gemiddeld",
            },
            {
                "framework": "BIA-BIV-DPIA",
                "koppeling": "Impact × waarschijnlijkheid = ISO 31000 risk matrix",
                "overlap": "Direct",
            },
            {
                "framework": "NIS2",
                "koppeling": "Risicomaatregelen Art. 21 gebaseerd op ISO 31000",
                "overlap": "Hoog",
            },
            {
                "framework": "BIO2",
                "koppeling": "Risicoanalyse A.5-6 volgt ISO 31000 principes",
                "overlap": "Hoog",
            },
            {
                "framework": "EU AI Act",
                "koppeling": "Risicoclassificatie (Art. 6) gebruikt ISO 31000 principes",
                "overlap": "Gemiddeld",
            },
        ],
    }


@app.get("/v1/iso31000/treatment-options")
def treatment_options():
    """Geef de 4 risico-behandelingsopties volgens ISO 31000."""
    return {
        "options": [
            {
                "id": "avoid",
                "name": "Vermijden",
                "description": "Stop met de activiteit die het risico veroorzaakt",
                "when": "Score ≥ 20, onaanvaardbaar",
            },
            {
                "id": "mitigate",
                "name": "Verminderen",
                "description": "Maatregelen nemen om impact of waarschijnlijkheid te verlagen",
                "when": "Score 12-19, beheersbaar met maatregelen",
            },
            {
                "id": "transfer",
                "name": "Overdragen",
                "description": "Risico delen met derden (verzekering, uitbesteding)",
                "when": "Financieel risico, niet-kritiek",
            },
            {
                "id": "accept",
                "name": "Accepteren",
                "description": "Risico accepteren met management-goedkeuring",
                "when": "Score ≤ 6, acceptabel niveau",
            },
        ],
        "note": "Combinatie van opties is mogelijk. Residuaal risico moet worden geaccepteerd.",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8533)
