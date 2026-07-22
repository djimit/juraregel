"""Temporal Decay — invalidate outdated benchmark results.

Implements Stanford's principle of temporal decay: legislation, case law,
models, prompts, retrieval indices, and vendor configurations change continuously.
A benchmark result is version-bound and can become outdated quickly.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_MAX_AGE_DAYS = int(os.getenv("BENCHMARK_MAX_AGE_DAYS", "90"))


@dataclass
class BenchmarkResult:
    """A benchmark result with temporal metadata."""

    result_id: str
    timestamp: str
    score: float
    model_version: str
    prompt_version: str
    index_version: str
    legal_sources_hash: str  # hash of the legal sources used
    max_age_days: int = DEFAULT_MAX_AGE_DAYS

    @property
    def age_days(self) -> float:
        """Age of this result in days."""
        try:
            result_time = datetime.fromisoformat(self.timestamp)
            delta = datetime.now() - result_time
            return delta.total_seconds() / 86400
        except (ValueError, TypeError):
            return float("inf")

    @property
    def is_expired(self) -> bool:
        """Check if this result has expired."""
        return self.age_days > self.max_age_days

    @property
    def expiry_date(self) -> str:
        """Get the expiry date."""
        try:
            result_time = datetime.fromisoformat(self.timestamp)
            expiry = result_time + timedelta(days=self.max_age_days)
            return expiry.isoformat()
        except (ValueError, TypeError):
            return "unknown"

    @property
    def freshness(self) -> float:
        """Freshness score: 1.0 = fresh, 0.0 = expired."""
        if self.is_expired:
            return 0.0
        return max(0.0, 1.0 - (self.age_days / self.max_age_days))


@dataclass
class DecayReport:
    """Report on temporal decay of benchmark results."""

    timestamp: str
    total_results: int
    fresh: int
    expired: int
    expiring_soon: int  # expires within 14 days
    results: list[dict[str, Any]]

    @property
    def freshness_ratio(self) -> float:
        """Ratio of fresh results."""
        return self.fresh / max(self.total_results, 1)


class TemporalDecay:
    """Manages temporal decay of benchmark results."""

    def __init__(self, max_age_days: int = DEFAULT_MAX_AGE_DAYS):
        self.max_age_days = max_age_days
        self._results: list[BenchmarkResult] = []

    def add_result(self, result: BenchmarkResult) -> None:
        """Register a benchmark result for decay tracking."""
        self._results.append(result)

    def check_decay(self) -> DecayReport:
        """Check temporal decay of all tracked results."""
        fresh = 0
        expired = 0
        expiring_soon = 0
        details = []

        for result in self._results:
            is_expired = result.is_expired
            age = result.age_days
            expires_in = result.max_age_days - age

            if is_expired:
                expired += 1
            else:
                fresh += 1
                if expires_in <= 14:
                    expiring_soon += 1

            details.append(
                {
                    "result_id": result.result_id,
                    "score": result.score,
                    "age_days": round(age, 1),
                    "is_expired": is_expired,
                    "freshness": round(result.freshness, 2),
                    "expiry_date": result.expiry_date,
                }
            )

        return DecayReport(
            timestamp=datetime.now().isoformat(),
            total_results=len(self._results),
            fresh=fresh,
            expired=expired,
            expiring_soon=expiring_soon,
            results=details,
        )

    def get_expired(self) -> list[BenchmarkResult]:
        """Get all expired results."""
        return [r for r in self._results if r.is_expired]

    def get_fresh(self) -> list[BenchmarkResult]:
        """Get all fresh results."""
        return [r for r in self._results if not r.is_expired]


# ─── Singleton ─────────────────────────────────────────────────

temporal_decay = TemporalDecay()
