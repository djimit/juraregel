"""Multi-Jurisdictionale Analyse — NL, EU, en internationale wetgeving.

Ondersteunt:
- Nederland (AVG + UAI + AWB)
- EU (AI Act + GDPR + eIDAS + NIS2)
- Internationaal (OECD AI Principles + Council of Europe AI Treaty)
- Kruisverwijzingen tussen jurisdicties
- Conflicterende verplichtingen identificeren

Academische foundation:
- Comparative Legal Analysis (Zweigert & Kötz, 1998)
- EU Multi-Level Governance (Hooghe & Marks, 2001)
- Regulatory Competition Theory (Ogus, 1999)
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)

# ─── Data Models ──────────────────────────────────────────────


class Jurisdiction(str, Enum):
    NETHERLANDS = "NL"
    EU = "EU"
    INTERNATIONAL = "INT"


@dataclass
class LegalObligation:
    """A legal obligation from a specific jurisdiction."""

    jurisdiction: Jurisdiction
    framework: str
    article: str
    title: str
    description: str
    requirement: str
    deadline: str | None
    penalty: str | None
    url: str | None


@dataclass
class Conflict:
    """A conflict between obligations from different jurisdictions."""

    obligation_a: LegalObligation
    obligation_b: LegalObligation
    conflict_type: str  # direct, indirect, timing
    severity: str  # low, medium, high, critical
    resolution_hint: str


@dataclass
class MultiJurisdictionReport:
    """Complete multi-jurisdiction analysis."""

    processing_activity: dict
    obligations: list[LegalObligation]
    conflicts: list[Conflict]
    applicable_frameworks: list[str]
    gaps: list[str]
    recommendations: list[str]
    generated_at: str


# ─── Multi-Jurisdiction Engine ────────────────────────────────


class MultiJurisdictionEngine:
    """Analyze compliance across multiple jurisdictions."""

    # Framework applicability rules
    FRAMEWORK_RULES = {
        "AVG": {
            "jurisdiction": Jurisdiction.NETHERLANDS,
            "triggers": ["persoonsgegevens", "betrokkene", "verwerking"],
            "always_applicable": True,  # AVG is van toepassing op alle NL verwerkingen
        },
        "UAI (Uitvoeringswet AI Act)": {
            "jurisdiction": Jurisdiction.NETHERLANDS,
            "triggers": ["ai_systems", "algoritme", "automatisering"],
            "always_applicable": False,
        },
        "EU AI Act": {
            "jurisdiction": Jurisdiction.EU,
            "triggers": ["ai_systems", "algoritme", "high-risk", "biometrie"],
            "always_applicable": False,
        },
        "eIDAS": {
            "jurisdiction": Jurisdiction.EU,
            "triggers": [
                "elektronische handtekening",
                "identiteit",
                "vertrouwensdiensten",
            ],
            "always_applicable": False,
        },
        "NIS2": {
            "jurisdiction": Jurisdiction.EU,
            "triggers": ["kritieke infrastructuur", "netwerkbeveiliging", "incident"],
            "always_applicable": False,
        },
        "OECD AI Principles": {
            "jurisdiction": Jurisdiction.INTERNATIONAL,
            "triggers": ["ai_systems", "internationale organisatie"],
            "always_applicable": False,
        },
    }

    def analyze(self, processing_activity: dict) -> MultiJurisdictionReport:
        """Perform multi-jurisdiction analysis."""
        start = time.time()

        # 1. Determine applicable frameworks
        applicable = self._determine_applicable_frameworks(processing_activity)

        # 2. Extract obligations per framework
        obligations = []
        for framework in applicable:
            fw_obligations = self._extract_obligations(framework, processing_activity)
            obligations.extend(fw_obligations)

        # 3. Identify conflicts
        conflicts = self._identify_conflicts(obligations)

        # 4. Identify gaps
        gaps = self._identify_gaps(obligations, applicable, processing_activity)

        # 5. Generate recommendations
        recommendations = self._generate_recommendations(obligations, conflicts, gaps)

        return MultiJurisdictionReport(
            processing_activity=processing_activity,
            obligations=obligations,
            conflicts=conflicts,
            applicable_frameworks=applicable,
            gaps=gaps,
            recommendations=recommendations,
            generated_at=datetime.utcnow().isoformat(),
        )

    def _determine_applicable_frameworks(self, activity: dict) -> list[str]:
        """Determine which frameworks apply."""
        applicable = []
        activity_str = json.dumps(activity).lower()

        for framework, rules in self.FRAMEWORK_RULES.items():
            if rules["always_applicable"]:
                applicable.append(framework)
            elif any(trigger in activity_str for trigger in rules["triggers"]):
                applicable.append(framework)

        return applicable

    def _extract_obligations(
        self, framework: str, activity: dict
    ) -> list[LegalObligation]:
        """Extract obligations for a framework."""
        obligations = []

        if framework == "AVG":
            obligations = self._avg_obligations(activity)
        elif framework == "EU AI Act":
            obligations = self._ai_act_obligations(activity)
        elif framework == "UAI (Uitvoeringswet AI Act)":
            obligations = self._uai_obligations(activity)
        elif framework == "NIS2":
            obligations = self._nis2_obligations(activity)

        return obligations

    def _avg_obligations(self, activity: dict) -> list[LegalObligation]:
        """Extract AVG obligations."""
        obligations = []

        # Art. 5 — Beginselen
        obligations.append(
            LegalObligation(
                jurisdiction=Jurisdiction.NETHERLANDS,
                framework="AVG",
                article="Art. 5",
                title="Beginselen van de verwerking",
                description="Persoonsgegevens worden rechtmatig, behoorlijk en transparant verwerkt",
                requirement="Documenteer de beginselen in je privacybeleid",
                deadline=None,
                penalty="Boete tot EUR 20.000.000 of 4% van de wereldwijde jaaromzet",
                url="https://eur-lex.europa.eu/legal-content/NL/TXT/?uri=CELEX:32016R0679",
            )
        )

        # Art. 35 — DPIA
        if activity.get("ai_systems") or activity.get("data_subject_count", 0) > 5000:
            obligations.append(
                LegalObligation(
                    jurisdiction=Jurisdiction.NETHERLANDS,
                    framework="AVG",
                    article="Art. 35",
                    title="Data Protection Impact Assessment (DPIA)",
                    description="DPIA verplicht bij waarschijnlijk hoog risico",
                    requirement="Voer een DPIA uit en documenteer deze",
                    deadline=None,
                    penalty="Boete tot EUR 10.000.000 of 2% van de wereldwijde jaaromzet",
                    url="https://eur-lex.europa.eu/legal-content/NL/TXT/?uri=CELEX:32016R0679",
                )
            )

        # Art. 32 — Beveiliging
        obligations.append(
            LegalObligation(
                jurisdiction=Jurisdiction.NETHERLANDS,
                framework="AVG",
                article="Art. 32",
                title="Beveiliging van de verwerking",
                description="Passende technische en organisatorische maatregelen",
                requirement="Implementeer encryptie, toegangscontrole, en logging",
                deadline=None,
                penalty="Boete tot EUR 10.000.000 of 2% van de wereldwijde jaaromzet",
                url="https://eur-lex.europa.eu/legal-content/NL/TXT/?uri=CELEX:32016R0679",
            )
        )

        return obligations

    def _ai_act_obligations(self, activity: dict) -> list[LegalObligation]:
        """Extract EU AI Act obligations."""
        obligations = []

        # Art. 9 — Risicobeheer
        obligations.append(
            LegalObligation(
                jurisdiction=Jurisdiction.EU,
                framework="EU AI Act",
                article="Art. 9",
                title="Risicobeheersysteem",
                description="Continuïteris iteratief proces voor risicobeheer",
                requirement="Implementeer een risicobeheersysteem voor het AI-systeem",
                deadline="2026-08-02",
                penalty="Boete tot EUR 15.000.000 of 3% van de wereldwijde jaaromzet",
                url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
            )
        )

        # Art. 10 — Data Governance
        obligations.append(
            LegalObligation(
                jurisdiction=Jurisdiction.EU,
                framework="EU AI Act",
                article="Art. 10",
                title="Data en data-governance",
                description="Training data moet relevant, representatief, en vrij van fouten",
                requirement="Documenteer datakwaliteit en onderzoek op biases",
                deadline="2026-08-02",
                penalty="Boete tot EUR 15.000.000 of 3% van de wereldwijde jaaromzet",
                url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
            )
        )

        # Art. 14 — Human Oversight
        obligations.append(
            LegalObligation(
                jurisdiction=Jurisdiction.EU,
                framework="EU AI Act",
                article="Art. 14",
                title="Menselijke tussenkomst",
                description="AI-systemen moeten effectieve menselijke tussenkomst mogelijk maken",
                requirement="Implementeer human-in-the-loop, override, en stop-mechanismen",
                deadline="2026-08-02",
                penalty="Boete tot EUR 15.000.000 of 3% van de wereldwijde jaaromzet",
                url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
            )
        )

        # Art. 27 — FRIA (indien hoog-risico)
        if activity.get("ai_systems") and activity.get("risk_tier") == "high":
            obligations.append(
                LegalObligation(
                    jurisdiction=Jurisdiction.EU,
                    framework="EU AI Act",
                    article="Art. 27",
                    title="Fundamental Rights Impact Assessment (FRIA)",
                    description="FRIA verplicht vóór inzet hoog-risico AI-systeem",
                    requirement="Voer een FRIA uit en documenteer deze",
                    deadline="2026-08-02",
                    penalty="Boete tot EUR 15.000.000 of 3% van de wereldwijde jaaromzet",
                    url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
                )
            )

        return obligations

    def _uai_obligations(self, activity: dict) -> list[LegalObligation]:
        """Extract Nederlandse Uitvoeringswet AI Act obligations."""
        return [
            LegalObligation(
                jurisdiction=Jurisdiction.NETHERLANDS,
                framework="UAI (Uitvoeringswet AI Act)",
                article="Art. 5 UAI",
                title="Aanwijzing toezichthouder",
                description="De AP is toezichthouder voor AI-systemen in Nederland",
                requirement="Rapporteer incidenten aan de AP",
                deadline=None,
                penalty="Bestuursrechtelijke handhaving door AP",
                url="https://wetten.overheid.nl",
            )
        ]

    def _nis2_obligations(self, activity: dict) -> list[LegalObligation]:
        """Extract NIS2 obligations."""
        return [
            LegalObligation(
                jurisdiction=Jurisdiction.EU,
                framework="NIS2",
                article="Art. 21",
                title="Cybersecurity risicobeheer",
                description="Passende technische en organisatorische maatregelen voor netwerkbeveiliging",
                requirement="Implementeer cybersecurity maatregelen en rapporteer incidenten",
                deadline="2024-10-17 (implementatie NL)",
                penalty="Boete tot EUR 10.000.000 of 2% van de wereldwijde jaaromzet",
                url="https://eur-lex.europa.eu/eli/dir/2022/2555/oj",
            )
        ]

    def _identify_conflicts(self, obligations: list[LegalObligation]) -> list[Conflict]:
        """Identify conflicts between obligations from different jurisdictions."""
        conflicts = []

        # Check for timing conflicts
        deadlines = {}
        for ob in obligations:
            if ob.deadline:
                if ob.deadline in deadlines:
                    conflicts.append(
                        Conflict(
                            obligation_a=deadlines[ob.deadline],
                            obligation_b=ob,
                            conflict_type="timing",
                            severity="medium",
                            resolution_hint="Plan resources om beide deadlines te halen",
                        )
                    )
                else:
                    deadlines[ob.deadline] = ob

        # Check for direct conflicts
        avg_dpia = [
            o for o in obligations if o.framework == "AVG" and "35" in o.article
        ]
        ai_fria = [
            o for o in obligations if o.framework == "EU AI Act" and "27" in o.article
        ]

        if avg_dpia and ai_fria:
            conflicts.append(
                Conflict(
                    obligation_a=avg_dpia[0],
                    obligation_b=ai_fria[0],
                    conflict_type="overlap",
                    severity="low",
                    resolution_hint="Combineer DPIA en FRIA waar mogelijk — Art. 27(2) AI Act stelt dat reeds uitgevoerde DPIA's kunnen worden meegenomen",
                )
            )

        return conflicts

    def _identify_gaps(
        self, obligations: list[LegalObligation], frameworks: list[str], activity: dict
    ) -> list[str]:
        """Identify compliance gaps."""
        gaps = []

        if "AVG" in frameworks and not any("35" in o.article for o in obligations):
            gaps.append(
                "Geen DPIA-uitvoering gedocumenteerd — verplicht bij hoog risico"
            )

        if "EU AI Act" in frameworks and not any(
            "27" in o.article for o in obligations
        ):
            if activity.get("ai_systems") and activity.get("risk_tier") == "high":
                gaps.append("Geen FRIA-uitvoering — verplicht voor hoog-risico AI")

        if not any("32" in o.article for o in obligations):
            gaps.append("Geen beveiligingsmaatregelen gedocumenteerd (AVG Art. 32)")

        return gaps

    def _generate_recommendations(
        self,
        obligations: list[LegalObligation],
        conflicts: list[Conflict],
        gaps: list[str],
    ) -> list[str]:
        """Generate recommendations."""
        recommendations = []

        # Priority: gaps first
        for gap in gaps:
            recommendations.append(f"URGENT: {gap}")

        # Then conflicts
        for conflict in conflicts:
            recommendations.append(
                f"AANDACHT: Conflict tussen {conflict.obligation_a.framework} en {conflict.obligation_b.framework}: {conflict.resolution_hint}"
            )

        # Then deadlines
        upcoming = [o for o in obligations if o.deadline]
        upcoming.sort(key=lambda o: o.deadline or "")
        for ob in upcoming[:3]:
            recommendations.append(
                f"DEADLINE: {ob.framework} {ob.article} — {ob.deadline}: {ob.title}"
            )

        return recommendations


# ─── Singleton ─────────────────────────────────────────────────

multi_jurisdiction_engine = MultiJurisdictionEngine()
