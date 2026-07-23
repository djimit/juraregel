"""Cross-Jurisdictie Analyse — vergelijkende recht-analyse over landen.

Ondersteunt:
- Nederland (NL) — BW, AVG, Awb, Sr, Sv
- Europese Unie (EU) — AI Act, GDPR, richtlijnen
- Internationaal (INT) — OECD, Council of Europe
- Verenigd Koninkrijk (UK) — UK GDPR, UK AI Strategy
- Verenigde Staten (US) — State AI laws, sectoral regulation
- Duitsland (DE) — BDSG, KI-V
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class JurisdictionProfile:
    """Profiel van een rechtsgebied."""

    code: str
    name: str
    legal_system: str  # civil_law, common_law, mixed
    frameworks: list[str]
    key_principles: list[str]
    penalties: dict[str, str]  # framework → max penalty
    ai_specific: bool


JURISDICTION_PROFILES = {
    "NL": JurisdictionProfile(
        code="NL",
        name="Nederland",
        legal_system="civil_law",
        frameworks=["AVG", "UAI", "BW", "Awb", "Sr", "Sv", "Wbp"],
        key_principles=[
            "Rechtmatigheid",
            "Doelbinding",
            "Minimalisatie",
            "Juistheid",
            "Bewaartermijn",
            "Integriteit",
            "Vertrouwelijkheid",
        ],
        penalties={"AVG": "EUR 20M of 4% omzet", "AI Act": "EUR 35M of 7% omzet"},
        ai_specific=True,
    ),
    "EU": JurisdictionProfile(
        code="EU",
        name="Europese Unie",
        legal_system="civil_law",
        frameworks=["EU AI Act", "GDPR", "eIDAS", "NIS2", "Digital Markets Act"],
        key_principles=[
            "Fundamental rights",
            "Non-discrimination",
            "Transparency",
            "Accountability",
            "Human oversight",
            "Safety",
        ],
        penalties={"GDPR": "EUR 20M of 4% omzet", "AI Act": "EUR 35M or 7% omzet"},
        ai_specific=True,
    ),
    "INT": JurisdictionProfile(
        code="INT",
        name="Internationaal",
        legal_system="mixed",
        frameworks=[
            "OECD AI Principles",
            "Council of Europe AI Treaty",
            "ECHR",
            "UNESCO AI Ethics",
        ],
        key_principles=[
            "Human rights",
            "Democracy",
            "Rule of law",
            "Inclusive growth",
            "Human-centered values",
            "Transparency",
            "Robustness",
            "Accountability",
        ],
        penalties={"ECHR": "EHRM vonnis", "OECD": "Geen bindende sanctie"},
        ai_specific=True,
    ),
    "UK": JurisdictionProfile(
        code="UK",
        name="Verenigd Koninkrijk",
        legal_system="common_law",
        frameworks=[
            "UK GDPR",
            "Data Protection Act 2018",
            "UK AI Strategy",
            "Online Safety Act",
        ],
        key_principles=[
            "Lawfulness",
            "Fairness",
            "Transparency",
            "Purpose limitation",
            "Data minimisation",
            "Accuracy",
            "Storage limitation",
            "Security",
        ],
        penalties={"UK GDPR": "GBP 17.5M of 4% omzet"},
        ai_specific=False,
    ),
    "US": JurisdictionProfile(
        code="US",
        name="Verenigde Staten",
        legal_system="common_law",
        frameworks=[
            "State AI Laws",
            "Sectoral AI Regulation",
            "FTC Act",
            "Executive Order 14110",
        ],
        key_principles=[
            "Sectoral regulation",
            "State-level patchwork",
            "First Amendment",
            "Due process",
            "Equal protection",
            "FTC enforcement",
        ],
        penalties={"FTC": "Civil penalties per violation", "State laws": "Varies"},
        ai_specific=False,
    ),
    "DE": JurisdictionProfile(
        code="DE",
        name="Duitsland",
        legal_system="civil_law",
        frameworks=["BDSG", "KI-V", "GDPR", "UrhG", "GG"],
        key_principles=[
            "Informationselle Selbstbestimmung",
            "Verhältnismäßigkeit",
            "Rechtmäßigkeit",
            "Zweckbindung",
            "Datensparsamkeit",
            "Richtigkeit",
        ],
        penalties={"GDPR": "EUR 20M or 4% omzet", "KI-V": "EUR 35M or 7% omzet"},
        ai_specific=True,
    ),
}


@dataclass
class CrossJurisdictionComparison:
    """Vergelijking tussen rechtsgebieden."""

    feature: str
    nl_support: bool
    eu_support: bool
    int_support: bool
    uk_support: bool
    us_support: bool
    de_support: bool
    notes: str


class CrossJurisdictionAnalyzer:
    """Analyseert verschillen tussen rechtsgebieden."""

    def compare_frameworks(self) -> list[dict[str, Any]]:
        """Vergelijk frameworks tussen rechtsgebieden."""
        comparisons = []

        all_frameworks = set()
        for profile in JURISDICTION_PROFILES.values():
            all_frameworks.update(profile.frameworks)

        for framework in sorted(all_frameworks):
            supported = []
            for code, profile in JURISDICTION_PROFILES.items():
                if framework in profile.frameworks:
                    supported.append(code)

            comparisons.append(
                {
                    "framework": framework,
                    "supported_by": supported,
                    "coverage": len(supported) / len(JURISDICTION_PROFILES),
                }
            )

        return comparisons

    def compare_penalties(self) -> list[dict[str, Any]]:
        """Vergelijk boetesancties tussen rechtsgebieden."""
        penalty_data = []
        for code, profile in JURISDICTION_PROFILES.items():
            for framework, penalty in profile.penalties.items():
                penalty_data.append(
                    {
                        "jurisdiction": code,
                        "framework": framework,
                        "max_penalty": penalty,
                    }
                )
        return penalty_data

    def find_gaps(self) -> list[dict[str, Any]]:
        """Videntificeer gaps in rechtsgebied-dekking."""
        gaps = []

        for code, profile in JURISDICTION_PROFILES.items():
            if not profile.ai_specific:
                gaps.append(
                    {
                        "jurisdiction": code,
                        "gap": "Geen AI-specifieke wetgeving",
                        "impact": "medium",
                        "recommendation": f"Monitor AI-regulering in {profile.name}",
                    }
                )

            if profile.legal_system == "common_law":
                gaps.append(
                    {
                        "jurisdiction": code,
                        "gap": "Common law — jurispridentie is belangrijker dan code",
                        "impact": "high",
                        "recommendation": "Voeg precedent-analyse toe voor common law jurisdicties",
                    }
                )

        return gaps

    def get_jurisdiction(self, code: str) -> JurisdictionProfile | None:
        """Haal een rechtsgebied profiel op."""
        return JURISDICTION_PROFILES.get(code)

    def compare_two(self, code_a: str, code_b: str) -> dict[str, Any]:
        """Vergelijk twee rechtsgebieden."""
        a = JURISDICTION_PROFILES.get(code_a)
        b = JURISDICTION_PROFILES.get(code_b)

        if not a or not b:
            return {"error": "Onbekend rechtsgebied"}

        shared = set(a.frameworks) & set(b.frameworks)
        only_a = set(a.frameworks) - set(b.frameworks)
        only_b = set(b.frameworks) - set(a.frameworks)

        return {
            "jurisdiction_a": a.name,
            "jurisdiction_b": b.name,
            "shared_frameworks": list(shared),
            "only_in_a": list(only_a),
            "only_in_b": list(only_b),
            "legal_system_a": a.legal_system,
            "legal_system_b": b.legal_system,
            "ai_specific_a": a.ai_specific,
            "ai_specific_b": b.ai_specific,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "jurisdictions": list(JURISDICTION_PROFILES.keys()),
            "profiles": {
                code: {
                    "name": p.name,
                    "legal_system": p.legal_system,
                    "frameworks": p.frameworks,
                    "ai_specific": p.ai_specific,
                }
                for code, p in JURISDICTION_PROFILES.items()
            },
        }


# ─── Singleton ─────────────────────────────────────────────────

cross_jurisdiction = CrossJurisdictionAnalyzer()
