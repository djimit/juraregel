"""Legal AI Error Taxonomy — 9 fouttypes + S1-S5 severity model.

Based on Stanford PNAS "No Free Benchmark" (2025/2026) requirement that
legal AI must classify errors by type AND by legal consequence severity.

Error types cover the full RAG-to-decision chain:
  Source → Retrieval → Interpretation → Application → Decision

Severity uses asymmetric weighting: one S5 error outweighs many S1 errors.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class LegalErrorType(str, Enum):
    """Nine error types spanning the full legal AI failure surface.

    Aligned with Stanford's requirement that legal AI must distinguish
    error types rather than collapsing into a single accuracy metric.
    """

    FACTUAL = "fout"
    SOURCE = "bronfout"
    INTERPRETATION = "interpretatiefout"
    JURISDICTION = "jurisdictiefout"
    TEMPORAL = "temporaliteitsfout"
    PROCEDURAL = "procedurefout"
    OMISSION = "omissiefout"
    BIAS = "bias_ongelijke_behandeling"
    CONFIDENTIALITY = "vertrouwelijkheidsincident"

    @property
    def default_severity(self) -> "Severity":
        """Default severity for each error type — can be overridden per instance."""
        mapping = {
            LegalErrorType.FACTUAL: Severity.S3_MATERIEEL,
            LegalErrorType.SOURCE: Severity.S3_MATERIEEL,
            LegalErrorType.INTERPRETATION: Severity.S3_MATERIEEL,
            LegalErrorType.JURISDICTION: Severity.S4_RECHTSVERLIES,
            LegalErrorType.TEMPORAL: Severity.S4_RECHTSVERLIES,
            LegalErrorType.PROCEDURAL: Severity.S4_RECHTSVERLIES,
            LegalErrorType.OMISSION: Severity.S3_MATERIEEL,
            LegalErrorType.BIAS: Severity.S5_SYSTEEMISCH,
            LegalErrorType.CONFIDENTIALITY: Severity.S5_SYSTEEMISCH,
        }
        return mapping[self]


class Severity(str, Enum):
    """S1-S5 severity scale — asymmetric impact weighting.

    Key principle: a system with many S1 errors may be more acceptable
    than a system with one recurring S5 error.
    """

    S1_COSMETISCH = "S1"
    S2_HERSTELBAAR = "S2"
    S3_MATERIEEL = "S3"
    S4_RECHTSVERLIES = "S4"
    S5_SYSTEEMISCH = "S5"

    @property
    def weight(self) -> float:
        """Exponential weighting — S5 is 16x S1, not 5x."""
        weights = {
            "S1": 1.0,
            "S2": 2.0,
            "S3": 4.0,
            "S4": 8.0,
            "S5": 16.0,
        }
        return weights[self.value]

    @property
    def blocks_release(self) -> bool:
        """S4 and S5 block release by default."""
        return self in (Severity.S4_RECHTSVERLIES, Severity.S5_SYSTEEMISCH)


@dataclass
class LegalError:
    """A classified legal AI error with full context."""

    error_type: LegalErrorType
    severity: Severity
    description: str
    source_claim: str = ""
    expected_answer: str = ""
    actual_answer: str = ""
    jurisdiction: str = ""
    legal_domain: str = ""
    recoverable: bool = True
    detectable: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def risk_score(self) -> float:
        """Stanford's acceptance formula component: severity × (1 - detectability)."""
        detectability = 1.0 if self.detectable else 0.2
        return self.severity.weight * (1.0 - detectability)


@dataclass
class SeverityDistribution:
    """Distribution of errors across severity levels — used for release decisions."""

    counts: dict[Severity, int] = field(
        default_factory=lambda: {s: 0 for s in Severity}
    )

    def add(self, error: LegalError) -> None:
        self.counts[error.severity] += 1

    @property
    def weighted_score(self) -> float:
        """Lower is better. S5 errors dominate."""
        return sum(s.weight * count for s, count in self.counts.items())

    @property
    def has_blocking_errors(self) -> bool:
        return any(
            self.counts[s] > 0
            for s in (Severity.S4_RECHTSVERLIES, Severity.S5_SYSTEEMISCH)
        )

    @property
    def total_errors(self) -> int:
        return sum(self.counts.values())

    @property
    def non_blocking_ratio(self) -> float:
        """Ratio of non-blocking error weight to total weight.

        Returns 1.0 = all errors are S1-S3, 0.0 = all errors are S4-S5.
        For the full Stanford acceptance formula, use severity_scorer.score_system().
        """
        if self.total_errors == 0:
            return 1.0

        blocking_weight = sum(
            s.weight * self.counts[s]
            for s in (Severity.S4_RECHTSVERLIES, Severity.S5_SYSTEEMISCH)
        )
        total_weight = self.weighted_score

        if total_weight == 0:
            return 1.0

        return (total_weight - blocking_weight) / total_weight

    def to_dict(self) -> dict[str, Any]:
        return {
            "counts": {s.value: c for s, c in self.counts.items()},
            "weighted_score": self.weighted_score,
            "has_blocking_errors": self.has_blocking_errors,
            "total_errors": self.total_errors,
            "non_blocking_ratio": self.non_blocking_ratio,
        }
