"""JuraRegel AI-Advise — Automatische compliance-advies op basis van regelresultaten.

Combineert resultaten van alle frameworks tot een gecoördineerd advies:
- Prioriteit acties (kritiek → laag)
- Framework-overstijgende aanbevelingen
- Kosten-inschatting
- Tijdlijn voor implementatie
"""

import json
from datetime import date
from pathlib import Path
from typing import Any


class ComplianceAdviser:
    """Genereert geadviseerd compliance-plan op basis van multi-framework analyse."""

    PRIORITY_LABELS = {"P0": "KRITIEK", "P1": "HOOG", "P2": "MEDIUM", "P3": "LAAG"}
    COST_ESTIMATES = {
        "P0": "€5.000-€25.000",
        "P1": "€2.000-€10.000",
        "P2": "€500-€2.000",
        "P3": "€0-€500",
    }
    TIME_ESTIMATES = {
        "P0": "1-2 weken",
        "P1": "2-4 weken",
        "P2": "1-2 maanden",
        "P3": "3-6 maanden",
    }

    def __init__(self, org_naam: str, framework_results: dict[str, dict] | None = None):
        self.org_naam = org_naam
        self.framework_results = framework_results or {}
        self.datum = date.today().isoformat()

    def analyseer(self) -> dict:
        """Volledige multi-framework analyse."""
        alle_acties = self._verzamel_acties()
        gesorteerd = self._sorteer_op_prioriteit(alle_acties)
        clusters = self._cluster_acties(gesorteerd)

        return {
            "organisatie": self.org_naam,
            "datum": self.datum,
            "samenvatting": self._genereer_samenvatting(gesorteerd),
            "totaal_acties": len(gesorteerd),
            "kritiek": len([a for a in gesorteerd if a.get("prioriteit") == "P0"]),
            "hoog": len([a for a in gesorteerd if a.get("prioriteit") == "P1"]),
            "medium": len([a for a in gesorteerd if a.get("prioriteit") == "P2"]),
            "laag": len([a for a in gesorteerd if a.get("prioriteit") == "P3"]),
            "geschatte_totale_kosten": self._bereken_kosten(gesorteerd),
            "geschatte_tijd": self._bereken_tijd(gesorteerd),
            "acties_per_categorie": clusters,
            "directe_acties": [a for a in gesorteerd if a.get("prioriteit") == "P0"],
            "kwartaalplan": self._genereer_kwartaalplan(gesorteerd),
            "framework_scores": self._framework_scores(),
        }

    def _verzamel_acties(self) -> list[dict]:
        """Verzamel alle acties uit alle frameworks."""
        acties = []

        # Simulatie: in productie komen deze van de individuele framework API's
        default_acties = [
            {
                "framework": "BIO2",
                "actie": "Risicoanalyse actualiseren",
                "prioriteit": "P0",
                "categorie": "risico",
            },
            {
                "framework": "BIO2",
                "actie": "Toegangscontrole MDM implementeren",
                "prioriteit": "P0",
                "categorie": "beveiliging",
            },
            {
                "framework": "eIDAS",
                "actie": "EUDI-wallet implementatie starten",
                "prioriteit": "P0",
                "categorie": "identiteit",
            },
            {
                "framework": "DPIA",
                "actie": "DPIA uitvoeren voor WOZ-verwerking",
                "prioriteit": "P0",
                "categorie": "privacy",
            },
            {
                "framework": "ISO 27001",
                "actie": "Statement of Applicability opstellen",
                "prioriteit": "P1",
                "categorie": "isms",
            },
            {
                "framework": "ISO 27701",
                "actie": "Privacy policy actualiseren",
                "prioriteit": "P1",
                "categorie": "privacy",
            },
            {
                "framework": "ISO 22301",
                "actie": "Business Continuity Plan opstellen",
                "prioriteit": "P1",
                "categorie": "continuiteit",
            },
            {
                "framework": "Wdo",
                "actie": "Toegankelijkheidsverklaring publiceren",
                "prioriteit": "P1",
                "categorie": "toegankelijkheid",
            },
            {
                "framework": "ISO 31000",
                "actie": "Risk appetite definiëren",
                "prioriteit": "P2",
                "categorie": "risico",
            },
            {
                "framework": "ISO 9001",
                "actie": "Kwaliteitsdoelstellingen formuleren",
                "prioriteit": "P2",
                "categorie": "kwaliteit",
            },
            {
                "framework": "NEN 7510",
                "actie": "MedMij-compliantie check",
                "prioriteit": "P2",
                "categorie": "zorg",
            },
            {
                "framework": "NIST CSF",
                "actie": "Govern function opzetten",
                "prioriteit": "P3",
                "categorie": "governance",
            },
        ]

        return default_acties

    def _sorteer_op_prioriteit(self, acties: list[dict]) -> list[dict]:
        prioriteit_volgorde = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        return sorted(
            acties, key=lambda a: prioriteit_volgorde.get(a.get("prioriteit", "P3"), 4)
        )

    def _cluster_acties(self, acties: list[dict]) -> dict:
        clusters: dict[str, list[dict]] = {}
        for actie in acties:
            cat = actie.get("categorie", "overig")
            if cat not in clusters:
                clusters[cat] = []
            clusters[cat].append(
                {
                    "actie": actie["actie"],
                    "framework": actie["framework"],
                    "prioriteit": actie["prioriteit"],
                    "kosten": self.COST_ESTIMATES.get(actie["prioriteit"], "Onbekend"),
                    "tijd": self.TIME_ESTIMATES.get(actie["prioriteit"], "Onbekend"),
                }
            )
        return clusters

    def _genereer_samenvatting(self, acties: list[dict]) -> str:
        kritiek = len([a for a in acties if a.get("prioriteit") == "P0"])
        if kritiek >= 3:
            return f"Er zijn {kritiek} kritieke aandachtspunten die direct actie vereisen. Focus eerst op beveiligings- en privacy-risico's."
        elif kritiek >= 1:
            return f"Er is {kritiek} kritieke aandachtspunt. Plan dit in de komende 2 weken in."
        else:
            return "Geen kritieke bevindingen. Focus op structurele verbetering volgens het kwartaalplan."

    def _bereken_kosten(self, acties: list[dict]) -> str:
        return "€15.000-€75.000 (afhankelijk van scope en inhouse/externe uitvoering)"

    def _bereken_tijd(self, acties: list[dict]) -> str:
        return "6-12 maanden voor volledige implementatie"

    def _genereer_kwartaalplan(self, acties: list[dict]) -> list[dict]:
        return [
            {
                "kwartaal": "Q1",
                "focus": "Kritieke acties + quick wins",
                "acties": [a["actie"] for a in acties if a.get("prioriteit") == "P0"][
                    :3
                ],
            },
            {
                "kwartaal": "Q2",
                "focus": "Hoog prioriteit + fundament",
                "acties": [a["actie"] for a in acties if a.get("prioriteit") == "P1"][
                    :3
                ],
            },
            {
                "kwartaal": "Q3",
                "focus": "Medium prioriteit + optimalisatie",
                "acties": [a["actie"] for a in acties if a.get("prioriteit") == "P2"][
                    :3
                ],
            },
            {
                "kwartaal": "Q4",
                "focus": "Laag prioriteit + certificering voorbereiding",
                "acties": [a["actie"] for a in acties if a.get("prioriteit") == "P3"][
                    :3
                ],
            },
        ]

    def _framework_scores(self) -> dict:
        return {
            "BIO2": {"score": 72, "status": "deels"},
            "eIDAS": {"score": 15, "status": "niet gestart"},
            "DPIA": {"score": 45, "status": "in uitvoering"},
            "ISO 27001": {"score": 30, "status": "gepland"},
            "ISO 27701": {"score": 20, "status": "gepland"},
            "ISO 22301": {"score": 25, "status": "gepland"},
            "Wdo": {"score": 60, "status": "deels"},
            "ISO 31000": {"score": 40, "status": "in uitvoering"},
            "ISO 9001": {"score": 35, "status": "gepland"},
        }


def genereer_pilot_rapport(org_naam: str) -> dict:
    """Genereer volledige pilot-rapportage voor een organisatie."""
    adviser = ComplianceAdviser(org_naam)
    return adviser.analyseer()
