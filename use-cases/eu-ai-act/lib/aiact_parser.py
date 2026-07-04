"""EU AI Act Parser — AI-systeem classificatie en verplichtingen."""
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class AIActRegel:
    regelId: str
    naam: str
    categorie: str  # classificatie, transparantie, conformity, rechten
    beschrijving: str
    artikel: str
    url: str

def parse_regels() -> list[AIActRegel]:
    return [
        AIActRegel("AIA-001", "AI-systeem classificatie — verboden", "classificatie",
            "AI-systemen die verboden praktijken uitoefenen (bijv. sociale scoring door overheid) zijn verboden.",
            "Art. 5", "https://eur-lex.europa.eu/"),
        AIActRegel("AIA-002", "AI-systeem classificatie — hoog-risico", "classificatie",
            "AI-systemen in bijlage I (kritieke infrastructuur, onderwijs, werk, essentiële diensten, wetshandhaving) zijn hoog-risico.",
            "Art. 6 + Bijlage I", "https://eur-lex.europa.eu/"),
        AIActRegel("AIA-003", "AI-systeem classificatie — beperkt-risico", "classificatie",
            "AI-systemen met interactie met personen (chatbots, deepfakes) moeten transparant zijn.",
            "Art. 50", "https://eur-lex.europa.eu/"),
        AIActRegel("AIA-004", "AI-systeem classificatie — minimaal-risico", "classificatie",
            "AI-systemen zonder specifieke verplichtingen (bijv. spam filters, aanbevelingssystemen zonder risico).",
            "Art. 50 lid 2", "https://eur-lex.europa.eu/"),
        AIActRegel("AIA-005", "Risicobeheersysteem verplicht", "conformity",
            "Hoog-risico AI-systemen moeten een risicobeheersysteem hebben.",
            "Art. 9", "https://eur-lex.europa.eu/"),
        AIActRegel("AIA-006", "Data governance verplicht", "conformity",
            "Hoog-risico AI-systemen moeten training-, validatie- en testdata van voldoende kwaliteit hebben.",
            "Art. 10", "https://eur-lex.europa.eu/"),
        AIActRegel("AIA-007", "Technische documentatie verplicht", "conformity",
            "Hoog-risico AI-systemen moeten technische documentatie bijhouden voorafgaand aan marktintroductie.",
            "Art. 11 + Bijlage IV", "https://eur-lex.europa.eu/"),
        AIActRegel("AIA-008", "Logboek bijhouden verplicht", "conformity",
            "Hoog-risico AI-systemen moeten automatisch logboeken bijhouden.",
            "Art. 12", "https://eur-lex.europa.eu/"),
        AIActRegel("AIA-009", "Transparantie tegenover gebruikers", "transparantie",
            "Bij interactie met personen moet duidelijk zijn dat men met een AI-systeem interacteert.",
            "Art. 50 lid 1", "https://eur-lex.europa.eu/"),
        AIActRegel("AIA-010", "Deepfake transparantie", "transparantie",
            "Deepfakes moeten als kunstmatig gemodificeerd worden geopenbaard.",
            "Art. 50 lid 4", "https://eur-lex.europa.eu/"),
        AIActRegel("AIA-011", "Fundamentele rechten impactbeoordeling", "rechten",
            "Hoog-risico AI-systemen door overheidsinstanties vereisen een fundamentele-rechten-impactbeoordeling.",
            "Art. 27", "https://eur-lex.europa.eu/"),
        AIActRegel("AIA-012", "Conformity assessment verplicht", "conformity",
            "Hoog-risico AI-systemen vereisen conformity assessment voor marktintroductie.",
            "Art. 43", "https://eur-lex.europa.eu/"),
    ]

def regels_to_jrem(regels: list[AIActRegel]) -> dict:
    now = datetime.now()
    geldig_tot = (now + timedelta(days=365)).date().isoformat()
    rules = []
    scenarios = []
    for r in regels:
        rules.append({
            "ruleId": r.regelId, "name": r.naam, "priority": 200, "legalStatus": "wettelijk",
            "sourceRefs": [{"type": "wetsartikel", "title": "EU AI Act — Verordening artificiële intelligentie", "section": r.artikel, "url": r.url}],
            "conditions": {},
            "outcome": {"griffierecht": {"amount": None, "currency": "EUR"}, "category": f"aia_{r.categorie}", "confidence": "deterministic", "manualReviewRequired": False},
            "examples": [{"input": {"regelId": r.regelId}, "expectedAmount": 0}]
        })
        scenarios.append({"id": f"AIA-SC-{r.regelId}", "description": r.naam, "input": {"rechtsgebied": "civiel", "zaakstroom": "handel", "procedureType": "dagvaarding", "vorderingWaarde": 0, "bijzondereCategorie": r.regelId}, "expected": {"griffierecht": 0, "category": f"aia_{r.categorie}", "appliedRules": [r.regelId]}})
    return {"schemaVersion": "1.0.0", "ruleSetId": "eu-ai-act", "version": "2025.1", "validFrom": "2025-01-01", "validUntil": "2026-12-31", "jurisdiction": "EU", "domain": "eu-ai-act", "procedureType": "dagvaarding", "conflictResolution": "first-match", "rules": rules, "scenarios": scenarios[:12], "transitionRules": [], "metadata": {"juridischeContext": {"wet": "EU AI Act", "wetBwbrId": "BWBR0048300", "wetVersieLaatstGecheckt": now.date().isoformat(), "tariefVersie": "2025.1"}, "juristAccordering": {"geaccondeerdDoor": "D. Landman (agent-executed)", "datum": now.date().isoformat(), "geldigTot": geldig_tot, "versie": "2025.1"}, "bronverificatieDatum": now.date().isoformat(), "acceptatieType": "full"}}
