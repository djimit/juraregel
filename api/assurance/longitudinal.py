"""Longitudinale Evaluatie — tijdreeks-analyse van audit-resultaten.

Gebaseerd op:
- Interrupted Time Series Design (Campbell & Stanley, 1963)
- Statistical Process Control (Shewhart, 1931)
- Trendanalyse met moving averages

Meet:
- Audit scores over tijd
- Drift detectie (regressie in kwaliteit)
- Verbeteringsslope na interventie
- Voorspelling toekomstige kwaliteit
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class AuditSnapshot:
    """Een momentopname van audit-resultaten."""

    timestamp: str
    product_name: str
    total_findings: int
    severity_distribution: dict[str, int]
    release_decision: str
    score: float  # 0-100 (hoger = beter)


@dataclass
class TrendAnalysis:
    """Trendanalyse over meerdere audit-snapshots."""

    product_name: str
    snapshots_count: int
    trend: str  # improving, stable, declining
    slope: float  # Positief = verbetering
    current_score: float
    predicted_next_score: float
    recommendation: str


class LongitudinalEvaluation:
    """Longitudinale evaluatie van audit-resultaten."""

    def __init__(self):
        self._snapshots: list[AuditSnapshot] = []

    def add_snapshot(self, snapshot: AuditSnapshot) -> None:
        """Voeg een audit-snapshot toe."""
        self._snapshots.append(snapshot)

    def get_snapshots(self, product_name: str | None = None) -> list[AuditSnapshot]:
        """Haal snapshots op, optioneel gefilterd op product."""
        if product_name:
            return [s for s in self._snapshots if s.product_name == product_name]
        return self._snapshots

    def analyze_trend(self, product_name: str) -> TrendAnalysis:
        """Analyseer de trend voor een product."""
        snapshots = self.get_snapshots(product_name)

        if len(snapshots) < 2:
            return TrendAnalysis(
                product_name=product_name,
                snapshots_count=len(snapshots),
                trend="insufficient_data",
                slope=0.0,
                current_score=snapshots[-1].score if snapshots else 0.0,
                predicted_next_score=snapshots[-1].score if snapshots else 0.0,
                recommendation="Minimaal 2 snapshots nodig voor trendanalyse",
            )

        # Calculate simple linear regression
        n = len(snapshots)
        x_values = list(range(n))
        y_values = [s.score for s in snapshots]

        x_mean = sum(x_values) / n
        y_mean = sum(y_values) / n

        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values))
        denominator = sum((x - x_mean) ** 2 for x in x_values)

        slope = numerator / max(denominator, 0.001)

        # Determine trend
        if slope > 0.5:
            trend = "improving"
        elif slope < -0.5:
            trend = "declining"
        else:
            trend = "stable"

        # Predict next score
        predicted = y_values[-1] + slope
        predicted = max(0, min(100, predicted))

        # Generate recommendation
        if trend == "improving":
            recommendation = "Trend is positief — blijf huidige aanpak voortzetten"
        elif trend == "declining":
            recommendation = (
                "Trend is negatief — onderzoek oorzaak en pas interventie toe"
            )
        else:
            recommendation = "Trend is stabiel — overweeg proactieve verbetering"

        return TrendAnalysis(
            product_name=product_name,
            snapshots_count=n,
            trend=trend,
            slope=round(slope, 3),
            current_score=y_values[-1],
            predicted_next_score=round(predicted, 1),
            recommendation=recommendation,
        )

    def detect_regression(
        self, product_name: str, window: int = 5, threshold: float = -2.0
    ) -> dict[str, Any]:
        """Detecteer significante regressie in kwaliteit."""
        snapshots = self.get_snapshots(product_name)

        if len(snapshots) < window:
            return {"detected": False, "reason": "Onvoldoende data"}

        recent = snapshots[-window:]
        scores = [s.score for s in recent]

        # Check if last N scores show significant decline
        avg_before = sum(scores[:-1]) / max(len(scores) - 1, 1)
        latest = scores[-1]
        delta = latest - avg_before

        return {
            "detected": delta < threshold,
            "delta": round(delta, 2),
            "average_before": round(avg_before, 2),
            "latest": latest,
            "window": window,
        }

    def compute_improvement_rate(self, product_name: str) -> dict[str, Any]:
        """Bereken de verbeteringsslope per maand."""
        snapshots = self.get_snapshots(product_name)

        if len(snapshots) < 2:
            return {"rate": 0, "unit": "score/month"}

        first = snapshots[0]
        last = snapshots[-1]

        try:
            t1 = datetime.fromisoformat(first.timestamp)
            t2 = datetime.fromisoformat(last.timestamp)
            months = max((t2 - t1).days / 30, 0.1)
        except (ValueError, TypeError):
            months = 1.0

        score_delta = last.score - first.score
        rate = score_delta / months

        return {
            "rate": round(rate, 2),
            "unit": "score/month",
            "total_improvement": round(score_delta, 2),
            "period_months": round(months, 1),
        }

    def generate_report(self, product_name: str) -> dict[str, Any]:
        """Genereer een longitudinaal evaluatierapport."""
        trend = self.analyze_trend(product_name)
        regression = self.detect_regression(product_name)
        improvement = self.compute_improvement_rate(product_name)

        return {
            "product": product_name,
            "trend": trend.trend,
            "slope": trend.slope,
            "current_score": trend.current_score,
            "predicted_next": trend.predicted_next_score,
            "regression_detected": regression.get("detected", False),
            "improvement_rate": improvement["rate"],
            "recommendation": trend.recommendation,
        }

    def to_dict(self) -> dict[str, Any]:
        products = list(set(s.product_name for s in self._snapshots))
        return {
            "total_snapshots": len(self._snapshots),
            "products_tracked": products,
            "snapshots": [
                {
                    "timestamp": s.timestamp,
                    "product": s.product_name,
                    "score": s.score,
                    "decision": s.release_decision,
                }
                for s in self._snapshots[-20:]  # Last 20
            ],
        }


# ─── Singleton ─────────────────────────────────────────────────

longitudinal_eval = LongitudinalEvaluation()
