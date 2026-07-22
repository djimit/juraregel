"""Drift Monitor — detect performance degradation between benchmark runs.

Implements NIST AI RMF MEASURE 1.1 continuous monitoring:
tracks accuracy/robustness metrics over time and alerts on drift.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DRIFT_THRESHOLD = 0.05  # 5% score drop triggers alert
DRIFT_STORE_PATH = os.getenv("DRIFT_STORE_PATH", ".swarm/evidence/drift-history.jsonl")


@dataclass
class DriftAlert:
    """A drift detection alert."""

    timestamp: str
    metric: str
    previous_score: float
    current_score: float
    delta: float
    threshold: float
    severity: str  # "warning", "critical"

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "metric": self.metric,
            "previous_score": self.previous_score,
            "current_score": self.current_score,
            "delta": self.delta,
            "threshold": self.threshold,
            "severity": self.severity,
        }


@dataclass
class DriftReport:
    """Complete drift analysis report."""

    run_id: str
    timestamp: str
    alerts: list[DriftAlert]
    metrics: dict[str, float]
    previous_metrics: dict[str, float]
    has_drift: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "alerts": [a.to_dict() for a in self.alerts],
            "metrics": self.metrics,
            "previous_metrics": self.previous_metrics,
            "has_drift": self.has_drift,
        }


class DriftMonitor:
    """Monitors benchmark performance drift over time."""

    def __init__(self, threshold: float = DRIFT_THRESHOLD):
        self.threshold = threshold
        self._history: list[dict[str, Any]] = []
        self._load_history()

    def _load_history(self) -> None:
        """Load drift history from disk."""
        path = Path(DRIFT_STORE_PATH)
        if path.exists():
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        self._history.append(json.loads(line))

    def _save_snapshot(self, metrics: dict[str, float]) -> None:
        """Save a metrics snapshot to history."""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
        }
        self._history.append(snapshot)

        path = Path(DRIFT_STORE_PATH)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a") as f:
            f.write(json.dumps(snapshot) + "\n")

    def check(self, current_metrics: dict[str, float]) -> DriftReport:
        """Check for drift between current and previous metrics."""
        previous = self._get_previous_metrics()
        alerts = []

        if previous:
            for metric, current_score in current_metrics.items():
                prev_score = previous.get(metric)
                if prev_score is not None:
                    delta = prev_score - current_score
                    if delta > self.threshold:
                        alerts.append(
                            DriftAlert(
                                timestamp=datetime.now().isoformat(),
                                metric=metric,
                                previous_score=prev_score,
                                current_score=current_score,
                                delta=delta,
                                threshold=self.threshold,
                                severity="critical" if delta > 0.10 else "warning",
                            )
                        )

        report = DriftReport(
            run_id=f"drift-{hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]}",
            timestamp=datetime.now().isoformat(),
            alerts=alerts,
            metrics=current_metrics,
            previous_metrics=previous or {},
            has_drift=len(alerts) > 0,
        )

        self._save_snapshot(current_metrics)
        return report

    def _get_previous_metrics(self) -> dict[str, float] | None:
        """Get the most recent metrics snapshot."""
        if self._history:
            return self._history[-1].get("metrics")
        return None

    def get_history(self, limit: int = 50) -> list[dict[str, Any]]:
        """Get drift history."""
        return self._history[-limit:]


# ─── Singleton ─────────────────────────────────────────────────

drift_monitor = DriftMonitor()
