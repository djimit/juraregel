"""Dashboard Data API — expose assurance metrics for UI consumption.

Provides aggregated data for visualizing:
- Severity distribution
- Benchmark scores over time
- Drift trends
- Gate verdicts
- Compliance task status
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class DashboardData:
    """Complete dashboard dataset."""

    timestamp: str
    overall_score: float
    severity_distribution: dict[str, int]
    benchmark_scores: dict[str, float]
    drift_status: str
    gate_verdicts: dict[str, str]
    compliance_tasks: list[dict[str, Any]]
    recent_alerts: list[dict[str, Any]]
    metrics: dict[str, Any]


class DashboardAPI:
    """Generates dashboard data from assurance modules."""

    def get_dashboard_data(self) -> DashboardData:
        """Collect all assurance metrics for dashboard display."""
        from .error_taxonomy import Severity, SeverityDistribution
        from .regression_set import regression_set
        from .challenge_set import challenge_set
        from .drift_monitor import drift_monitor
        from .release_gate import evaluate_release
        from .severity_scorer import UseCaseProfile
        from .djimitflo_bridge import djimitflo_bridge

        # Run benchmarks
        reg = regression_set.run()
        chal = challenge_set.run()
        drift = drift_monitor.check({"regression": reg.score, "challenge": chal.score})

        # Severity distribution (example from current state)
        dist = SeverityDistribution()

        # Gate verdicts for each autonomy level
        gate_verdicts = {}
        for level in range(1, 6):
            uc = UseCaseProfile(f"l{level}-test", level, "civiel", "advocaat")
            decision = evaluate_release([], uc)
            gate_verdicts[f"L{level}"] = decision.verdict

        # Compliance tasks
        tasks = djimitflo_bridge.get_tasks()
        task_dicts = [
            {
                "title": t.title,
                "priority": t.priority,
                "control_id": t.control_id,
                "approvers": t.approvers,
            }
            for t in tasks
        ]

        # Drift alerts
        alerts = [
            {
                "metric": a.metric,
                "delta": a.delta,
                "severity": a.severity,
            }
            for a in drift.alerts
        ]

        # Overall score = average of benchmark scores
        overall = (reg.score + chal.score) / 2

        return DashboardData(
            timestamp=datetime.now().isoformat(),
            overall_score=round(overall, 2),
            severity_distribution={s.value: dist.counts[s] for s in Severity},
            benchmark_scores={
                "regression": reg.score,
                "challenge": chal.score,
            },
            drift_status="drift" if drift.has_drift else "stable",
            gate_verdicts=gate_verdicts,
            compliance_tasks=task_dicts,
            recent_alerts=alerts,
            metrics={
                "regression_passed": reg.passed,
                "regression_total": reg.total_cases,
                "challenge_passed": chal.passed,
                "challenge_total": chal.total_cases,
                "canary_safe": not chal.canary_triggered,
                "drift_alerts": len(alerts),
                "compliance_tasks": len(task_dicts),
            },
        )

    def to_json(self) -> str:
        """Serialize dashboard data to JSON."""
        data = self.get_dashboard_data()
        return json.dumps(
            {
                "timestamp": data.timestamp,
                "overall_score": data.overall_score,
                "severity_distribution": data.severity_distribution,
                "benchmark_scores": data.benchmark_scores,
                "drift_status": data.drift_status,
                "gate_verdicts": data.gate_verdicts,
                "compliance_tasks": data.compliance_tasks,
                "recent_alerts": data.recent_alerts,
                "metrics": data.metrics,
            },
            indent=2,
        )


# ─── Singleton ─────────────────────────────────────────────────

dashboard_api = DashboardAPI()
