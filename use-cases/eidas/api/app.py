"""
eIDAS 2.0 Rule API — European Digital Identity Framework

Provides compliance checking for:
- eIDAS 1.0: Vertrouwensdiensten (handtekening, zegel, tijdsstempel, ERD, website-auth)
- eIDAS 2.0: EUDI-wallet, QAA, Electronic Archival, attributenuitwisseling
- Grensoverschrijdende erkenning en wallet-interoperabiliteit
- TSP-kwalificatie, trust lists, kwaliteitskeurmerken
- PID-provider (RvIG), certificering (RDI), DPIA

Usage:
  python3 use-cases/eidas/api/app.py
  → http://127.0.0.1:8523/v1/health
"""

import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from api_base import create_app

JREM_PATH = Path(__file__).parent.parent / "jrem/exports/eidas-2026.2.json"

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("eidas", JREM_DIR, 8523)


# ─── Custom eIDAS Endpoints ──────────────────────────────────


@app.get("/v1/eidas/wallet-status")
def wallet_status():
    """EUDI-wallet implementatie status met deadline countdown."""
    today = date.today()
    deadline = date(2026, 12, 1)
    days_remaining = (deadline - today).days

    return {
        "framework": "eIDAS 2.0",
        "component": "EUDI-wallet",
        "deadline": "2026-12-01",
        "days_remaining": days_remaining,
        "status": "critical"
        if days_remaining < 180
        else "warning"
        if days_remaining < 365
        else "planning",
        "nl_readiness": {
            "wallet_available": False,
            "expected_date": "2027-Q1",
            "pid_provider": "RvIG (Rijksdienst voor Identiteitsgegevens)",
            "certification_authority": "RDI (Rijksinspectie Digitale Infrastructuur)",
            "risk": "HIGH — NL wallet verwacht na EU deadline",
        },
        "requirements": [
            {
                "id": "EID-008",
                "description": "Wallet in productie",
                "deadline": "2026-12-01",
            },
            {
                "id": "EID-012",
                "description": "Sole control door gebruiker",
                "deadline": "2026-12-01",
            },
            {
                "id": "EID-013",
                "description": "PID minimum dataset",
                "deadline": "2026-12-01",
            },
            {
                "id": "EID-017",
                "description": "Grensoverschrijdende interoperabiliteit",
                "deadline": "2026-12-01",
            },
            {
                "id": "EID-029",
                "description": "Security levels (LoA laag/substantieel/hoog)",
                "deadline": "2026-12-01",
            },
            {
                "id": "EID-030",
                "description": "Conformiteitsbeoordeling",
                "deadline": "2026-12-01",
            },
        ],
    }


@app.get("/v1/eidas/deadlines")
def deadlines():
    """Overzicht alle eIDAS deadlines met urgentie."""
    today = date.today()
    deadlines_list = [
        {
            "date": "2024-09-29",
            "status": "passed",
            "urgency": "info",
            "rules": ["EID-016", "EID-021", "EID-025"],
            "description": "Grensoverschrijdende erkenning handtekeningen + niet-discriminatie",
        },
        {
            "date": "2026-01-01",
            "status": "pending" if date(2026, 1, 1) >= today else "overdue",
            "urgency": "warning",
            "rules": [
                "EID-001",
                "EID-002",
                "EID-003",
                "EID-004",
                "EID-005",
                "EID-019",
                "EID-020",
            ],
            "description": "Vertrouwensdiensten (handtekening, zegel, tijdsstempel, ERD, website-auth)",
        },
        {
            "date": "2026-12-01",
            "status": "pending",
            "urgency": "critical"
            if (date(2026, 12, 1) - today).days < 365
            else "warning",
            "rules": [
                "EID-006",
                "EID-007",
                "EID-008",
                "EID-009",
                "EID-010",
                "EID-011",
                "EID-012",
                "EID-013",
                "EID-014",
                "EID-015",
                "EID-017",
                "EID-018",
                "EID-022",
                "EID-023",
                "EID-024",
                "EID-026",
                "EID-029",
                "EID-030",
                "EID-031",
                "EID-032",
            ],
            "description": "EUDI-wallet + nieuwe vertrouwensdiensten + attributen",
        },
        {
            "date": "2027-12-01",
            "status": "future",
            "urgency": "info",
            "rules": ["EID-027", "EID-028"],
            "description": "Wallet kwaliteitskeurmerk + private sector acceptatie",
        },
    ]
    return {"deadlines": deadlines_list, "total_rules": 32, "today": today.isoformat()}


@app.get("/v1/eidas/rapport/{org_id}")
def rapport(org_id: str):
    """Genereert een eIDAS compliance rapport voor een organisatie."""
    import json

    with open(JREM_PATH) as f:
        jrem = json.load(f)

    compliant = sum(1 for r in jrem["rules"] if r["outcome"]["compliant"])
    non_compliant = sum(1 for r in jrem["rules"] if not r["outcome"]["compliant"])
    total = len(jrem["rules"])

    return {
        "organisatie": org_id,
        "framework": "eIDAS 2.0 (EU 2024/1183)",
        "ruleset_version": jrem["version"],
        "generated_at": datetime.now().isoformat(),
        "samenvatting": {
            "totaal_regels": total,
            "compliant": compliant,
            "niet_compliant": non_compliant,
            "compliance_percentage": round((compliant / total) * 100, 1),
        },
        "categorieen": {
            "vertrouwensdiensten": {"regels": 7, "status": "eIDAS 1.0 + 2.0"},
            "wallet": {"regels": 7, "status": "eIDAS 2.0 — deadline 2026-12-01"},
            "crossborder": {"regels": 3, "status": "Interoperabiliteit"},
            "tsp": {"regels": 2, "status": "Kwalificatie"},
            "attributen": {"regels": 3, "status": "Wallet attributen"},
            "trustlists": {"regels": 2, "status": "EUTL"},
            "keurmerken": {"regels": 2, "status": "Kwaliteit"},
            "overig": {"regels": 6, "status": "Privacy, security, implementing"},
        },
        "acties": [
            {
                "prioriteit": "CRITICAL",
                "regel": "EID-011",
                "actie": "Start wallet implementatie",
            },
            {
                "prioriteit": "HIGH",
                "regel": "EID-008",
                "actie": "Wallet productie vóór deadline",
            },
            {
                "prioriteit": "HIGH",
                "regel": "EID-017",
                "actie": "Grensoverschrijdende interoperabiliteit",
            },
            {
                "prioriteit": "MEDIUM",
                "regel": "EID-006",
                "actie": "QAA als nieuwe vertrouwensdienst",
            },
            {
                "prioriteit": "MEDIUM",
                "regel": "EID-007",
                "actie": "Electronic Archival implementatie",
            },
        ],
    }


@app.get("/v1/eidas/categorieen")
def categorieen():
    """Lijst alle eIDAS compliance categorieën met regels."""
    import json

    with open(JREM_PATH) as f:
        jrem = json.load(f)

    cats = {}
    for rule in jrem["rules"]:
        cat = rule["outcome"]["category"]
        if cat not in cats:
            cats[cat] = []
        cats[cat].append(
            {
                "ruleId": rule["ruleId"],
                "name": rule["name"],
                "compliant": rule["outcome"]["compliant"],
                "deadline": rule["outcome"]["deadline"],
            }
        )

    return {"categorieen": cats, "totaal": len(cats)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8523)
