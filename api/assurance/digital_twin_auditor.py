"""Digital Twin Auditor — JLAIF audit voor de Compliance Digital Twin.

Audits the digital twin output for:
- Realism of predictions (simulations vs reality)
- Bias in scenario selection
- Completeness of risk coverage
- Temporal validity of scores
- False precision in impact predictions
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
class TwinFinding:
    """A single digital twin audit finding."""

    error_type: LegalErrorType
    severity: Severity
    description: str
    evidence: str
    category: str


@dataclass
class TwinAuditReport:
    """Complete digital twin audit report."""

    audit_id: str
    timestamp: str
    organisation_id: str
    findings: list[TwinFinding]
    severity_distribution: SeverityDistribution
    release_decision: str
    human_review_required: bool
    node_count: int
    scenario_count: int
    alert_count: int
    overall_score: float

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
            "node_count": self.node_count,
            "scenario_count": self.scenario_count,
            "alert_count": self.alert_count,
            "overall_score": self.overall_score,
        }


class DigitalTwinAuditor:
    """Audits Digital Twin output."""

    def audit(
        self,
        report: dict[str, Any],
        use_case: UseCaseProfile | None = None,
    ) -> TwinAuditReport:
        """Audit a digital twin report."""
        if use_case is None:
            use_case = UseCaseProfile(
                name="digital_twin_audit",
                autonomy_level=3,
                legal_domain="algemeen",
                user_group="compliance_officer",
            )

        findings: list[TwinFinding] = []

        # Check node coverage
        findings.extend(self._check_node_coverage(report))

        # Check scenario realism
        findings.extend(self._check_scenario_realism(report))

        # Check score validity
        findings.extend(self._check_score_validity(report))

        # Check bias in alerts
        findings.extend(self._check_alert_bias(report))

        # Check false precision
        findings.extend(self._check_false_precision(report))

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

        return TwinAuditReport(
            audit_id=f"twin-audit-{int(time.time())}",
            timestamp=datetime.now().isoformat(),
            organisation_id=report.get("organisation_id", "unknown"),
            findings=findings,
            severity_distribution=distribution,
            release_decision=decision.verdict,
            human_review_required=decision.verdict != "GO",
            node_count=len(report.get("nodes", [])),
            scenario_count=len(report.get("scenarios", [])),
            alert_count=len(report.get("alerts", [])),
            overall_score=report.get("overall_score", 0),
        )

    def _check_node_coverage(self, report: dict) -> list[TwinFinding]:
        """Check if all required node types are present."""
        findings = []
        nodes = report.get("nodes", [])
        node_types = {n.get("node_type", "") for n in nodes}

        required_types = {"processing", "risk", "framework"}
        missing = required_types - node_types

        if missing:
            findings.append(
                TwinFinding(
                    error_type=LegalErrorType.OMISSION,
                    severity=Severity.S3_MATERIEEL,
                    description=f"Ontbrekende node types in digital twin: {missing}",
                    evidence=f"Aanwezig: {node_types}",
                    category="node_coverage",
                )
            )

        # Check for at least 1 processing node
        processing_nodes = [n for n in nodes if n.get("node_type") == "processing"]
        if not processing_nodes:
            findings.append(
                TwinFinding(
                    error_type=LegalErrorType.OMISSION,
                    severity=Severity.S4_RECHTSVERLIES,
                    description="Geen verwerkingsactiviteit nodes in digital twin",
                    evidence="Twin zonder verwerkingsactiviteiten heeft geen realiteitswaarde",
                    category="node_coverage",
                )
            )

        return findings

    def _check_scenario_realism(self, report: dict) -> list[TwinFinding]:
        """Check if scenarios are realistic."""
        findings = []
        scenarios = report.get("scenarios", [])

        if not scenarios:
            findings.append(
                TwinFinding(
                    error_type=LegalErrorType.OMISSION,
                    severity=Severity.S3_MATERIEEL,
                    description="Geen 'what-if' scenarios gegenereerd",
                    evidence="Digital twin zonder scenarios heeft geen voorspellende waarde",
                    category="scenario_realism",
                )
            )
            return findings

        # Check for unrealistic impact predictions
        for scenario in scenarios:
            impact = scenario.get("predicted_impact", {})
            for framework, delta in impact.items():
                if abs(delta) > 30:
                    findings.append(
                        TwinFinding(
                            error_type=LegalErrorType.FACTUAL,
                            severity=Severity.S2_HERSTELBAAR,
                            description=f"Ongerealistiche impact voorspelling: {framework} {delta:+d} punten",
                            evidence=f"Scenario: {scenario.get('description', '')[:50]}",
                            category="scenario_realism",
                        )
                    )

        # Check for bias: all scenarios positive
        all_positive = all(
            all(v >= 0 for v in s.get("predicted_impact", {}).values())
            for s in scenarios
        )
        if all_positive and len(scenarios) > 1:
            findings.append(
                TwinFinding(
                    error_type=LegalErrorType.BIAS,
                    severity=Severity.S3_MATERIEEL,
                    description="Alle scenarios voorspellen positieve impact — mogelijke optimism bias",
                    evidence="Geen negatieve scenario's gegenereerd",
                    category="scenario_realism",
                )
            )

        return findings

    def _check_score_validity(self, report: dict) -> list[TwinFinding]:
        """Check if scores are within valid ranges."""
        findings = []

        # Check overall score
        overall = report.get("overall_score", 0)
        if overall < 0 or overall > 100:
            findings.append(
                TwinFinding(
                    error_type=LegalErrorType.FACTUAL,
                    severity=Severity.S3_MATERIEEL,
                    description=f"Ongeldige overall score: {overall} (moet 0-100 zijn)",
                    evidence=f"Score: {overall}",
                    category="score_validity",
                )
            )

        # Check framework scores
        fw_scores = report.get("framework_scores", {})
        for fw, score in fw_scores.items():
            if score < 0 or score > 100:
                findings.append(
                    TwinFinding(
                        error_type=LegalErrorType.FACTUAL,
                        severity=Severity.S2_HERSTELBAAR,
                        description=f"Ongeldige framework score {fw}: {score}",
                        evidence=f"Score: {score}",
                        category="score_validity",
                    )
                )

        return findings

    def _check_alert_bias(self, report: dict) -> list[TwinFinding]:
        """Check for bias in alert generation."""
        findings = []
        alerts = report.get("alerts", [])
        nodes = report.get("nodes", [])

        # Check if at-risk nodes have corresponding alerts
        at_risk = [n for n in nodes if n.get("status") == "at_risk"]
        if at_risk and not alerts:
            findings.append(
                TwinFinding(
                    error_type=LegalErrorType.OMISSION,
                    severity=Severity.S3_MATERIEEL,
                    description=f"{len(at_risk)} at-risico nodes maar geen alerts",
                    evidence=f"At-risk nodes: {[n.get('name') for n in at_risk]}",
                    category="alert_bias",
                )
            )

        return findings

    def _check_false_precision(self, report: dict) -> list[TwinFinding]:
        """Check for false precision in predictions."""
        findings = []
        scenarios = report.get("scenarios", [])

        for scenario in scenarios:
            impact = scenario.get("predicted_impact", {})
            # Check for overly precise predictions (e.g., exactly +15, +20)
            for framework, delta in impact.items():
                if delta % 5 == 0 and abs(delta) > 10:
                    findings.append(
                        TwinFinding(
                            error_type=LegalErrorType.INTERPRETATION,
                            severity=Severity.S2_HERSTELBAAR,
                            description=f"False precision in prediction: {framework} {delta:+d} (waarschijnlijk afgerond)",
                            evidence=f"Scenario: {scenario.get('description', '')[:50]}",
                            category="false_precision",
                        )
                    )

        return findings


# ─── Singleton ─────────────────────────────────────────────────

digital_twin_auditor = DigitalTwinAuditor()
