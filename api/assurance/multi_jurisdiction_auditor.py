"""Multi-Jurisdiction Auditor — JLAIF audit voor de Multi-Jurisdiction Engine.

Audits the multi-jurisdiction analysis for:
- Jurisdiction confusion (most common error in our audits)
- Outdated articles and penalties
- Missed conflicts
- Framework coverage gaps
- Penalty accuracy
"""

from __future__ import annotations

import logging
import re
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

# Known outdated or incorrect penalty amounts
PENALTY_BENCHMARKS = {
    "AVG Art. 5": {"max": "EUR 20.000.000", "percent": "4%"},
    "AVG Art. 32": {"max": "EUR 10.000.000", "percent": "2%"},
    "AVG Art. 35": {"max": "EUR 10.000.000", "percent": "2%"},
    "AI Act Art. 9": {"max": "EUR 15.000.000", "percent": "3%"},
    "AI Act Art. 10": {"max": "EUR 15.000.000", "percent": "3%"},
    "NIS2 Art. 21": {"max": "EUR 10.000.000", "percent": "2%"},
}

# Known deadlines (2026 perspective)
KNOWN_DEADLINES = {
    "EU AI Act hoog-risico": "2026-08-02",
    "NIS2 implementatie NL": "2024-10-17",
    "eIDAS herziening": "2026-01-01",
}


@dataclass
class JurisdictionFinding:
    """A single multi-jurisdiction audit finding."""

    error_type: LegalErrorType
    severity: Severity
    description: str
    evidence: str
    category: str


@dataclass
class JurisdictionAuditReport:
    """Complete multi-jurisdiction audit report."""

    audit_id: str
    timestamp: str
    findings: list[JurisdictionFinding]
    severity_distribution: SeverityDistribution
    release_decision: str
    human_review_required: bool
    obligation_count: int
    conflict_count: int
    gap_count: int
    frameworks: list[str]

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
            "obligation_count": self.obligation_count,
            "conflict_count": self.conflict_count,
            "gap_count": self.gap_count,
            "frameworks": self.frameworks,
        }


class MultiJurisdictionAuditor:
    """Audits Multi-Jurisdiction Engine output."""

    def audit(
        self,
        report: dict[str, Any],
        use_case: UseCaseProfile | None = None,
    ) -> JurisdictionAuditReport:
        """Audit a multi-jurisdiction report."""
        if use_case is None:
            use_case = UseCaseProfile(
                name="multi_jurisdiction_audit",
                autonomy_level=3,
                legal_domain="multi",
                user_group="jurist",
            )

        findings: list[JurisdictionFinding] = []

        # Check jurisdiction consistency
        findings.extend(self._check_jurisdiction_consistency(report))

        # Check penalty accuracy
        findings.extend(self._check_penalty_accuracy(report))

        # Check deadline validity
        findings.extend(self._check_deadlines(report))

        # Check conflict detection
        findings.extend(self._check_conflict_detection(report))

        # Check framework coverage
        findings.extend(self._check_framework_coverage(report))

        # Check article references
        findings.extend(self._check_article_references(report))

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

        return JurisdictionAuditReport(
            audit_id=f"jur-audit-{int(time.time())}",
            timestamp=datetime.now().isoformat(),
            findings=findings,
            severity_distribution=distribution,
            release_decision=decision.verdict,
            human_review_required=decision.verdict != "GO",
            obligation_count=len(report.get("obligations", [])),
            conflict_count=len(report.get("conflicts", [])),
            gap_count=len(report.get("gaps", [])),
            frameworks=report.get("applicable_frameworks", []),
        )

    def _check_jurisdiction_consistency(
        self, report: dict
    ) -> list[JurisdictionFinding]:
        """Check if obligations are assigned to correct jurisdictions."""
        findings = []
        obligations = report.get("obligations", [])

        for ob in obligations:
            framework = ob.get("framework", "")
            jurisdiction = ob.get("jurisdiction", "")

            # AVG should be NL or EU, not INT
            if framework == "AVG" and jurisdiction == "INT":
                findings.append(
                    JurisdictionFinding(
                        error_type=LegalErrorType.JURISDICTION,
                        severity=Severity.S4_RECHTSVERLIES,
                        description="AVG toegewezen aan internationale jurisdictie in plaats van NL/EU",
                        evidence=f"Framework: {framework}, Jurisdiction: {jurisdiction}",
                        category="jurisdiction_consistency",
                    )
                )

            # AI Act should be EU, not NL
            if framework == "EU AI Act" and jurisdiction == "NL":
                findings.append(
                    JurisdictionFinding(
                        error_type=LegalErrorType.JURISDICTION,
                        severity=Severity.S3_MATERIEEL,
                        description="EU AI Act toegewezen aan NL jurisdictie in plaats van EU",
                        evidence=f"Framework: {framework}, Jurisdiction: {jurisdiction}",
                        category="jurisdiction_consistency",
                    )
                )

        return findings

    def _check_penalty_accuracy(self, report: dict) -> list[JurisdictionFinding]:
        """Check if penalty amounts are accurate."""
        findings = []
        obligations = report.get("obligations", [])

        for ob in obligations:
            penalty = ob.get("penalty", "")
            article = ob.get("article", "")

            # Check for inflated penalties
            if penalty and "EUR" in penalty:
                match = re.search(r"EUR\s*([\d\.]+)\.([\d\.]+)\.([\d\.]+)", penalty)
                if match:
                    amount = int(match.group(1).replace(".", ""))
                    # AVG max is 20M, AI Act max is 15M
                    if "AVG" in ob.get("framework", "") and amount > 20:
                        findings.append(
                            JurisdictionFinding(
                                error_type=LegalErrorType.FACTUAL,
                                severity=Severity.S3_MATERIEEL,
                                description=f"Ongeldige boete: {penalty} — AVG max is EUR 20M",
                                evidence=f"Article: {article}",
                                category="penalty_accuracy",
                            )
                        )

        return findings

    def _check_deadlines(self, report: dict) -> list[JurisdictionFinding]:
        """Check if deadlines are still valid."""
        findings = []
        obligations = report.get("obligations", [])

        for ob in obligations:
            deadline = ob.get("deadline", "")
            if deadline and "2023" in deadline:
                findings.append(
                    JurisdictionFinding(
                        error_type=LegalErrorType.TEMPORAL,
                        severity=Severity.S3_MATERIEEL,
                        description=f"Verstreken deadline: {deadline}",
                        evidence=f"Obligation: {ob.get('title', '')}",
                        category="deadlines",
                    )
                )

        return findings

    def _check_conflict_detection(self, report: dict) -> list[JurisdictionFinding]:
        """Check if conflicts are properly detected."""
        findings = []
        obligations = report.get("obligations", [])
        conflicts = report.get("conflicts", [])

        # If multiple jurisdictions but no conflicts, suspicious
        jurisdictions = {ob.get("jurisdiction", "") for ob in obligations}
        if len(jurisdictions) > 1 and not conflicts:
            findings.append(
                JurisdictionFinding(
                    error_type=LegalErrorType.OMISSION,
                    severity=Severity.S2_HERSTELBAAR,
                    description=f"Meerdere jurisdicties ({jurisdictions}) maar geen conflicten geïdentificeerd",
                    evidence="Multi-jurisdiction zonder conflicts is onwaarschijnlijk",
                    category="conflict_detection",
                )
            )

        return findings

    def _check_framework_coverage(self, report: dict) -> list[JurisdictionFinding]:
        """Check if all applicable frameworks are covered."""
        findings = []
        frameworks = report.get("applicable_frameworks", [])
        obligations = report.get("obligations", [])

        covered_frameworks = {ob.get("framework", "") for ob in obligations}
        missing = set(frameworks) - covered_frameworks

        if missing:
            findings.append(
                JurisdictionFinding(
                    error_type=LegalErrorType.OMISSION,
                    severity=Severity.S3_MATERIEEL,
                    description=f"Frameworks zonder obligaties: {missing}",
                    evidence=f"Toegepast: {frameworks}, Obligaties: {covered_frameworks}",
                    category="framework_coverage",
                )
            )

        return findings

    def _check_article_references(self, report: dict) -> list[JurisdictionFinding]:
        """Check if article references are valid."""
        findings = []
        obligations = report.get("obligations", [])

        for ob in obligations:
            article = ob.get("article", "")
            framework = ob.get("framework", "")

            # Check for malformed article references
            if not re.match(r"^Art\.?\s*\d+", article):
                findings.append(
                    JurisdictionFinding(
                        error_type=LegalErrorType.SOURCE,
                        severity=Severity.S2_HERSTELBAAR,
                        description=f"Onconventieel artikel format: '{article}'",
                        evidence=f"Framework: {framework}",
                        category="article_references",
                    )
                )

        return findings


# ─── Singleton ─────────────────────────────────────────────────

multi_jurisdiction_auditor = MultiJurisdictionAuditor()
