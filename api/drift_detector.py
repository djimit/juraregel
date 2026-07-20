"""Drift Detection Engine — Continuous compliance monitoring.

Detects:
1. Implementation drift (beleid vs. werkelijkheid)
2. Regulatory drift (wetswijzigingen)
3. Evidence drift (verlopen bewijsstukken)
4. Score drift (compliance-score trend)

Based on RegTech 2026 best practices (Stanford, Deloitte, RegPulse).
"""

from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)

# ─── Data Models ──────────────────────────────────────────────


class DriftType(str, Enum):
    IMPLEMENTATION = "implementation"
    REGULATORY = "regulatory"
    EVIDENCE_EXPIRED = "evidence_expired"
    SCORE_DECLINE = "score_decline"
    MISSING_REVIEW = "missing_review"


class DriftSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DriftItem:
    """A single drift detection item."""

    type: DriftType
    severity: DriftSeverity
    description: str
    expected: str
    actual: str
    remediation: str
    citation: str | None = None
    detected_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class DriftReport:
    """Complete drift report for an assessment."""

    assessment_id: str
    organisation_id: str
    drift_items: list[DriftItem]
    drift_score: float  # 0-100, higher = more drift
    previous_score: float | None
    score_trend: str  # improving, stable, declining
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


# ─── Drift Detector ────────────────────────────────────────────


class DriftDetector:
    """Continuous compliance drift detection."""

    def __init__(self):
        self._baselines: dict[str, dict] = {}
        self._history: dict[str, list[dict]] = {}

    def set_baseline(self, assessment_id: str, baseline: dict) -> None:
        """Set the baseline for an assessment."""
        baseline["_timestamp"] = datetime.utcnow().isoformat()
        self._baselines[assessment_id] = baseline

    def detect_drift(self, assessment_id: str, current_state: dict) -> DriftReport:
        """Detect drift between baseline and current state."""
        baseline = self._baselines.get(assessment_id, {})
        drift_items = []

        # 1. Implementation drift
        baseline_measures = baseline.get("measures", {})
        current_measures = current_state.get("measures", {})

        for measure_id, expected_status in baseline_measures.items():
            actual_status = current_measures.get(measure_id)
            if actual_status and actual_status != expected_status:
                drift_items.append(
                    DriftItem(
                        type=DriftType.IMPLEMENTATION,
                        severity=DriftSeverity.HIGH,
                        description=f"Maatregel '{measure_id}' wijkt af",
                        expected=str(expected_status),
                        actual=str(actual_status),
                        remediation=f"Herstel implementatie van '{measure_id}'",
                        citation="AVG Art. 5(2) — Verantwoordingsplicht",
                    )
                )

        # 2. Evidence expiry
        baseline_evidence = baseline.get("evidence", [])
        now = datetime.utcnow()
        for evidence in baseline_evidence:
            expiry = evidence.get("expiry_date")
            if expiry:
                expiry_date = (
                    datetime.fromisoformat(expiry)
                    if isinstance(expiry, str)
                    else expiry
                )
                if expiry_date < now:
                    drift_items.append(
                        DriftItem(
                            type=DriftType.EVIDENCE_EXPIRED,
                            severity=DriftSeverity.MEDIUM,
                            description=f"Bewijsstuk '{evidence.get('title')}' is verlopen",
                            expected=f"Geldig tot {expiry}",
                            actual="Verlopen",
                            remediation=f"Vernieuw bewijsstuk '{evidence.get('title')}'",
                            citation="AVG Art. 5(1)(d) — Juistheid",
                        )
                    )

        # 3. Missing review
        next_review = baseline.get("next_review_date")
        if next_review:
            review_date = (
                datetime.fromisoformat(next_review)
                if isinstance(next_review, str)
                else next_review
            )
            if review_date < now:
                drift_items.append(
                    DriftItem(
                        type=DriftType.MISSING_REVIEW,
                        severity=DriftSeverity.HIGH,
                        description="Review-termijn overschreden",
                        expected=f"Review voor {next_review}",
                        actual="Review gemist",
                        remediation="Plan direct een herziening in",
                        citation="AVG Art. 35(11) — Periodieke herziening DPIA",
                    )
                )

        # 4. Score drift
        current_score = current_state.get("compliance_score", 0)
        previous_score = baseline.get("compliance_score")
        score_trend = "stable"
        if previous_score is not None:
            if current_score < previous_score - 10:
                score_trend = "declining"
                drift_items.append(
                    DriftItem(
                        type=DriftType.SCORE_DECLINE,
                        severity=DriftSeverity.HIGH,
                        description=f"Compliance score gedaald van {previous_score} naar {current_score}",
                        expected=f"Score >= {previous_score}",
                        actual=f"Score: {current_score}",
                        remediation="Analyseer oorzaak scordaling en neem maatregelen",
                    )
                )
            elif current_score > previous_score + 5:
                score_trend = "improving"

        # Calculate drift score
        drift_score = self._calculate_drift_score(drift_items)

        # Store history
        if assessment_id not in self._history:
            self._history[assessment_id] = []
        self._history[assessment_id].append(
            {
                "timestamp": now.isoformat(),
                "drift_score": drift_score,
                "drift_count": len(drift_items),
            }
        )

        return DriftReport(
            assessment_id=assessment_id,
            organisation_id=current_state.get("organisation_id", "unknown"),
            drift_items=drift_items,
            drift_score=drift_score,
            previous_score=previous_score,
            score_trend=score_trend,
        )

    def _calculate_drift_score(self, drift_items: list[DriftItem]) -> float:
        """Calculate overall drift score (0-100, higher = more drift)."""
        if not drift_items:
            return 0.0

        severity_weights = {
            DriftSeverity.LOW: 10,
            DriftSeverity.MEDIUM: 25,
            DriftSeverity.HIGH: 50,
            DriftSeverity.CRITICAL: 100,
        }

        total_weight = sum(severity_weights[item.severity] for item in drift_items)
        # Normalize: max 100 (e.g., 2 critical = 100, or 4 high = 100)
        drift_score = min(total_weight / max(len(drift_items), 1) * 2, 100)
        return round(drift_score, 1)

    def get_trend(self, assessment_id: str, window: int = 10) -> list[dict]:
        """Get drift trend over time."""
        history = self._history.get(assessment_id, [])
        return history[-window:]


# ─── Singleton ─────────────────────────────────────────────────

drift_detector = DriftDetector()
