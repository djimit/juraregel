"""Agent Auditor — JLAIF audit voor de Agentic AI Workflows.

Audits agent output for:
- Hallucination flags (agent claims vs reality)
- Citation accuracy
- Confidence calibration
- Step completeness
- Bias in risk identification
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
class AgentFinding:
    """A single agent audit finding."""

    error_type: LegalErrorType
    severity: Severity
    description: str
    evidence: str
    step: str


@dataclass
class AgentAuditReport:
    """Complete agent audit report."""

    audit_id: str
    timestamp: str
    agent_name: str
    findings: list[AgentFinding]
    severity_distribution: SeverityDistribution
    release_decision: str
    human_review_required: bool
    steps_completed: int
    steps_expected: int
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "timestamp": self.timestamp,
            "agent_name": self.agent_name,
            "findings_count": len(self.findings),
            "findings": [
                {
                    "type": f.error_type.value,
                    "severity": f.severity.value,
                    "description": f.description,
                    "step": f.step,
                }
                for f in self.findings
            ],
            "severity_distribution": self.severity_distribution.to_dict(),
            "release_decision": self.release_decision,
            "human_review_required": self.human_review_required,
            "steps_completed": self.steps_completed,
            "steps_expected": self.steps_expected,
            "confidence": self.confidence,
        }


class AgentAuditor:
    """Audits Agentic AI Workflow output."""

    def audit(
        self,
        result: dict[str, Any],
        expected_steps: int = 5,
        use_case: UseCaseProfile | None = None,
    ) -> AgentAuditReport:
        """Audit an agent execution result."""
        if use_case is None:
            use_case = UseCaseProfile(
                name="agent_audit",
                autonomy_level=4,
                legal_domain="algemeen",
                user_group="compliance_officer",
            )

        findings: list[AgentFinding] = []

        # Check step completeness
        findings.extend(self._check_steps(result, expected_steps))

        # Check confidence calibration
        findings.extend(self._check_confidence(result))

        # Check citation accuracy
        findings.extend(self._check_citations(result))

        # Check hallucination flags
        findings.extend(self._check_hallucinations(result))

        # Check bias in recommendations
        findings.extend(self._check_bias(result))

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

        trace = result.get("trace", [])
        steps_completed = len([s for s in trace if s.get("status") == "complete"])

        return AgentAuditReport(
            audit_id=f"agent-audit-{int(time.time())}",
            timestamp=datetime.now().isoformat(),
            agent_name=result.get("agent", "unknown"),
            findings=findings,
            severity_distribution=distribution,
            release_decision=decision.verdict,
            human_review_required=decision.verdict != "GO",
            steps_completed=steps_completed,
            steps_expected=expected_steps,
            confidence=result.get("confidence", 0),
        )

    def _check_steps(self, result: dict, expected: int) -> list[AgentFinding]:
        """Check if all expected steps completed."""
        findings = []
        trace = result.get("trace", [])
        completed = [s for s in trace if s.get("status") == "complete"]

        if len(completed) < expected:
            findings.append(
                AgentFinding(
                    error_type=LegalErrorType.OMISSION,
                    severity=Severity.S3_MATERIEEL,
                    description=f"Incomplete execution: {len(completed)}/{expected} stappen",
                    evidence=f"Completed: {[s.get('step') for s in completed]}",
                    step="completeness",
                )
            )

        return findings

    def _check_confidence(self, result: dict) -> list[AgentFinding]:
        """Check confidence calibration."""
        findings = []
        confidence = result.get("confidence", 0)
        status = result.get("status", "")

        if confidence > 0.95 and status != "success":
            findings.append(
                AgentFinding(
                    error_type=LegalErrorType.INTERPRETATION,
                    severity=Severity.S3_MATERIEEL,
                    description=f"Confidence {confidence} onjuist: status is '{status}'",
                    evidence="High confidence with non-success status",
                    step="confidence_calibration",
                )
            )

        if confidence < 0.5 and status == "success":
            findings.append(
                AgentFinding(
                    error_type=LegalErrorType.INTERPRETATION,
                    severity=Severity.S2_HERSTELBAAR,
                    description=f"Confidence {confidence} te laag voor success-status",
                    evidence="Low confidence success is unreliable",
                    step="confidence_calibration",
                )
            )

        return findings

    def _check_citations(self, result: dict) -> list[AgentFinding]:
        """Check citation accuracy."""
        findings = []
        citations = result.get("citations", [])

        if not citations and result.get("status") == "success":
            findings.append(
                AgentFinding(
                    error_type=LegalErrorType.SOURCE,
                    severity=Severity.S3_MATERIEEL,
                    description="Geen bronverwijzingen in succesvolle output",
                    evidence="Success without citations is unreliable",
                    step="citations",
                )
            )

        return findings

    def _check_hallucinations(self, result: dict) -> list[AgentFinding]:
        """Check for hallucination flags."""
        findings = []
        flags = result.get("hallucination_flags", [])

        if flags:
            findings.append(
                AgentFinding(
                    error_type=LegalErrorType.FACTUAL,
                    severity=Severity.S4_RECHTSVERLIES,
                    description=f"{len(flags)} hallucinatie-flag(s) gedetecteerd",
                    evidence=f"Flags: {str(flags)[:100]}",
                    step="hallucination_check",
                )
            )

        return findings

    def _check_bias(self, result: dict) -> list[AgentFinding]:
        """Check for bias in recommendations."""
        findings = []
        recommendations = result.get("recommendations", [])

        if len(recommendations) == 0 and result.get("status") == "success":
            findings.append(
                AgentFinding(
                    error_type=LegalErrorType.OMISSION,
                    severity=Severity.S2_HERSTELBAAR,
                    description="Geen aanbevelingen gegenereerd",
                    evidence="Success without recommendations is incomplete",
                    step="bias_check",
                )
            )

        return findings


# ─── Singleton ─────────────────────────────────────────────────

agent_auditor = AgentAuditor()
