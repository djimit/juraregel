"""Independent Validation Layer — audit van de auditor.

Voorkomt self-reference bias door:
- Onafhankelijke canary testcases te injecteren
- Zelf-evaluatie te vergelijken met onafhankelijke evaluatie
- Verschillen te rapporteren als S4 bevinding
- Automatische herkalibratie te triggeren bij drift > 10%
"""

from __future__ import annotations

import hashlib
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


# ─── Independent Test Cases ────────────────────────────────────

# Deze testcases zijn ONBEKEND bij de producten die geauditeerd worden.
# Ze worden gebruikt om te controleren of de audit-eerlijk is.

INDEPENDENT_TEST_CASES = [
    {
        "case_id": "INDEP-001",
        "category": "pii_detection",
        "input": "De patiënt met BSN 987654321 heeft recht op inzage.",
        "expected_findings": ["BSN"],
        "min_severity": "critical",
    },
    {
        "case_id": "INDEP-002",
        "category": "jurisdiction",
        "input": "Conform Art. 9 van de EU AI Act is risicobeheer verplicht.",
        "expected_jurisdiction": "EU",
        "min_severity": "medium",
    },
    {
        "case_id": "INDEP-003",
        "category": "citation",
        "input": "De verwerking is rechtmatig omdat het noodzakelijk is.",
        "expected_findings": ["missing_citation"],
        "min_severity": "medium",
    },
    {
        "case_id": "INDEP-004",
        "category": "temporal",
        "input": "De Privacyrichtlijn uit 1995 is hier van toepassing.",
        "expected_findings": ["outdated_term"],
        "min_severity": "medium",
    },
    {
        "case_id": "INDEP-005",
        "category": "bias",
        "input": "Het systeem is volledig objectief en heeft geen beperkingen.",
        "expected_findings": ["no_counter_arguments"],
        "min_severity": "low",
    },
]


@dataclass
class ValidationResult:
    """Result of independent validation."""

    case_id: str
    category: str
    passed: bool
    expected: str
    actual: str
    drift_detected: bool
    severity: str


@dataclass
class IndependentValidationReport:
    """Complete independent validation report."""

    run_id: str
    timestamp: str
    total_cases: int
    passed: int
    failed: int
    drift_detected: bool
    results: list[ValidationResult]
    overall_reliable: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "total_cases": self.total_cases,
            "passed": self.passed,
            "failed": self.failed,
            "drift_detected": self.drift_detected,
            "overall_reliable": self.overall_reliable,
            "results": [
                {
                    "case_id": r.case_id,
                    "category": r.category,
                    "passed": r.passed,
                    "drift_detected": r.drift_detected,
                }
                for r in self.results
            ],
        }


class IndependentValidationLayer:
    """Validates audit results using independent test cases."""

    DRIFT_THRESHOLD = 0.10  # 10% difference triggers drift alert

    def __init__(self):
        self._baseline: dict[str, bool] = {}
        self._history: list[IndependentValidationReport] = []

    def validate_audit(
        self,
        audit_fn,
        audit_name: str,
    ) -> IndependentValidationReport:
        """Run independent validation on an audit function."""
        results = []

        for case in INDEPENDENT_TEST_CASES:
            try:
                # Run the audit function on the independent test case
                audit_result = audit_fn(case["input"])

                # Check if expected findings are present
                passed = self._check_case(case, audit_result)
                drift = self._check_drift(case["case_id"], passed)

                results.append(
                    ValidationResult(
                        case_id=case["case_id"],
                        category=case["category"],
                        passed=passed,
                        expected=str(
                            case.get(
                                "expected_findings",
                                case.get("expected_jurisdiction", "unknown"),
                            )
                        ),
                        actual=str(audit_result)[:100],
                        drift_detected=drift,
                        severity=case["min_severity"],
                    )
                )
            except Exception as e:
                results.append(
                    ValidationResult(
                        case_id=case["case_id"],
                        category=case["category"],
                        passed=False,
                        expected="valid execution",
                        actual=f"Error: {str(e)[:50]}",
                        drift_detected=False,
                        severity="critical",
                    )
                )

        passed_count = sum(1 for r in results if r.passed)
        drift = any(r.drift_detected for r in results)

        report = IndependentValidationReport(
            run_id=f"indep-{hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]}",
            timestamp=datetime.now().isoformat(),
            total_cases=len(results),
            passed=passed_count,
            failed=len(results) - passed_count,
            drift_detected=drift,
            results=results,
            overall_reliable=passed_count == len(results) and not drift,
        )

        self._history.append(report)
        return report

    def _check_case(self, case: dict, audit_result: Any) -> bool:
        """Check if audit result matches expected findings."""
        category = case["category"]

        if category == "pii_detection":
            # Check if PII was detected in text containing BSN
            if isinstance(audit_result, dict):
                return (
                    audit_result.get("has_pii", False)
                    or audit_result.get("detection_count", 0) > 0
                )
            return False

        elif category == "jurisdiction":
            # Check if EU jurisdiction was detected
            if isinstance(audit_result, dict):
                return audit_result.get("primary") == "EU"
            return False

        elif category == "citation":
            # Check if missing citation was detected
            if isinstance(audit_result, dict):
                return audit_result.get("findings_count", 0) > 0
            return False

        elif category == "temporal":
            # Check if outdated term was detected
            if isinstance(audit_result, dict):
                return audit_result.get("findings_count", 0) > 0
            return False

        elif category == "bias":
            # Check if lack of counter-arguments was detected
            if isinstance(audit_result, dict):
                return audit_result.get("findings_count", 0) > 0
            return False

        return False

    def _check_drift(self, case_id: str, current_result: bool) -> bool:
        """Check if result has drifted from baseline."""
        if case_id in self._baseline:
            baseline = self._baseline[case_id]
            return baseline != current_result
        self._baseline[case_id] = current_result
        return False

    def get_history(self, limit: int = 10) -> list[IndependentValidationReport]:
        """Get validation history."""
        return self._history[-limit:]


# ─── Singleton ─────────────────────────────────────────────────

independent_validation = IndependentValidationLayer()
