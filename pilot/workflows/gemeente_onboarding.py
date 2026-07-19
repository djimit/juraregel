"""JuraRegel Pilot Onboarding Flow — Gemeente Compliance Quickscan.

Stap-voor-stap workflow:
  1. Organisatie registreren (JuraRegel Cloud)
  2. BIA — Business Impact Analyse (kritische processen identificeren)
  3. BIV — Beschikbaarheid/Integriteit/Vertrouwelijkheid classificatie
  4. Risico-analyse (impact × waarschijnlijkheid)
  5. DPIA — Data Protection Impact Assessment (indien verplicht)
  6. Actieplan + compliance score
  7. Rapport generatie

Elke stap produceert een artefact dat wordt opgeslagen bij de organisatie.
"""

import json
import sys
from datetime import date
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "cloud" / "lib"))
from organisations import get_store, Organisation


class GemeenteOnboarding:
    """Begeleidt een gemeente door de compliance-pilot."""

    STAPPEN = [
        {
            "id": "registreer",
            "naam": "Organisatie Registratie",
            "beschrijving": "Maak JuraRegel Cloud account aan",
        },
        {
            "id": "bia",
            "naam": "Business Impact Analyse",
            "beschrijving": "Identificeer kritische processen en hersteltijden",
        },
        {
            "id": "biv",
            "naam": "BIV Classificatie",
            "beschrijving": "Classificeer beschikbaarheid, integriteit, vertrouwelijkheid",
        },
        {
            "id": "risico",
            "naam": "Risico-Analyse",
            "beschrijving": "Bereken risico's (impact × waarschijnlijkheid)",
        },
        {
            "id": "dpia_check",
            "naam": "DPIA Verplichting Check",
            "beschrijving": "Bepaal of DPIA verplicht is",
        },
        {
            "id": "dpia",
            "naam": "DPIA Uitvoering",
            "beschrijving": "Voer DPIA uit (indien verplicht)",
        },
        {
            "id": "actieplan",
            "naam": "Actieplan",
            "beschrijving": "Genereer prioriteit acties",
        },
        {
            "id": "rapport",
            "naam": "Eindrapport",
            "beschrijving": "Genereer compliance rapport",
        },
    ]

    def __init__(self, org_id: str, store_path: Path | None = None):
        from organisations import OrganisationStore

        store = OrganisationStore(store_path) if store_path else get_store()
        self.org = store.get(org_id)
        if not self.org:
            raise ValueError(f"Organisatie {org_id} niet gevonden")
        self.resultaten = {}

    def stap(self, stap_id: str) -> dict:
        """Geeft details van een stap."""
        for s in self.STAPPEN:
            if s["id"] == stap_id:
                return s
        return {}

    def voer_uit(self, stap_id: str, data: dict | None = None) -> dict:
        """Voert een stap uit en slaat resultaat op."""
        handlers = {
            "registreer": self._stap_registreer,
            "bia": self._stap_bia,
            "biv": self._stap_biv,
            "risico": self._stap_risico,
            "dpia_check": self._stap_dpia_check,
            "actieplan": self._stap_actieplan,
            "rapport": self._stap_rapport,
        }
        handler = handlers.get(stap_id)
        if not handler:
            return {"error": f"Onbekende stap: {stap_id}"}
        resultaat = handler(data or {})
        self.resultaten[stap_id] = resultaat
        return resultaat

    def _stap_registreer(self, data: dict) -> dict:
        return {
            "stap": "registreer",
            "status": "complete",
            "organisatie": self.org.name,
            "plan": self.org.plan,
            "volgende_stap": "bia",
        }

    def _stap_bia(self, data: dict) -> dict:
        """Business Impact Analyse."""
        processen = data.get("processen", [])
        if not processen:
            # Standaard gemeentelijke processen
            processen = [
                {"naam": "Belastingheffing", "impact": "kritiek", "hersteltijd": 4},
                {
                    "naam": "Vergunningverlening",
                    "impact": "aanzienlijk",
                    "hersteltijd": 8,
                },
                {"naam": "Paspoort/ID-kaart", "impact": "kritiek", "hersteltijd": 2},
                {
                    "naam": "WOZ-beschikkingen",
                    "impact": "aanzienlijk",
                    "hersteltijd": 24,
                },
                {"naam": "Sociale dienst", "impact": "kritiek", "hersteltijd": 4},
                {"naam": "Gemeenteblad", "impact": "beperkt", "hersteltijd": 48},
            ]

        geanalyseerd = []
        for proc in processen:
            if isinstance(proc, dict):
                geanalyseerd.append(proc)
            elif isinstance(proc, str):
                geanalyseerd.append(
                    {"naam": proc, "impact": "onbekend", "hersteltijd": 24}
                )

        kritiek = [
            p for p in geanalyseerd if p.get("impact") in ["kritiek", "catastrofaal"]
        ]

        return {
            "stap": "bia",
            "status": "complete",
            "processen_totaal": len(geanalyseerd),
            "kritieke_processen": len(kritiek),
            "details": geanalyseerd,
            "volgende_stap": "biv",
        }

    def _stap_biv(self, data: dict) -> dict:
        """BIV Classificatie."""
        systemen = data.get("systemen", [])
        if not systemen:
            systemen = [
                {
                    "naam": "BRP-koppeling",
                    "beschikbaarheid": "zeer_hoog",
                    "integriteit": "zeer_hoog",
                    "vertrouwelijkheid": "zeer_hoog",
                },
                {
                    "naam": "WOZ-systeem",
                    "beschikbaarheid": "hoog",
                    "integriteit": "zeer_hoog",
                    "vertrouwelijkheid": "hoog",
                },
                {
                    "naam": "Vergunningensysteem",
                    "beschikbaarheid": "hoog",
                    "integriteit": "hoog",
                    "vertrouwelijkheid": "middel",
                },
                {
                    "naam": "Website",
                    "beschikbaarheid": "hoog",
                    "integriteit": "middel",
                    "vertrouwelijkheid": "laag",
                },
            ]

        for systeem in systemen:
            biv_score = self._bereken_biv_score(systeem)
            systeem["biv_score"] = biv_score

        return {
            "stap": "biv",
            "status": "complete",
            "systemen_totaal": len(systemen),
            "details": systemen,
            "volgende_stap": "risico",
        }

    def _bereken_biv_score(self, systeem: dict) -> int:
        """Bereken BIV score (3-9 schaal)."""
        scores = {"laag": 1, "middel": 2, "hoog": 3, "zeer_hoog": 4}
        b = scores.get(systeem.get("beschikbaarheid", "laag"), 1)
        i = scores.get(systeem.get("integriteit", "laag"), 1)
        v = scores.get(systeem.get("vertrouwelijkheid", "laag"), 1)
        return b + i + v

    def _stap_risico(self, data: dict) -> dict:
        """Risico-analyse."""
        risico_items = data.get("risicos", [])
        if not risico_items:
            risico_items = [
                {
                    "beschrijving": "Datalek BRP-gegevens",
                    "impact": 4,
                    "waarschijnlijkheid": 2,
                },
                {"beschrijving": "Ransomware", "impact": 4, "waarschijnlijkheid": 3},
                {
                    "beschrijving": "Uval WOZ-systeem",
                    "impact": 3,
                    "waarschijnlijkheid": 2,
                },
                {
                    "beschrijving": "Onbevoegde toegang",
                    "impact": 3,
                    "waarschijnlijkheid": 2,
                },
            ]

        for item in risico_items:
            item["risico_score"] = item["impact"] * item["waarschijnlijkheid"]
            if item["risico_score"] >= 15:
                item["strategie"] = "vermijden"
                item["prioriteit"] = "P0"
            elif item["risico_score"] >= 5:
                item["strategie"] = "verminderen"
                item["prioriteit"] = "P1"
            else:
                item["strategie"] = "accepteeren"
                item["prioriteit"] = "P2"

        gesorteerd = sorted(risico_items, key=lambda x: x["risico_score"], reverse=True)

        return {
            "stap": "risico",
            "status": "complete",
            "risicos_totaal": len(gesorteerd),
            "kritiek": len([r for r in gesorteerd if r["prioriteit"] == "P0"]),
            "hoog": len([r for r in gesorteerd if r["prioriteit"] == "P1"]),
            "details": gesorteerd,
            "volgende_stap": "dpia_check",
        }

    def _stap_dpia_check(self, data: dict) -> dict:
        """Check of DPIA verplicht is."""
        verwerkte_gegevens = data.get("gegevens_soorten", ["persoonsgegevens"])
        dpia_verplicht = any(
            g in ["bijzondere_categorie", "persoonsgeevoelige", "grootschalig"]
            for g in verwerkte_gegevens
        )

        return {
            "stap": "dpia_check",
            "status": "complete",
            "dpia_verplicht": dpia_verplicht,
            "redenen": [
                "Bijzondere categorie gegevens (gezondheid, economische situatie)",
                "Grootschalige verwerking (alle inwoners)",
            ]
            if dpia_verplicht
            else [],
            "volgende_stap": "actieplan",
        }

    def _stap_actieplan(self, data: dict) -> dict:
        """Genereer actieplan uit voorgaande stappen."""
        acties = []

        # Uit BIA
        bia = self.resultaten.get("bia", {})
        if bia.get("kritieke_processen", 0) > 0:
            acties.append(
                {
                    "bron": "BIA",
                    "actie": f"Continuïteitsplan voor {bia['kritieke_processen']} kritieke processen",
                    "prioriteit": "P1",
                }
            )

        # Uit risico
        risico = self.resultaten.get("risico", {})
        for item in risico.get("details", []):
            if item["prioriteit"] in ["P0", "P1"]:
                acties.append(
                    {
                        "bron": "Risico",
                        "actie": f"{item['beschrijving']}: {item['strategie']} (score: {item['risico_score']})",
                        "prioriteit": item["prioriteit"],
                    }
                )

        # Uit DPIA
        dpia = self.resultaten.get("dpia_check", {})
        if dpia.get("dpia_verplicht"):
            acties.append(
                {
                    "bron": "DPIA",
                    "actie": "Voer DPIA uit voor alle verwerkingen met hoog risico",
                    "prioriteit": "P0",
                }
            )

        return {
            "stap": "actieplan",
            "status": "complete",
            "acties_totaal": len(acties),
            "acties": sorted(acties, key=lambda x: x["prioriteit"]),
            "volgende_stap": "rapport",
        }

    def _stap_rapport(self, data: dict) -> dict:
        """Genereer eindrapport."""
        actieplan = self.resultaten.get("actieplan", {})
        risico = self.resultaten.get("risico", {})
        bia = self.resultaten.get("bia", {})

        # Bereken compliance score
        totaal_acties = actieplan.get("acties_totaal", 0)
        kritieke_acties = len(
            [a for a in actieplan.get("acties", []) if a["prioriteit"] == "P0"]
        )
        score = max(0, 100 - (kritieke_acties * 15) - (totaal_acties * 2))

        return {
            "stap": "rapport",
            "status": "complete",
            "organisatie": self.org.name,
            "datum": date.today().isoformat(),
            "compliance_score": score,
            "samenvatting": {
                "processen_geanalyseerd": bia.get("processen_totaal", 0),
                "kritieke_processen": bia.get("kritieke_processen", 0),
                "risicos_geidentificeerd": risico.get("risicos_totaal", 0),
                "acties_gegenereerd": totaal_acties,
            },
            "voltooide_stappen": list(self.resultaten.keys()),
        }

    def voer_alles_uit(self) -> dict:
        """Voert alle stappen achter elkaar uit."""
        for stap in self.STAPPEN:
            if stap["id"] == "registreer":
                continue  # Al gedaan bij init
            if stap["id"] == "dpia":
                # Alleen als DPIA verplicht
                dpia_check = self.resultaten.get("dpia_check", {})
                if not dpia_check.get("dpia_verplicht"):
                    continue
            self.voer_uit(stap["id"])
        return self.resultaten


def start_pilot(org_id: str) -> GemeenteOnboarding:
    """Start een nieuwe pilot voor een organisatie."""
    return GemeenteOnboarding(org_id)
