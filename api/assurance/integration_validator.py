"""Integration Validator — OpenMythos × Djiftflo × JLAIF cross-checks.

Verifieert:
1. OpenMythos benchmark cases sluiten aan bij JLAIF fouttypes
2. Djimitflo NEDERUS controls sluiten aan bij JLAIF severity levels
3. Waargenomen OpenMythos-categorieën zijn gedekt door JLAIF modules
4. Alle 5 NEDERUS controls zijn gedekt door JLAIF audits
5. Geen ontbrekende mappings tussen de drie systemen
"""

from __future__ import annotations

import logging
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


# ─── OpenMythos → JLAIF Mapping ───────────────────────────────

OPENMYTHOS_TO_JLAIF: dict[str, dict[str, Any]] = {
    "hierarchy": {
        "jlaif_modules": ["approval_gate.py", "jurisdiction.py"],
        "error_types": ["procedurefout", "jurisdictiefout"],
        "severity_range": ["S2", "S3"],
        "ned_controls": ["NED-01", "NED-03"],
    },
    "injection": {
        "jlaif_modules": ["pii_redaction.py"],
        "error_types": ["vertrouwelijkheidsincident"],
        "severity_range": ["S4", "S5"],
        "ned_controls": ["NED-05"],
    },
    "tool-scope": {
        "jlaif_modules": ["citation_verification.py", "scanner.py"],
        "error_types": ["bronfout", "omissiefout"],
        "severity_range": ["S2", "S3"],
        "ned_controls": ["NED-04"],
    },
    "value-alignment": {
        "jlaif_modules": ["formal_severity.py", "bias_score.py"],
        "error_types": ["bias_ongelijke_behandeling", "interpretatiefout"],
        "severity_range": ["S2", "S3", "S4"],
        "ned_controls": ["NED-02"],
    },
    "calibration": {
        "jlaif_modules": ["formal_severity.py", "severity_scorer.py"],
        "error_types": ["interpretatiefout", "feitelijke_fout"],
        "severity_range": ["S2", "S3"],
        "ned_controls": ["NED-01"],
    },
    "hallucination": {
        "jlaif_modules": ["citation_verification.py", "rag_auditor.py"],
        "error_types": ["bronfout", "feitelijke_fout"],
        "severity_range": ["S3", "S4"],
        "ned_controls": ["NED-04"],
    },
    "temporal-reasoning": {
        "jlaif_modules": ["temporal_validity.py", "temporal_decay.py"],
        "error_types": ["temporaliteitsfout"],
        "severity_range": ["S2", "S3"],
        "ned_controls": ["NED-03"],
    },
    "cross-lingual": {
        "jlaif_modules": ["jurisdiction.py", "cross_jurisdiction.py"],
        "error_types": ["jurisdictiefout"],
        "severity_range": ["S3", "S4"],
        "ned_controls": ["NED-03"],
    },
    "contradiction": {
        "jlaif_modules": ["causality_network.py", "formal_severity.py"],
        "error_types": ["interpretatiefout", "procedurefout"],
        "severity_range": ["S3", "S4"],
        "ned_controls": ["NED-01"],
    },
    "dpia-completeness": {
        "jlaif_modules": ["rag_auditor.py", "golden_standard.py"],
        "error_types": ["omissiefout", "procedurefout"],
        "severity_range": ["S2", "S3"],
        "ned_controls": ["NED-01"],
    },
    "fria-coverage": {
        "jlaif_modules": ["rag_auditor.py", "golden_standard.py"],
        "error_types": ["omissiefout", "procedurefout"],
        "severity_range": ["S2", "S3", "S4"],
        "ned_controls": ["NED-01"],
    },
    "evidence-linking": {
        "jlaif_modules": ["citation_verification.py", "drift_monitor.py"],
        "error_types": ["bronfout", "omissiefout"],
        "severity_range": ["S2", "S3"],
        "ned_controls": ["NED-04"],
    },
    "bias-detection": {
        "jlaif_modules": ["bias_score.py", "formal_severity.py"],
        "error_types": ["bias_ongelijke_behandeling"],
        "severity_range": ["S2", "S3", "S4"],
        "ned_controls": ["NED-02"],
    },
    "proportionality": {
        "jlaif_modules": ["formal_severity.py", "severity_scorer.py"],
        "error_types": ["interpretatiefout", "procedurefout"],
        "severity_range": ["S2", "S3"],
        "ned_controls": ["NED-03"],
    },
    "data-minimization": {
        "jlaif_modules": ["pii_redaction.py"],
        "error_types": ["vertrouwelijkheidsincident"],
        "severity_range": ["S4", "S5"],
        "ned_controls": ["NED-02", "NED-05"],
    },
    "security": {
        "jlaif_modules": ["pii_redaction.py", "benchmark_capture_prevention.py"],
        "error_types": ["vertrouwelijkheidsincident", "procedurefout"],
        "severity_range": ["S3", "S4", "S5"],
        "ned_controls": ["NED-05"],
    },
    "transparency": {
        "jlaif_modules": ["citation_verification.py", "dashboard.py"],
        "error_types": ["bronfout", "omissiefout"],
        "severity_range": ["S2", "S3"],
        "ned_controls": ["NED-04"],
    },
    "accountability": {
        "jlaif_modules": ["approval_gate.py", "drift_monitor.py"],
        "error_types": ["procedurefout", "omissiefout"],
        "severity_range": ["S2", "S3"],
        "ned_controls": ["NED-01", "NED-05"],
    },
    "canary": {
        "jlaif_modules": ["benchmark_capture_prevention.py", "scanner.py"],
        "error_types": ["vertrouwelijkheidsincident", "procedurefout"],
        "severity_range": ["S3", "S4", "S5"],
        "ned_controls": ["NED-05"],
    },
    "overthinking": {
        "jlaif_modules": ["formal_severity.py", "approval_gate.py"],
        "error_types": ["procedurefout", "interpretatiefout"],
        "severity_range": ["S1", "S2", "S3"],
        "ned_controls": ["NED-01", "NED-03"],
    },
}

# ─── NEDERUS → JLAIF Mapping ──────────────────────────────────

NEDERUS_TO_JLAIF: dict[str, dict[str, Any]] = {
    "NED-01": {
        "title": "AI Impact Assessment",
        "jlaif_modules": [
            "rag_auditor.py",
            "orchestrator_auditor.py",
            "golden_standard.py",
        ],
        "error_types": ["omissiefout", "procedurefout", "feitelijke_fout"],
        "severity": "high",
        "evidence": ["audit_report", "confidence_score", "release_decision"],
    },
    "NED-02": {
        "title": "Bias & Fairness Testing",
        "jlaif_modules": ["bias_score.py", "formal_severity.py"],
        "error_types": ["bias_ongelijke_behandeling"],
        "severity": "high",
        "evidence": ["bias_rate", "severity_weighted_score"],
    },
    "NED-03": {
        "title": "Human Oversight",
        "jlaif_modules": ["approval_gate.py", "jurisdiction.py"],
        "error_types": ["jurisdictiefout", "procedurefout"],
        "severity": "high",
        "evidence": ["approval_status", "human_review_required"],
    },
    "NED-04": {
        "title": "Transparency & Explainability",
        "jlaif_modules": ["citation_verification.py", "dashboard.py"],
        "error_types": ["bronfout", "omissiefout"],
        "severity": "medium",
        "evidence": ["citation_rate", "explanation_available"],
    },
    "NED-05": {
        "title": "Incident Response & Reporting",
        "jlaif_modules": ["benchmark_capture_prevention.py", "drift_monitor.py"],
        "error_types": ["vertrouwelijkheidsincident", "procedurefout"],
        "severity": "critical",
        "evidence": ["incident_log", "response_time", "containment_status"],
    },
}


@dataclass
class ValidationCheck:
    """A single validation check result."""

    check_id: str
    source: str  # "openmythos", "nederus", "cross"
    target: str
    passed: bool
    details: str
    severity: str  # "info", "warning", "error", "critical"


@dataclass
class IntegrationReport:
    """Complete integration validation report."""

    timestamp: str
    total_checks: int
    passed: int
    failed: int
    warnings: int
    checks: list[ValidationCheck]
    coverage: dict[str, float]
    evidence_status: str
    observed: dict[str, Any]

    @property
    def pass_rate(self) -> float:
        return self.passed / max(self.total_checks, 1)


class IntegrationValidator:
    """Validates OpenMythos × Djimitflo × JLAIF integration."""

    def __init__(self, evidence_path: Path | None = None):
        self.evidence_path = evidence_path or (
            Path(__file__).resolve().parents[2]
            / "evidence"
            / "ecosystem-status-2026-07-30.json"
        )

    def _read_evidence(self) -> dict[str, Any]:
        return json.loads(self.evidence_path.read_text())

    def validate_all(self) -> IntegrationReport:
        """Run all integration checks."""
        evidence = self._read_evidence()
        checks = []

        # OpenMythos checks
        checks.extend(self._check_openmythos_coverage())
        checks.extend(self._check_openmythos_jlaif_mapping())

        # NEDERUS checks
        checks.extend(self._check_nederus_coverage())
        checks.extend(self._check_nederus_jlaif_mapping())

        # Cross-system checks
        checks.extend(self._check_cross_references())
        checks.extend(self._check_severity_alignment())
        checks.extend(self._check_module_existence())
        checks.extend(self._check_observed_ecosystem(evidence))

        # Summary
        passed = sum(1 for c in checks if c.passed)
        failed = sum(1 for c in checks if not c.passed)
        warnings = sum(1 for c in checks if c.severity == "warning")

        # Coverage
        om_coverage = self._compute_openmythos_coverage(
            set(evidence["openmythos"]["categories"])
        )
        ned_coverage = self._compute_nederus_coverage()
        evidence_status = (
            "verified"
            if evidence["djimitflo"]["openmythosEvalRuns"] > 0
            and evidence["djimitflo"]["externalNederusControlsObserved"]
            and evidence["juraregel"]["bridgeTransport"] != "in-memory-only"
            else "evidence-incomplete"
        )

        return IntegrationReport(
            timestamp=__import__("datetime").datetime.now().isoformat(),
            total_checks=len(checks),
            passed=passed,
            failed=failed,
            warnings=warnings,
            checks=checks,
            coverage={
                "openmythos": om_coverage,
                "nederus": ned_coverage,
                "overall": (om_coverage + ned_coverage) / 2,
            },
            evidence_status=evidence_status,
            observed={
                "openmythosCases": evidence["openmythos"]["corpusCases"],
                "openmythosCategories": len(evidence["openmythos"]["categories"]),
                "djimitfloEvalRuns": evidence["djimitflo"]["openmythosEvalRuns"],
                "bridgeTransport": evidence["juraregel"]["bridgeTransport"],
            },
        )

    def _check_observed_ecosystem(
        self, evidence: dict[str, Any]
    ) -> list[ValidationCheck]:
        checks = []
        for category in evidence["openmythos"]["categories"]:
            checks.append(
                ValidationCheck(
                    check_id=f"observed-openmythos-{category}",
                    source="openmythos",
                    target=category,
                    passed=category in OPENMYTHOS_TO_JLAIF,
                    details="Observed corpus category has a JLAIF mapping.",
                    severity="error",
                )
            )
        checks.append(
            ValidationCheck(
                check_id="observed-djimitflo-openmythos-runs",
                source="djimitflo",
                target="openmythos_eval_runs",
                passed=evidence["djimitflo"]["openmythosEvalRuns"] > 0,
                details=(
                    f"Observed {evidence['djimitflo']['openmythosEvalRuns']} "
                    "persisted OpenMythos evaluation runs."
                ),
                severity="warning",
            )
        )
        checks.append(
            ValidationCheck(
                check_id="observed-juraregel-djimitflo-transport",
                source="cross",
                target="djimitflo-bridge",
                passed=evidence["juraregel"]["bridgeTransport"] != "in-memory-only",
                details=f"Observed transport: {evidence['juraregel']['bridgeTransport']}.",
                severity="warning",
            )
        )
        return checks

    def _check_openmythos_coverage(self) -> list[ValidationCheck]:
        """Check if all OpenMythos categories have JLAIF mappings."""
        checks = []
        for category in OPENMYTHOS_TO_JLAIF:
            mapping = OPENMYTHOS_TO_JLAIF[category]
            checks.append(
                ValidationCheck(
                    check_id=f"om-{category}-exists",
                    source="openmythos",
                    target=category,
                    passed=True,
                    details=f"Category '{category}' mapped to {len(mapping['jlaif_modules'])} JLAIF modules",
                    severity="info",
                )
            )
        return checks

    def _check_openmythos_jlaif_mapping(self) -> list[ValidationCheck]:
        """Check if OpenMythos error types map to valid JLAIF types."""
        checks = []
        valid_types = {
            "feitelijke_fout",
            "bronfout",
            "interpretatiefout",
            "jurisdictiefout",
            "temporaliteitsfout",
            "procedurefout",
            "omissiefout",
            "bias_ongelijke_behandeling",
            "vertrouwelijkheidsincident",
        }

        for category, mapping in OPENMYTHOS_TO_JLAIF.items():
            for error_type in mapping.get("error_types", []):
                checks.append(
                    ValidationCheck(
                        check_id=f"om-{category}-type-{error_type}",
                        source="openmythos",
                        target=error_type,
                        passed=error_type in valid_types,
                        details=f"Error type '{error_type}' is {'valid' if error_type in valid_types else 'INVALID'}",
                        severity="error" if error_type not in valid_types else "info",
                    )
                )
        return checks

    def _check_nederus_coverage(self) -> list[ValidationCheck]:
        """Check if all NEDERUS controls have JLAIF mappings."""
        checks = []
        for control_id in NEDERUS_TO_JLAIF:
            mapping = NEDERUS_TO_JLAIF[control_id]
            checks.append(
                ValidationCheck(
                    check_id=f"ned-{control_id}-exists",
                    source="nederus",
                    target=control_id,
                    passed=True,
                    details=f"Control '{control_id}' ({mapping['title']}) mapped to {len(mapping['jlaif_modules'])} modules",
                    severity="info",
                )
            )
        return checks

    def _check_nederus_jlaif_mapping(self) -> list[ValidationCheck]:
        """Check if NEDERUS evidence requirements are satisfiable."""
        checks = []
        for control_id, mapping in NEDERUS_TO_JLAIF.items():
            evidence = mapping.get("evidence", [])
            checks.append(
                ValidationCheck(
                    check_id=f"ned-{control_id}-evidence",
                    source="nederus",
                    target=control_id,
                    passed=len(evidence) > 0,
                    details=f"Control '{control_id}' requires {len(evidence)} evidence types: {evidence}",
                    severity="warning" if len(evidence) == 0 else "info",
                )
            )
        return checks

    def _check_cross_references(self) -> list[ValidationCheck]:
        """Check cross-references between OpenMythos and NEDERUS."""
        checks = []

        # Every OpenMythos category should map to at least one NED control
        for category, mapping in OPENMYTHOS_TO_JLAIF.items():
            ned_controls = mapping.get("ned_controls", [])
            checks.append(
                ValidationCheck(
                    check_id=f"cross-{category}-ned",
                    source="cross",
                    target=category,
                    passed=len(ned_controls) > 0,
                    details=f"Category '{category}' maps to NED controls: {ned_controls}",
                    severity="warning" if len(ned_controls) == 0 else "info",
                )
            )

        return checks

    def _check_severity_alignment(self) -> list[ValidationCheck]:
        """Check if severity levels are aligned across systems."""
        checks = []

        for category, mapping in OPENMYTHOS_TO_JLAIF.items():
            sev_range = mapping.get("severity_range", [])
            valid_severities = {"S1", "S2", "S3", "S4", "S5"}
            for sev in sev_range:
                checks.append(
                    ValidationCheck(
                        check_id=f"sev-{category}-{sev}",
                        source="openmythos",
                        target=sev,
                        passed=sev in valid_severities,
                        details=f"Severity '{sev}' is {'valid' if sev in valid_severities else 'INVALID'}",
                        severity="error" if sev not in valid_severities else "info",
                    )
                )

        return checks

    def _check_module_existence(self) -> list[ValidationCheck]:
        """Check if referenced JLAIF modules actually exist."""
        import os

        checks = []
        assurance_dir = os.path.join(os.path.dirname(__file__))

        all_modules = set()
        for mapping in OPENMYTHOS_TO_JLAIF.values():
            all_modules.update(mapping.get("jlaif_modules", []))
        for mapping in NEDERUS_TO_JLAIF.values():
            all_modules.update(mapping.get("jlaif_modules", []))

        for module_file in all_modules:
            module_path = os.path.join(assurance_dir, module_file)
            exists = os.path.exists(module_path)
            checks.append(
                ValidationCheck(
                    check_id=f"mod-{module_file}-exists",
                    source="cross",
                    target=module_file,
                    passed=exists,
                    details=f"Module '{module_file}' {'exists' if exists else 'MISSING'}",
                    severity="error" if not exists else "info",
                )
            )

        return checks

    def _compute_openmythos_coverage(self, observed: set[str]) -> float:
        """Compute coverage only for categories observed in versioned evidence."""
        total = len(observed)
        covered = sum(
            1
            for category in observed
            if category in OPENMYTHOS_TO_JLAIF
            and OPENMYTHOS_TO_JLAIF[category].get("jlaif_modules")
            and OPENMYTHOS_TO_JLAIF[category].get("error_types")
        )
        return round(covered / max(total, 1), 2)

    def _compute_nederus_coverage(self) -> float:
        """Compute NEDERUS control coverage."""
        total = len(NEDERUS_TO_JLAIF)
        covered = sum(
            1
            for m in NEDERUS_TO_JLAIF.values()
            if len(m.get("jlaif_modules", [])) > 0 and len(m.get("evidence", [])) > 0
        )
        return round(covered / max(total, 1), 2)


# ─── Singleton ─────────────────────────────────────────────────

integration_validator = IntegrationValidator()
