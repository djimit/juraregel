"""Orchestrator Auditor — JLAIF audit voor de Compliance Orchestrator.

Audits the autonomous compliance assessment output for:
- Juridische juistheid van conclusies
- Volledigheid van assessment stappen
- Bronverplichtingen per bewering
- Jurisdictie-consistentie
- Procedurele correctheid
- Bias in risico-prioritering
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


@dataclass
class OrchestratorFinding:
    """A single orchestrator audit finding."""

    error_type: LegalErrorType
    severity: Severity
    description: str
    evidence: str
    step: str


@dataclass
class OrchestratorAuditReport:
    """Complete orchestrator audit report."""

    audit_id: str
    timestamp: str
    assessment_id: str
    findings: list[OrchestratorFinding]
    severity_distribution: SeverityDistribution
    release_decision: str
    human_review_required: bool
    steps_completed: int
    steps_expected: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "timestamp": self.timestamp,
            "assessment_id": self.assessment_id,
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
        }


class OrchestratorAuditor:
    """Audits Compliance Orchestrator output."""

    EXPECTED_STEPS = 7

    def audit(
        self,
        assessment: dict[str, Any],
        use_case: UseCaseProfile | None = None,
    ) -> OrchestratorAuditReport:
        """Audit a complete compliance assessment."""
        if use_case is None:
            use_case = UseCaseProfile(
                name="orchestrator_audit",
                autonomy_level=4,
                legal_domain="algemeen",
                user_group="compliance_officer",
            )

        findings: list[OrchestratorFinding] = []

        # Check completeness
        findings.extend(self._check_step_completeness(assessment))

        # Check conclusion quality
        findings.extend(self._check_conclusion(assessment))

        # Check jurisdiction consistency
        findings.extend(self._check_jurisdiction(assessment))

        # Check bias in risk prioritization
        findings.extend(self._check_bias(assessment))

        # Check procedural correctness
        findings.extend(self._check_procedure(assessment))

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

        steps_completed = assessment.get("steps_completed", 0)

        return OrchestratorAuditReport(
            audit_id=f"orch-audit-{int(time.time())}",
            timestamp=datetime.now().isoformat(),
            assessment_id=assessment.get("assessment_id", "unknown"),
            findings=findings,
            severity_distribution=distribution,
            release_decision=decision.verdict,
            human_review_required=decision.verdict != "GO",
            steps_completed=steps_completed,
            steps_expected=self.EXPECTED_STEPS,
        )

    def _check_step_completeness(self, assessment: dict) -> list[OrchestratorFinding]:
        """Check if all expected assessment steps are present."""
        findings = []
        required_steps = [
            "jurisdiction_analysis",
            "risk_prediction",
            "knowledge_graph",
            "drift_detection",
            "rag_search",
            "synthese",
            "audit_logging",
        ]

        steps = assessment.get("steps", [])
        step_names = [s.get("name", "") for s in steps]

        for required in required_steps:
            if required not in step_names:
                findings.append(
                    OrchestratorFinding(
                        error_type=LegalErrorType.OMISSION,
                        severity=Severity.S3_MATERIEEL,
                        description=f"Ontbrekende assessment stap: {required}",
                        evidence=f"Gevonden stappen: {step_names}",
                        step="completeness_check",
                    )
                )

        return findings

    def _check_conclusion(self, assessment: dict) -> list[OrchestratorFinding]:
        """Check the quality of the conclusion."""
        findings = []
        conclusion = assessment.get("conclusion", "")

        if not conclusion:
            findings.append(
                OrchestratorFinding(
                    error_type=LegalErrorType.OMISSION,
                    severity=Severity.S4_RECHTSVERLIES,
                    description="Geen conclusie gegenereerd",
                    evidence="Lege conclusie in assessment output",
                    step="conclusion_check",
                )
            )
            return findings

        # Check for citations
        citation_patterns = [r"Art\.?\s*\d+", r"§\s*\d+", r"ECLI:", r"EB|EDPB"]
        citation_count = sum(len(re.findall(p, conclusion)) for p in citation_patterns)

        word_count = len(conclusion.split())
        expected_citations = max(1, word_count // 100)

        if citation_count < expected_citations:
            findings.append(
                OrchestratorFinding(
                    error_type=LegalErrorType.SOURCE,
                    severity=Severity.S3_MATERIEEL,
                    description=f"Conclusie heeft onvoldoende bronverwijzingen: {citation_count}/{expected_citations}",
                    evidence=f"Woorden: {word_count}, citaties: {citation_count}",
                    step="conclusion_check",
                )
            )

        return findings

    def _check_jurisdiction(self, assessment: dict) -> list[OrchestratorFinding]:
        """Check jurisdiction consistency."""
        findings = []
        jurisdiction = assessment.get("jurisdiction_analysis", {})
        conclusion = assessment.get("conclusion", "")

        primary_jurisdiction = jurisdiction.get("primary", "")
        if primary_jurisdiction and conclusion:
            # Check if conclusion references different jurisdiction
            if primary_jurisdiction == "nederland":
                eu_only_terms = ["EU AI Act", "Europese richtlijn", "EDPB"]
                for term in eu_only_terms:
                    if term.lower() in conclusion.lower():
                        # Check if NL context is also present
                        if "nederland" not in conclusion.lower():
                            findings.append(
                                OrchestratorFinding(
                                    error_type=LegalErrorType.JURISDICTION,
                                    severity=Severity.S3_MATERIEEL,
                                    description=f"Conclusie gebruikt EU-term '{term}' zonder NL-context",
                                    evidence=f"Primary jurisdiction: {primary_jurisdiction}",
                                    step="jurisdiction_check",
                                )
                            )
                        break

        return findings

    def _check_bias(self, assessment: dict) -> list[OrchestratorFinding]:
        """Check for bias in risk prioritization."""
        findings = []
        risks = assessment.get("risk_predictions", [])

        if not risks:
            return findings

        # Check if all risks have similar scores (no differentiation)
        scores = [r.get("risk_score", 0) for r in risks]
        if scores and max(scores) - min(scores) < 0.1 and len(scores) > 2:
            findings.append(
                OrchestratorFinding(
                    error_type=LegalErrorType.BIAS,
                    severity=Severity.S2_HERSTELBAAR,
                    description="Risico-scores zonder differentiatie — mogelijke bias",
                    evidence=f"Score range: {min(scores):.2f}-{max(scores):.2f}",
                    step="bias_check",
                )
            )

        return findings

    def _check_procedure(self, assessment: dict) -> list[OrchestratorFinding]:
        """Check procedural correctness."""
        findings = []

        # Check if human_review_required is set correctly
        human_review = assessment.get("human_review_required", None)
        confidence = assessment.get("confidence", 1.0)

        if human_review is None:
            findings.append(
                OrchestratorFinding(
                    error_type=LegalErrorType.PROCEDURAL,
                    severity=Severity.S3_MATERIEEL,
                    description="human_review_required veld ontbreekt",
                    evidence="Veld is None of niet aanwezig",
                    step="procedure_check",
                )
            )
        elif confidence < 0.85 and not human_review:
            findings.append(
                OrchestratorFinding(
                    error_type=LegalErrorType.PROCEDURAL,
                    severity=Severity.S4_RECHTSVERLIES,
                    description=f"Confidence {confidence:.2f} < 0.85 maar human_review_required=False",
                    evidence=f"Confidence: {confidence}, human_review: {human_review}",
                    step="procedure_check",
                )
            )

        return findings


# ─── Singleton ─────────────────────────────────────────────────

orchestrator_auditor = OrchestratorAuditor()
