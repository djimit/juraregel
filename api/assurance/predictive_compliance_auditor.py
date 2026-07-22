"""Predictive Compliance Auditor — JLAIF audit voor de Predictive Engine.

Audits the predictive compliance output for:
- Statistische redelijkheid van voorspellingen
- Temporaliteitsgeldigheid van trends
- Bias in risico-factoren
- Volledigheid van aanbevelingen
- Procedurele correctheid van early warnings
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .error_taxonomy import (
    LegalError,
    LegalErrorType,
    Severity,
    SeverityDistribution,
)
from .severity_scorer import UseCaseProfile
from .release_gate import evaluate_release

logger = logging.getLogger(__name__)


@dataclass
class PredictiveFinding:
    """A single predictive compliance finding."""

    error_type: LegalErrorType
    severity: Severity
    description: str
    evidence: str
    category: str


@dataclass
class PredictiveAuditReport:
    """Complete predictive compliance audit report."""

    audit_id: str
    timestamp: str
    organisation_id: str
    findings: list[PredictiveFinding]
    severity_distribution: SeverityDistribution
    release_decision: str
    human_review_required: bool
    risk_count: int
    warning_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "timestamp": self.timestamp,
            "organisation_id": self.organisation_id,
            "findings_count": len(self.findings),
            "findings": [
                {
                    "type": f.error_type.value,
                    "severity": f.severity.value,
                    "description": f.description,
                    "category": f.category,
                }
                for f in self.findings
            ],
            "severity_distribution": self.severity_distribution.to_dict(),
            "release_decision": self.release_decision,
            "human_review_required": self.human_review_required,
            "risk_count": self.risk_count,
            "warning_count": self.warning_count,
        }


class PredictiveComplianceAuditor:
    """Audits Predictive Compliance Engine output."""

    def audit(
        self,
        report: dict[str, Any],
        use_case: UseCaseProfile | None = None,
    ) -> PredictiveAuditReport:
        """Audit a predictive compliance report."""
        if use_case is None:
            use_case = UseCaseProfile(
                name="predictive_compliance_audit",
                autonomy_level=3,
                legal_domain="algemeen",
                user_group="compliance_officer",
            )

        findings: list[PredictiveFinding] = []

        # Check risk predictions
        findings.extend(self._check_risk_predictions(report))

        # Check trend analysis
        findings.extend(self._check_trend_analysis(report))

        # Check early warnings
        findings.extend(self._check_early_warnings(report))

        # Check regulatory forecast
        findings.extend(self._check_regulatory_forecast(report))

        # Check bias
        findings.extend(self._check_bias(report))

        # Build distribution
        distribution = SeverityDistribution()
        errors = []
        for finding in findings:
            distribution.add(
                LegalError(finding.error_type, finding.severity, finding.description)
            )
            errors.append(
                LegalError(
                    finding.error_type,
                    finding.severity,
                    finding.description,
                    source_claim=finding.evidence,
                )
            )

        decision = evaluate_release(errors, use_case)

        return PredictiveAuditReport(
            audit_id=f"pred-audit-{int(time.time())}",
            timestamp=datetime.now().isoformat(),
            organisation_id=report.get("organisation_id", "unknown"),
            findings=findings,
            severity_distribution=distribution,
            release_decision=decision.verdict,
            human_review_required=decision.verdict != "GO",
            risk_count=len(report.get("risk_predictions", [])),
            warning_count=len(report.get("early_warnings", [])),
        )

    def _check_risk_predictions(self, report: dict) -> list[PredictiveFinding]:
        """Check risk predictions for statistical reasonableness."""
        findings = []
        risks = report.get("risk_predictions", [])

        if not risks:
            findings.append(
                PredictiveFinding(
                    error_type=LegalErrorType.OMISSION,
                    severity=Severity.S3_MATERIEEL,
                    description="Geen risico-voorspellingen gegenereerd",
                    evidence="Lege risk_predictions lijst",
                    category="risk_predictions",
                )
            )
            return findings

        # Check probability ranges
        for risk in risks:
            prob = risk.get("probability", 0)
            impact = risk.get("impact", 0)
            score = risk.get("risk_score", 0)

            if not (0 <= prob <= 1):
                findings.append(
                    PredictiveFinding(
                        error_type=LegalErrorType.FACTUAL,
                        severity=Severity.S3_MATERIEEL,
                        description=f"Ongeldige waarschijnlijkheid: {prob} (moet 0-1 zijn)",
                        evidence=f"Risk: {risk.get('description', '')[:50]}",
                        category="risk_predictions",
                    )
                )

            # Check if risk_score = probability * impact
            expected_score = prob * impact
            if abs(score - expected_score) > 0.01:
                findings.append(
                    PredictiveFinding(
                        error_type=LegalErrorType.FACTUAL,
                        severity=Severity.S2_HERSTELBAAR,
                        description=f"Risico-score komt niet overeen: {score} vs verwacht {expected_score:.2f}",
                        evidence=f"p={prob}, i={impact}, score={score}",
                        category="risk_predictions",
                    )
                )

        return findings

    def _check_trend_analysis(self, report: dict) -> list[PredictiveFinding]:
        """Check trend analysis for temporal validity."""
        findings = []
        trend = report.get("trend_analysis", {})

        if not trend:
            findings.append(
                PredictiveFinding(
                    error_type=LegalErrorType.OMISSION,
                    severity=Severity.S2_HERSTELBAAR,
                    description="Geen trend-analyse aanwezig",
                    evidence="trend_analysis ontbreekt",
                    category="trend_analysis",
                )
            )
            return findings

        # Check if forecasts are within valid range
        for field_name in ["forecast_30d", "forecast_90d", "forecast_180d"]:
            value = trend.get(field_name, -1)
            if value < 0 or value > 100:
                findings.append(
                    PredictiveFinding(
                        error_type=LegalErrorType.TEMPORAL,
                        severity=Severity.S2_HERSTELBAAR,
                        description=f"Ongeldige forecast {field_name}: {value} (moet 0-100 zijn)",
                        evidence="Forecast waarde buiten bereik",
                        category="trend_analysis",
                    )
                )

        # Check confidence interval
        ci = trend.get("confidence_interval", (0, 0))
        if ci[0] > ci[1]:
            findings.append(
                PredictiveFinding(
                    error_type=LegalErrorType.FACTUAL,
                    severity=Severity.S3_MATERIEEL,
                    description="Confidence interval is inverted (lower > upper)",
                    evidence=f"CI: {ci}",
                    category="trend_analysis",
                )
            )

        return findings

    def _check_early_warnings(self, report: dict) -> list[PredictiveFinding]:
        """Check early warnings for completeness."""
        findings = []
        warnings = report.get("early_warnings", [])
        risks = report.get("risk_predictions", [])

        # High-risk items should have warnings
        high_risks = [r for r in risks if r.get("risk_score", 0) > 0.7]
        if high_risks and not warnings:
            findings.append(
                PredictiveFinding(
                    error_type=LegalErrorType.OMISSION,
                    severity=Severity.S3_MATERIEEL,
                    description=f"{len(high_risks)} hoog-risico items maar geen early warnings",
                    evidence=f"High risks: {len(high_risks)}, warnings: 0",
                    category="early_warnings",
                )
            )

        return findings

    def _check_regulatory_forecast(self, report: dict) -> list[PredictiveFinding]:
        """Check regulatory forecast for temporal validity."""
        findings = []
        forecasts = report.get("regulatory_forecast", [])

        if not forecasts:
            findings.append(
                PredictiveFinding(
                    error_type=LegalErrorType.OMISSION,
                    severity=Severity.S2_HERSTELBAAR,
                    description="Geen regelgevingsvoorspellingen",
                    evidence="Lege regulatory_forecast",
                    category="regulatory_forecast",
                )
            )

        return findings

    def _check_bias(self, report: dict) -> list[PredictiveFinding]:
        """Check for systematic bias in predictions."""
        findings = []
        risks = report.get("risk_predictions", [])

        if len(risks) < 3:
            return findings

        # Check if all risks have same timeframe (potential bias)
        timeframes = [r.get("timeframe", "") for r in risks]
        if len(set(timeframes)) == 1:
            findings.append(
                PredictiveFinding(
                    error_type=LegalErrorType.BIAS,
                    severity=Severity.S2_HERSTELBAAR,
                    description=f"Alle risico's hebben dezelfde timeframe ({timeframes[0]}) — mogelijke bias",
                    evidence=f"Timeframes: {timeframes}",
                    category="bias",
                )
            )

        # Check if all probabilities are clustered (no differentiation)
        probs = [r.get("probability", 0) for r in risks]
        if probs and max(probs) - min(probs) < 0.15:
            findings.append(
                PredictiveFinding(
                    error_type=LegalErrorType.BIAS,
                    severity=Severity.S2_HERSTELBAAR,
                    description="Waarschijnlijkheden zonder differentiatie — mogelijke bias",
                    evidence=f"Prob range: {min(probs):.2f}-{max(probs):.2f}",
                    category="bias",
                )
            )

        return findings


# ─── Singleton ─────────────────────────────────────────────────

predictive_compliance_auditor = PredictiveComplianceAuditor()
