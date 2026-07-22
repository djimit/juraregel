"""Continuous Evaluation Auditor — JLAIF audit voor de Continuous Evaluation Engine.

This is the "auditor of the auditor" — checks whether the continuous evaluation
engine itself is reliable. Key risks:
- Self-reference bias (checks hardcoded to True)
- Grade inflation
- Missing independent validation
- False confidence in self-assessment
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
class EvalFinding:
    """A single evaluation audit finding."""

    error_type: LegalErrorType
    severity: Severity
    description: str
    evidence: str
    category: str


@dataclass
class EvalAuditReport:
    """Complete evaluation audit report."""

    audit_id: str
    timestamp: str
    report_id: str
    findings: list[EvalFinding]
    severity_distribution: SeverityDistribution
    release_decision: str
    human_review_required: bool
    modules_evaluated: int
    overall_grade: str
    overall_score: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "timestamp": self.timestamp,
            "report_id": self.report_id,
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
            "modules_evaluated": self.modules_evaluated,
            "overall_grade": self.overall_grade,
            "overall_score": self.overall_score,
        }


class ContinuousEvaluationAuditor:
    """Audits the Continuous Evaluation Engine."""

    def audit(
        self,
        report: dict[str, Any],
        use_case: UseCaseProfile | None = None,
    ) -> EvalAuditReport:
        """Audit a continuous evaluation report."""
        if use_case is None:
            use_case = UseCaseProfile(
                name="continuous_eval_audit",
                autonomy_level=4,
                legal_domain="algemeen",
                user_group="auditor",
            )

        findings: list[EvalFinding] = []

        # Check self-reference bias
        findings.extend(self._check_self_reference(report))

        # Check grade inflation
        findings.extend(self._check_grade_inflation(report))

        # Check independence
        findings.extend(self._check_independence(report))

        # Check coverage
        findings.extend(self._check_coverage(report))

        # Check false confidence
        findings.extend(self._check_false_confidence(report))

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

        return EvalAuditReport(
            audit_id=f"eval-audit-{int(time.time())}",
            timestamp=datetime.now().isoformat(),
            report_id=report.get("report_id", "unknown"),
            findings=findings,
            severity_distribution=distribution,
            release_decision=decision.verdict,
            human_review_required=decision.verdict != "GO",
            modules_evaluated=len(report.get("results", [])),
            overall_grade=report.get("overall_grade", "?"),
            overall_score=report.get("overall_score", 0),
        )

    def _check_self_reference(self, report: dict) -> list[EvalFinding]:
        """Check for self-reference bias (all checks pass)."""
        findings = []
        results = report.get("results", [])

        if not results:
            return findings

        all_passed = all(r.get("passed", False) for r in results)
        if all_passed and len(results) > 2:
            findings.append(
                EvalFinding(
                    error_type=LegalErrorType.BIAS,
                    severity=Severity.S4_RECHTSVERLIES,
                    description=f"Alle {len(results)} modules slagen — mogelijke self-reference bias",
                    evidence="Zelf-evaluatie die alles als 'passed' markeert is niet onafhankelijk",
                    category="self_reference",
                )
            )

        return findings

    def _check_grade_inflation(self, report: dict) -> list[EvalFinding]:
        """Check for grade inflation."""
        findings = []
        grade = report.get("overall_grade", "")
        score = report.get("overall_score", 0)

        # A-grade with score < 0.95 is suspicious
        if grade == "A" and score < 0.9:
            findings.append(
                EvalFinding(
                    error_type=LegalErrorType.FACTUAL,
                    severity=Severity.S3_MATERIEEL,
                    description=f"Grade inflation: A-grade met score {score:.2f}",
                    evidence=f"Grade {grade} verwacht score >= 0.90",
                    category="grade_inflation",
                )
            )

        return findings

    def _check_independence(self, report: dict) -> list[EvalFinding]:
        """Check for independent validation."""
        findings = []
        results = report.get("results", [])

        # Check if any module failed (indicator of independence)
        failed = [r for r in results if not r.get("passed", True)]
        if not failed and len(results) > 3:
            findings.append(
                EvalFinding(
                    error_type=LegalErrorType.PROCEDURAL,
                    severity=Severity.S3_MATERIEEL,
                    description="Geen ene module gefaald — onafhankelijke validatie ontbreekt",
                    evidence="Zonder failures is de evaluatie mogelijk niet kritisch genoeg",
                    category="independence",
                )
            )

        return findings

    def _check_coverage(self, report: dict) -> list[EvalFinding]:
        """Check evaluation coverage."""
        findings = []
        results = report.get("results", [])

        expected_modules = 6
        if len(results) < expected_modules:
            findings.append(
                EvalFinding(
                    error_type=LegalErrorType.OMISSION,
                    severity=Severity.S2_HERSTELBAAR,
                    description=f"Onvolledige dekking: {len(results)}/{expected_modules} modules geëvalueerd",
                    evidence=f"Geëvalueerd: {[r.get('module') for r in results]}",
                    category="coverage",
                )
            )

        return findings

    def _check_false_confidence(self, report: dict) -> list[EvalFinding]:
        """Check for false confidence in self-assessment."""
        findings = []
        results = report.get("results", [])

        # Check if all scores are rounded (indicator of estimation)
        scores = [r.get("score", 0) for r in results]
        all_rounded = all(s == int(s) or s * 10 == int(s * 10) for s in scores if s > 0)

        if all_rounded and len(scores) > 3:
            findings.append(
                EvalFinding(
                    error_type=LegalErrorType.INTERPRETATION,
                    severity=Severity.S2_HERSTELBAAR,
                    description="Alle scores zijn afgerond — mogelijke false confidence",
                    evidence=f"Scores: {scores}",
                    category="false_confidence",
                )
            )

        return findings


# ─── Singleton ─────────────────────────────────────────────────

continuous_evaluation_auditor = ContinuousEvaluationAuditor()
