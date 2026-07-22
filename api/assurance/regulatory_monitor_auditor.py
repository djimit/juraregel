"""Regulatory Monitor Auditor — JLAIF audit voor de Regulatory Monitor.

Audits regulatory change detection for:
- Change detection accuracy
- False positives in scraping
- Impact assessment quality
- Temporal validity of detected changes
- Framework coverage
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
class RegulatoryFinding:
    """A single regulatory monitor finding."""

    error_type: LegalErrorType
    severity: Severity
    description: str
    evidence: str
    category: str


@dataclass
class RegulatoryAuditReport:
    """Complete regulatory monitor audit report."""

    audit_id: str
    timestamp: str
    findings: list[RegulatoryFinding]
    severity_distribution: SeverityDistribution
    release_decision: str
    human_review_required: bool
    changes_detected: int
    errors_count: int
    sources_scanned: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "timestamp": self.timestamp,
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
            "changes_detected": self.changes_detected,
            "errors_count": self.errors_count,
            "sources_scanned": self.sources_scanned,
        }


class RegulatoryMonitorAuditor:
    """Audits Regulatory Monitor output."""

    def audit(
        self,
        result: dict[str, Any],
        use_case: UseCaseProfile | None = None,
    ) -> RegulatoryAuditReport:
        """Audit a regulatory scan result."""
        if use_case is None:
            use_case = UseCaseProfile(
                name="regulatory_monitor_audit",
                autonomy_level=3,
                legal_domain="algemeen",
                user_group="compliance_officer",
            )

        findings: list[RegulatoryFinding] = []

        # Check for scan errors
        findings.extend(self._check_scan_errors(result))

        # Check change quality
        findings.extend(self._check_change_quality(result))

        # Check impact assessment
        findings.extend(self._check_impact_assessment(result))

        # Check temporal validity
        findings.extend(self._check_temporal_validity(result))

        # Check framework coverage
        findings.extend(self._check_framework_coverage(result))

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

        return RegulatoryAuditReport(
            audit_id=f"reg-audit-{int(time.time())}",
            timestamp=datetime.now().isoformat(),
            findings=findings,
            severity_distribution=distribution,
            release_decision=decision.verdict,
            human_review_required=decision.verdict != "GO",
            changes_detected=result.get("changes_detected", 0),
            errors_count=len(result.get("errors", [])),
            sources_scanned=result.get("sources_scanned", 0),
        )

    def _check_scan_errors(self, result: dict) -> list[RegulatoryFinding]:
        """Check for scan errors."""
        findings = []
        errors = result.get("errors", [])

        if errors:
            findings.append(
                RegulatoryFinding(
                    error_type=LegalErrorType.PROCEDURAL,
                    severity=Severity.S2_HERSTELBAAR,
                    description=f"{len(errors)} scan-fouten gedetecteerd",
                    evidence=f"Errors: {str(errors)[:100]}",
                    category="scan_errors",
                )
            )

        return findings

    def _check_change_quality(self, result: dict) -> list[RegulatoryFinding]:
        """Check quality of detected changes."""
        findings = []
        changes = result.get("changes", [])

        if not changes and result.get("changes_detected", 0) > 0:
            findings.append(
                RegulatoryFinding(
                    error_type=LegalErrorType.FACTUAL,
                    severity=Severity.S3_MATERIEEL,
                    description="Changes_detected > 0 maar geen changes data",
                    evidence="Inconsistent change reporting",
                    category="change_quality",
                )
            )

        # Check for changes without impact assessment
        for change in changes:
            if not change.get("impact_level"):
                findings.append(
                    RegulatoryFinding(
                        error_type=LegalErrorType.OMISSION,
                        severity=Severity.S2_HERSTELBAAR,
                        description=f"Change zonder impact assessment: {change.get('title', '')[:50]}",
                        evidence="Missing impact_level",
                        category="change_quality",
                    )
                )

        return findings

    def _check_impact_assessment(self, result: dict) -> list[RegulatoryFinding]:
        """Check impact assessment quality."""
        findings = []
        changes = result.get("changes", [])

        for change in changes:
            impact_score = change.get("impact_score", 0)
            impact_level = change.get("impact_level", "")

            # Check consistency between score and level
            if impact_score > 0.7 and impact_level in ("low", "medium"):
                findings.append(
                    RegulatoryFinding(
                        error_type=LegalErrorType.INTERPRETATION,
                        severity=Severity.S2_HERSTELBAAR,
                        description=f"Impact score {impact_score} inconsistent met level '{impact_level}'",
                        evidence=f"Change: {change.get('title', '')[:50]}",
                        category="impact_assessment",
                    )
                )

        return findings

    def _check_temporal_validity(self, result: dict) -> list[RegulatoryFinding]:
        """Check temporal validity of detected changes."""
        findings = []
        changes = result.get("changes", [])

        for change in changes:
            effective_date = change.get("effective_date", "")
            if effective_date and "2022" in effective_date:
                findings.append(
                    RegulatoryFinding(
                        error_type=LegalErrorType.TEMPORAL,
                        severity=Severity.S2_HERSTELBAAR,
                        description=f"Mogelijk verouderde change: {change.get('title', '')[:50]}",
                        evidence=f"Effective date: {effective_date}",
                        category="temporal_validity",
                    )
                )

        return findings

    def _check_framework_coverage(self, result: dict) -> list[RegulatoryFinding]:
        """Check framework coverage."""
        findings = []
        changes = result.get("changes", [])

        if changes:
            all_frameworks = set()
            for change in changes:
                all_frameworks.update(change.get("affected_frameworks", []))

            expected = {"AVG", "EU AI Act", "NIS2", "eIDAS"}
            missing = expected - all_frameworks
            if missing and len(changes) > 5:
                findings.append(
                    RegulatoryFinding(
                        error_type=LegalErrorType.OMISSION,
                        severity=Severity.S2_HERSTELBAAR,
                        description=f"Frameworks niet gedetecteerd: {missing}",
                        evidence=f"Gedetecteerd: {all_frameworks}",
                        category="framework_coverage",
                    )
                )

        return findings


# ─── Singleton ─────────────────────────────────────────────────

regulatory_monitor_auditor = RegulatoryMonitorAuditor()
