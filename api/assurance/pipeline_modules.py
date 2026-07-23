"""Concrete JLAIF pipeline modules — implement the JLAIFModule protocol.

Each module wraps an existing assurance component into the pipeline interface.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from .pipeline import ModuleCategory, ModuleResult, PipelineState

logger = logging.getLogger(__name__)


@dataclass
class PIIRedactionModule:
    """PII detection and redaction module."""

    name: str = "pii-redaction"
    priority: int = 10
    category: ModuleCategory = ModuleCategory.PREPROCESSING
    critical: bool = False

    def execute(self, state: PipelineState) -> ModuleResult:
        from .pii_redaction import pii_redaction

        text = state.input_text
        result = pii_redaction.audit_only(text)

        state.add_result("pii_detections", result.detections)
        state.add_result("pii_density", result.pii_density)

        findings = []
        for detection in result.detections:
            severity = "S5" if detection.severity == "critical" else "S3"
            findings.append(
                {
                    "type": "vertrouwelijkheidsincident",
                    "severity": severity,
                    "description": f"PII gedetecteerd: {detection.description}",
                    "evidence": f"Type: {detection.pii_type}, Hash: {detection.original_hash}",
                    "module": self.name,
                }
            )

        if result.blocked:
            findings.append(
                {
                    "type": "vertrouwelijkheidsincident",
                    "severity": "S5",
                    "description": f"PII-densiteit {result.pii_density:.1f}% overschrijdt drempel",
                    "evidence": f"Densiteit: {result.pii_density:.1f}%, Drempel: 3.0%",
                    "module": self.name,
                }
            )

        return ModuleResult(
            module_name=self.name,
            category=self.category,
            success=True,
            findings=findings,
            metrics={
                "detections": len(result.detections),
                "density": result.pii_density,
            },
        )


@dataclass
class JurisdictionModule:
    """Jurisdiction classification module."""

    name: str = "jurisdiction-classifier"
    priority: int = 20
    category: ModuleCategory = ModuleCategory.PREPROCESSING
    critical: bool = False

    def execute(self, state: PipelineState) -> ModuleResult:
        from .jurisdiction import jurisdiction_classifier

        text = state.input_text
        expected = state.context.get("expected_jurisdiction", "")

        result = jurisdiction_classifier.classify(text)
        state.add_result("jurisdiction", result.primary)
        state.add_result("jurisdiction_confidence", result.confidence)

        findings = []

        # Check for jurisdiction warnings
        for warning in result.warnings:
            findings.append(
                {
                    "type": "jurisdictiefout",
                    "severity": "S3",
                    "description": warning,
                    "evidence": f"Primary: {result.primary}, Secondary: {result.secondary}",
                    "module": self.name,
                }
            )

        # Check consistency with expected jurisdiction
        if expected and result.primary != expected and result.primary != "unknown":
            findings.append(
                {
                    "type": "jurisdictiefout",
                    "severity": "S4",
                    "description": f"Jurisdictie-mismatch: verwacht '{expected}', gedetecteerd '{result.primary}'",
                    "evidence": f"Expected: {expected}, Detected: {result.primary}, Confidence: {result.confidence:.2f}",
                    "module": self.name,
                }
            )

        return ModuleResult(
            module_name=self.name,
            category=self.category,
            success=True,
            findings=findings,
            metrics={"primary": result.primary, "confidence": result.confidence},
        )


@dataclass
class CitationModule:
    """Citation verification module."""

    name: str = "citation-verification"
    priority: int = 30
    category: ModuleCategory = ModuleCategory.ANALYSIS
    critical: bool = False

    def execute(self, state: PipelineState) -> ModuleResult:
        from .citation_verification import citation_verifier

        text = state.input_text
        result = citation_verifier.verify(text)

        state.add_result("citation_rate", result.citation_rate)
        state.add_result("uncited_claims", result.uncited_claims)

        findings = []

        if result.citation_rate < 0.5 and result.total_claims > 0:
            findings.append(
                {
                    "type": "bronfout",
                    "severity": "S3",
                    "description": f"Lage citatie-rate: {result.citation_rate:.0%} ({result.uncited_claims} beweringen zonder bron)",
                    "evidence": f"Cited: {result.cited_claims}, Total: {result.total_claims}",
                    "module": self.name,
                }
            )

        return ModuleResult(
            module_name=self.name,
            category=self.category,
            success=True,
            findings=findings,
            metrics={
                "citation_rate": result.citation_rate,
                "uncited": result.uncited_claims,
            },
        )


@dataclass
class TemporalModule:
    """Temporal validity check module."""

    name: str = "temporal-validity"
    priority: int = 40
    category: ModuleCategory = ModuleCategory.ANALYSIS
    critical: bool = False

    def execute(self, state: PipelineState) -> ModuleResult:
        from .temporal_validity import temporal_checker

        text = state.input_text
        result = temporal_checker.check(text)

        state.add_result("outdated_count", result.outdated_count)

        findings = []
        for finding in result.findings:
            severity = "S3" if finding.severity == "high" else "S2"
            findings.append(
                {
                    "type": "temporaliteitsfout",
                    "severity": severity,
                    "description": finding.description,
                    "evidence": f"Old: {finding.old_reference}, New: {finding.new_reference}",
                    "module": self.name,
                }
            )

        return ModuleResult(
            module_name=self.name,
            category=self.category,
            success=True,
            findings=findings,
            metrics={"outdated": result.outdated_count},
        )


@dataclass
class SeverityScoringModule:
    """Severity-weighted scoring module."""

    name: str = "severity-scoring"
    priority: int = 50
    category: ModuleCategory = ModuleCategory.SCORING
    critical: bool = False

    def execute(self, state: PipelineState) -> ModuleResult:
        from .error_taxonomy import LegalError, Severity, SeverityDistribution

        # Collect all findings from previous modules
        all_findings = state.findings

        distribution = SeverityDistribution()
        for finding in all_findings:
            sev_map = {
                "S1": Severity.S1_COSMETISCH,
                "S2": Severity.S2_HERSTELBAAR,
                "S3": Severity.S3_MATERIEEL,
                "S4": Severity.S4_RECHTSVERLIES,
                "S5": Severity.S5_SYSTEEMISCH,
            }
            sev = sev_map.get(finding.get("severity", "S1"), Severity.S1_COSMETISCH)
            distribution.add(
                LegalError(
                    error_type=finding.get("type", "feitelijke_fout"),
                    severity=sev,
                    description=finding.get("description", ""),
                )
            )

        state.add_result("severity_distribution", distribution.to_dict())
        state.add_result("weighted_score", distribution.weighted_score)
        state.add_result("has_blocking", distribution.has_blocking_errors)

        findings = []
        if distribution.has_blocking_errors:
            findings.append(
                {
                    "type": "procedurefout",
                    "severity": "S4",
                    "description": f"Blokkerende fouten gedetecteerd (gewogen score: {distribution.weighted_score:.1f})",
                    "evidence": str(distribution.counts),
                    "module": self.name,
                }
            )

        return ModuleResult(
            module_name=self.name,
            category=self.category,
            success=True,
            findings=findings,
            metrics={
                "weighted_score": distribution.weighted_score,
                "total_findings": distribution.total_errors,
                "has_blocking": distribution.has_blocking_errors,
            },
        )


@dataclass
class ReleaseGateModule:
    """Final release gate decision module."""

    name: str = "release-gate"
    priority: int = 60
    category: ModuleCategory = ModuleCategory.POSTPROCESSING
    critical: bool = True

    def execute(self, state: PipelineState) -> ModuleResult:
        from .release_gate import evaluate_release
        from .severity_scorer import UseCaseProfile

        # Build use case from context
        uc = UseCaseProfile(
            name=state.context.get("product_name", "pipeline"),
            autonomy_level=state.context.get("autonomy_level", 2),
            legal_domain=state.context.get("legal_domain", "algemeen"),
            user_group=state.context.get("user_group", "advocaat"),
        )

        # Collect errors from state
        from .error_taxonomy import LegalError, Severity, LegalErrorType

        errors = []
        for finding in state.findings:
            sev_map = {
                "S1": Severity.S1_COSMETISCH,
                "S2": Severity.S2_HERSTELBAAR,
                "S3": Severity.S3_MATERIEEL,
                "S4": Severity.S4_RECHTSVERLIES,
                "S5": Severity.S5_SYSTEEMISCH,
            }
            sev = sev_map.get(finding.get("severity", "S1"), Severity.S1_COSMETISCH)
            errors.append(
                LegalError(
                    error_type=LegalErrorType(finding.get("type", "feitelijke_fout")),
                    severity=sev,
                    description=finding.get("description", ""),
                )
            )

        decision = evaluate_release(errors, uc)
        state.add_result("release_decision", decision.verdict)
        state.add_result("release_reason", decision.reason)

        findings = []
        if decision.verdict != "GO":
            findings.append(
                {
                    "type": "procedurefout",
                    "severity": "S3" if decision.verdict == "CONDITIONAL" else "S4",
                    "description": f"Release gate: {decision.verdict} — {decision.reason}",
                    "evidence": str(decision.details),
                    "module": self.name,
                }
            )

        return ModuleResult(
            module_name=self.name,
            category=self.category,
            success=True,
            findings=findings,
            metrics={"decision": decision.verdict},
        )
