"""Formalized Severity Model — wiskundige onderbouwing van het JLAIF severity-model.

Gebaseerd op:
- Expected Utility Theory (von Neumann & Morgenstern, 1944)
- Value of Statistical Life (VSL) voor juridische risico's
- Prospect Theory (Kahneman & Tversky, 1979) voor asymmetrische risico-perceptie

Het model formaliseert waarom één S5-fout zwaarder weegt dan vele S1-fouten:
de utility-functie van juridische correctie is niet-lineair maar exponentieel.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


@dataclass
class FormalSeverity:
    """Geformaliseerd severity niveau met wiskundige onderbouwing."""

    level: str
    weight: float
    utility_loss: float  # Verlies in utiliteit (0-1)
    recovery_cost: float  # Relatieve herstelkosten (0-1)
    legal_consequence: str
    prospect_theory_factor: float  # λ-factor uit prospect theory


# Prospect theory: λ = 2.25 (gemiddelde uit experimenten)
# Mensen wegen verlies 2.25x zwaarder dan gelijkwaardige winst
PROSPECT_LOSS_AVERSION = 2.25

# Base voor exponentiële weging
# U(w) = 1 - e^(-αw) waar α de risico-aversiecoëfficiënt is
EXP_BASE = 2.0

FORMAL_SEVERITIES = {
    "S1": FormalSeverity(
        level="S1",
        weight=1.0,
        utility_loss=0.01,
        recovery_cost=0.01,
        legal_consequence="Geen extern gevolg",
        prospect_theory_factor=1.0,
    ),
    "S2": FormalSeverity(
        level="S2",
        weight=2.0,
        utility_loss=0.05,
        recovery_cost=0.05,
        legal_consequence="Intern herstelbaar zonder extern gevolg",
        prospect_theory_factor=1.5,
    ),
    "S3": FormalSeverity(
        level="S3",
        weight=4.0,
        utility_loss=0.15,
        recovery_cost=0.15,
        legal_consequence="Materiële inhoudelijke fout, correctie vereist",
        prospect_theory_factor=2.0,
    ),
    "S4": FormalSeverity(
        level="S4",
        weight=8.0,
        utility_loss=0.40,
        recovery_cost=0.35,
        legal_consequence="Potentieel rechtsverlies of grondrechtenimpact",
        prospect_theory_factor=PROSPECT_LOSS_AVERSION,
    ),
    "S5": FormalSeverity(
        level="S5",
        weight=16.0,
        utility_loss=0.85,
        recovery_cost=0.70,
        legal_consequence="Ernstige of systemische schade, niet volledig herstelbaar",
        prospect_theory_factor=PROSPECT_LOSS_AVERSION * 1.5,
    ),
}


class FormalSeverityModel:
    """Geformaliseerd severity-model met wiskundige onderbouwing."""

    def __init__(self, risk_aversion: float = 1.0):
        self.risk_aversion = risk_aversion

    def utility(self, weight: float) -> float:
        """Bereken utility-verlies: U(w) = 1 - e^(-αw)"""
        return 1.0 - math.exp(-self.risk_aversion * weight / 10.0)

    def combined_weight(self, severities: list[str]) -> float:
        """
        Combineer meerdere severity levels.

        Gebaseerd op: U_combined = 1 - ∏(1 - U_i)
        Dit modelleert dat meerdere fouten multiplicatief zijn, niet additief.
        """
        if not severities:
            return 0.0

        utilities = []
        for sev in severities:
            if sev in FORMAL_SEVERITIES:
                utilities.append(self.utility(FORMAL_SEVERITIES[sev].weight))

        # Probabilistic union: P(A∪B) = 1 - (1-P(A))(1-P(B))
        combined = 1.0
        for u in utilities:
            combined *= 1.0 - u

        return 1.0 - combined

    def prospect_adjusted_weight(self, severity: str) -> float:
        """
        Prospect-theorie-aangepaste weging.

        Verlies wordt λ keer zwaarder gewonnen dan gelijkwaardige winst.
        """
        if severity not in FORMAL_SEVERITIES:
            return 1.0

        sev = FORMAL_SEVERITIES[severity]
        return sev.weight * sev.prospect_theory_factor

    def expected_utility_loss(
        self, severities: list[str], probabilities: list[float]
    ) -> float:
        """
        Verwacht utility-verlies: E[U] = Σ p_i * U(w_i)

        Args:
            severities: Lijst van severity levels
            probabilities: Bijbehorende waarschijnlijkheden
        """
        if len(severities) != len(probabilities):
            raise ValueError("Severities en probabilities moeten zelfde lengte hebben")

        expected = 0.0
        for sev, prob in zip(severities, probabilities):
            if sev in FORMAL_SEVERITIES:
                expected += prob * self.utility(FORMAL_SEVERITIES[sev].weight)

        return expected

    def compare_systems(
        self, system_a: list[str], system_b: list[str]
    ) -> dict[str, Any]:
        """
        Vergelijk twee systemen op basis van hun severity distributie.

        Returns:
            Dict met gewogen scores, utility vergelijking, en aanbeveling
        """
        weight_a = self.combined_weight(system_a)
        weight_b = self.combined_weight(system_b)

        return {
            "system_a": {
                "severities": system_a,
                "combined_weight": round(weight_a, 3),
                "utility_loss": round(self.utility(weight_a), 3),
            },
            "system_b": {
                "severities": system_b,
                "combined_weight": round(weight_b, 3),
                "utility_loss": round(self.utility(weight_b), 3),
            },
            "preferred": "A" if weight_a < weight_b else "B",
            "difference": round(abs(weight_a - weight_b), 3),
        }

    def explain_weighting(self, severity: str) -> dict[str, Any]:
        """Leg uit waarop een severity weging is gebaseerd."""
        if severity not in FORMAL_SEVERITIES:
            return {"error": f"Onbekend severity level: {severity}"}

        sev = FORMAL_SEVERITIES[severity]
        return {
            "level": sev.level,
            "base_weight": sev.weight,
            "utility_loss": sev.utility_loss,
            "recovery_cost": sev.recovery_cost,
            "legal_consequence": sev.legal_consequence,
            "prospect_theory_factor": sev.prospect_theory_factor,
            "prospect_adjusted_weight": self.prospect_adjusted_weight(severity),
            "formal_utility": round(self.utility(sev.weight), 4),
            "explanation": (
                f"Severity {sev.level} heeft een base weight van {sev.weight}, "
                f"gecorrigeerd met prospect-theorie factor {sev.prospect_theory_factor} "
                f"(λ={PROSPECT_LOSS_AVERSION}). Het utility-loss is {sev.utility_loss:.0%} "
                f"met relatieve herstelkosten van {sev.recovery_cost:.0%}."
            ),
        }


# ─── Singleton ─────────────────────────────────────────────────

formal_severity_model = FormalSeverityModel()
