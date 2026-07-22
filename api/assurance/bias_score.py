"""Bias Score Calculator — breekt bias down per AI-product.

Combineert bevindingen van alle auditors om een geaggregeerde bias-score
per product te berekenen. Maakt trendanalyse en cross-product vergelijking mogelijk.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ProductBiasScore:
    """Bias score for a single product."""

    product_name: str
    total_audits: int
    total_findings: int
    bias_findings: int
    bias_rate: float  # bias findings / total findings
    severity_weighted_bias: float
    trend: str  # improving, stable, worsening
    top_bias_categories: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "product": self.product_name,
            "total_audits": self.total_audits,
            "total_findings": self.total_findings,
            "bias_findings": self.bias_findings,
            "bias_rate": round(self.bias_rate, 2),
            "severity_weighted_bias": round(self.severity_weighted_bias, 2),
            "trend": self.trend,
            "top_categories": self.top_bias_categories,
        }


@dataclass
class CrossProductBiasReport:
    """Cross-product bias comparison."""

    timestamp: str
    product_scores: list[ProductBiasScore]
    overall_bias_rate: float
    highest_risk_product: str
    lowest_risk_product: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "overall_bias_rate": round(self.overall_bias_rate, 2),
            "highest_risk": self.highest_risk_product,
            "lowest_risk": self.lowest_risk_product,
            "products": [p.to_dict() for p in self.product_scores],
        }


class BiasScoreCalculator:
    """Calculates bias scores across products."""

    def calculate_from_audits(
        self,
        audit_results: dict[str, list[dict[str, Any]]],
    ) -> CrossProductBiasReport:
        """Calculate bias scores from audit results."""
        product_scores = []

        for product, findings in audit_results.items():
            total = len(findings)
            bias_findings = [
                f
                for f in findings
                if f.get("type") in ("bias_ongelijke_behandeling", "bias")
            ]

            # Severity-weighted bias
            severity_weights = {"S1": 1, "S2": 2, "S3": 4, "S4": 8, "S5": 16}
            weighted = sum(
                severity_weights.get(f.get("severity", "S1"), 1) for f in bias_findings
            )

            # Top bias categories
            categories: dict[str, int] = {}
            for f in bias_findings:
                cat = f.get("category", "unknown")
                categories[cat] = categories.get(cat, 0) + 1

            top_categories = sorted(
                categories.keys(), key=lambda k: categories[k], reverse=True
            )[:3]

            score = ProductBiasScore(
                product_name=product,
                total_audits=1,
                total_findings=total,
                bias_findings=len(bias_findings),
                bias_rate=len(bias_findings) / max(total, 1),
                severity_weighted_bias=weighted,
                trend="stable",
                top_bias_categories=top_categories,
            )
            product_scores.append(score)

        # Overall
        total_findings = sum(p.total_findings for p in product_scores)
        total_bias = sum(p.bias_findings for p in product_scores)
        overall_rate = total_bias / max(total_findings, 1)

        # Highest/lowest risk
        if product_scores:
            highest = max(product_scores, key=lambda p: p.severity_weighted_bias)
            lowest = min(product_scores, key=lambda p: p.severity_weighted_bias)
        else:
            highest = lowest = ProductBiasScore("none", 0, 0, 0, 0, 0, "stable", [])

        return CrossProductBiasReport(
            timestamp=datetime.now().isoformat(),
            product_scores=product_scores,
            overall_bias_rate=overall_rate,
            highest_risk_product=highest.product_name,
            lowest_risk_product=lowest.product_name,
        )


# ─── Singleton ─────────────────────────────────────────────────

bias_calculator = BiasScoreCalculator()
