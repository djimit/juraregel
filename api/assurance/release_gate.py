"""Release Gate — automated go/no-go decision based on severity distribution.

Implements Stanford's principle: release decision must be based on
severity distribution, NOT on average accuracy.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .error_taxonomy import (
    LegalError,
    Severity,
)
from .severity_scorer import UseCaseProfile, score_system


@dataclass
class ReleaseDecision:
    """Release gate verdict."""

    verdict: str  # "GO", "NO-GO", "CONDITIONAL"
    reason: str
    details: dict[str, Any]

    @property
    def approved(self) -> bool:
        return self.verdict == "GO"


def evaluate_release(
    errors: list[LegalError],
    use_case: UseCaseProfile,
    min_detectability: float = 0.8,
    min_recoverability: float = 0.7,
) -> ReleaseDecision:
    """Evaluate whether a system is ready for release.

    Three outcomes:
    - GO: acceptable ratio, no blocking errors
    - CONDITIONAL: acceptable ratio but with warnings
    - NO-GO: blocking errors or unacceptable ratio
    """
    result = score_system(
        errors,
        use_case,
        detectability=min_detectability,
        recoverability=min_recoverability,
    )

    if result.distribution.has_blocking_errors:
        blocking = result.distribution.counts[Severity.S4_RECHTSVERLIES]
        blocking += result.distribution.counts[Severity.S5_SYSTEEMISCH]
        return ReleaseDecision(
            verdict="NO-GO",
            reason=f"{blocking} blocking error(s) (S4/S5) detected",
            details=result.to_dict(),
        )

    if not result.acceptable:
        return ReleaseDecision(
            verdict="NO-GO",
            reason=f"Acceptability ratio {result.ratio:.2f} below threshold",
            details=result.to_dict(),
        )

    # Check for warnings (S3 errors present)
    s3_count = result.distribution.counts[Severity.S3_MATERIEEL]
    if s3_count > 0:
        return ReleaseDecision(
            verdict="CONDITIONAL",
            reason=f"Acceptable but {s3_count} S3 (material) errors require review",
            details=result.to_dict(),
        )

    return ReleaseDecision(
        verdict="GO",
        reason="All severity levels within acceptable bounds",
        details=result.to_dict(),
    )
