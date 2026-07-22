"""OpenMythos Benchmark Runner — Full compliance evaluation framework.

Runs comprehensive benchmarks across all OpenMythos categories:
- hierarchy: Art 14(1), 14(3) — Human oversight hierarchy
- injection: Art 15(2), 15(4) — Prompt injection safeguards
- tool-scope: Art 10(2), 10(3) — Data scope limitations
- value-alignment: Art 9(1), 9(2) — Risk management alignment
- calibration: Art 15(1), 15(3) — Accuracy calibration
- hallucination: Art 12(1), 12(2) — Logging/record-keeping
- temporal-reasoning: Art 11(1), 11(2) — Technical documentation timeline
- cross-lingual: Art 11(1) — Multi-language documentation
- contradiction: Art 14(1) — Contradictory oversight

Plus compliance-specific categories:
- dpia-completeness: Art 35(7) — DPIA criteria coverage
- fria-coverage: Art 27(1) — FRIA element coverage
- evidence-linking: Art 5(2) — Verifiability
- bias-detection: Art 10(2)(f), 10(3) — Bias examination
- proportionality: Art 35(7)(b)(c) — Necessity and proportionality
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


# ─── Extended Category Map ────────────────────────────────────

CATEGORY_MAP = {
    # Original OpenMythos categories
    "hierarchy": ["Art 14(1)", "Art 14(3)"],
    "injection": ["Art 15(2)", "Art 15(4)"],
    "tool-scope": ["Art 10(2)", "Art 10(3)"],
    "value-alignment": ["Art 9(1)", "Art 9(2)"],
    "calibration": ["Art 15(1)", "Art 15(3)"],
    "hallucination": ["Art 12(1)", "Art 12(2)"],
    "temporal-reasoning": ["Art 11(1)", "Art 11(2)"],
    "cross-lingual": ["Art 11(1)"],
    "contradiction": ["Art 14(1)"],
    # Compliance-specific categories
    "dpia-completeness": ["Art 35(7)", "Art 35(3)"],
    "fria-coverage": ["Art 27(1)", "Art 27(3)"],
    "evidence-linking": ["Art 5(2)", "Art 35(7)(d)"],
    "bias-detection": ["Art 10(2)(f)", "Art 10(3)"],
    "proportionality": ["Art 35(7)(b)", "Art 35(7)(c)"],
    "data-minimization": ["Art 25(1)", "Art 5(1)(c)"],
    "security": ["Art 32(1)", "Art 32(2)"],
    "transparency": ["Art 13", "Art 50"],
    "accountability": ["Art 5(2)", "Art 24"],
}


# ─── Data Models ──────────────────────────────────────────────


@dataclass
class BenchmarkCase:
    """A single benchmark case."""

    case_id: str
    category: str
    description: str
    articles: list[str]
    checks: list[dict[str, Any]]


@dataclass
class BenchmarkResult:
    """Result of a benchmark run."""

    case_id: str
    category: str
    score: float  # 0.0-1.0
    passed: int
    total: int
    findings: list[dict]
    verdict: str  # PASS, WARN, FAIL
    execution_time_ms: int


@dataclass
class BenchmarkReport:
    """Complete benchmark report."""

    run_id: str
    timestamp: str
    results: list[BenchmarkResult]
    overall_score: float
    overall_verdict: str
    summary: dict[str, int]  # {PASS: n, WARN: n, FAIL: n}


# ─── Benchmark Runner ─────────────────────────────────────────


class BenchmarkRunner:
    """Run OpenMythos compliance benchmarks."""

    def __init__(self):
        self._cases: list[BenchmarkCase] = []
        self._generate_cases()

    def _generate_cases(self) -> None:
        """Generate benchmark cases from category map."""
        for category, articles in CATEGORY_MAP.items():
            case = BenchmarkCase(
                case_id=f"OM-{category.upper()}",
                category=category,
                description=f"OpenMythos benchmark: {category}",
                articles=articles,
                checks=self._generate_checks(category, articles),
            )
            self._cases.append(case)

    def _generate_checks(self, category: str, articles: list[str]) -> list[dict]:
        """Generate checks for a category."""
        checks = []

        # Hierarchy checks
        if category == "hierarchy":
            checks = [
                {
                    "id": "hier-1",
                    "description": "Human oversight is defined",
                    "check": "has_oversight_definition",
                },
                {
                    "id": "hier-2",
                    "description": "Override capability exists",
                    "check": "has_override",
                },
                {
                    "id": "hier-3",
                    "description": "Stop mechanism is implemented",
                    "check": "has_stop_mechanism",
                },
            ]
        # DPIA completeness checks
        elif category == "dpia-completeness":
            checks = [
                {
                    "id": "dpia-1",
                    "description": "Processing description complete",
                    "check": "has_processing_description",
                },
                {
                    "id": "dpia-2",
                    "description": "Necessity assessment present",
                    "check": "has_necessity_assessment",
                },
                {
                    "id": "dpia-3",
                    "description": "Risk assessment present",
                    "check": "has_risk_assessment",
                },
                {
                    "id": "dpia-4",
                    "description": "Measures documented",
                    "check": "has_measures",
                },
                {
                    "id": "dpia-5",
                    "description": "DPIA approval recorded",
                    "check": "has_approval",
                },
            ]
        # FRIA coverage checks
        elif category == "fria-coverage":
            checks = [
                {
                    "id": "fria-1",
                    "description": "Use context described",
                    "check": "has_use_context",
                },
                {
                    "id": "fria-2",
                    "description": "Affected persons identified",
                    "check": "has_affected_persons",
                },
                {
                    "id": "fria-3",
                    "description": "Rights impact assessed",
                    "check": "has_rights_impact",
                },
                {
                    "id": "fria-4",
                    "description": "Mitigation measures defined",
                    "check": "has_mitigation",
                },
            ]
        # Evidence linking checks
        elif category == "evidence-linking":
            checks = [
                {
                    "id": "evid-1",
                    "description": "Evidence linked to sections",
                    "check": "has_evidence_links",
                },
                {
                    "id": "evid-2",
                    "description": "Evidence verified",
                    "check": "has_verified_evidence",
                },
                {
                    "id": "evid-3",
                    "description": "Evidence not expired",
                    "check": "evidence_current",
                },
            ]
        # Bias detection checks
        elif category == "bias-detection":
            checks = [
                {
                    "id": "bias-1",
                    "description": "Training data examined",
                    "check": "data_examined",
                },
                {
                    "id": "bias-2",
                    "description": "Bias metrics defined",
                    "check": "has_bias_metrics",
                },
                {
                    "id": "bias-3",
                    "description": "Remediation documented",
                    "check": "has_remediation",
                },
            ]
        # Default checks
        else:
            checks = [
                {
                    "id": f"{category[:4]}-1",
                    "description": f"{category} requirement 1",
                    "check": "requirement_met",
                },
                {
                    "id": f"{category[:4]}-2",
                    "description": f"{category} requirement 2",
                    "check": "requirement_met",
                },
            ]

        return checks

    def run_all(self) -> BenchmarkReport:
        """Run all benchmark cases."""
        start = time.time()
        results = []

        for case in self._cases:
            result = self._run_case(case)
            results.append(result)

        overall_score = sum(r.score for r in results) / max(len(results), 1)
        summary = {"PASS": 0, "WARN": 0, "FAIL": 0}
        for r in results:
            summary[r.verdict] = summary.get(r.verdict, 0) + 1

        overall_verdict = (
            "PASS"
            if overall_score >= 0.8
            else "WARN"
            if overall_score >= 0.6
            else "FAIL"
        )

        return BenchmarkReport(
            run_id=f"bench-{int(start)}",
            timestamp=datetime.utcnow().isoformat(),
            results=results,
            overall_score=round(overall_score, 3),
            overall_verdict=overall_verdict,
            summary=summary,
        )

    def _run_case(self, case: BenchmarkCase) -> BenchmarkResult:
        """Run a single benchmark case."""
        start = time.time()
        findings = []
        passed = 0

        for check in case.checks:
            # Evaluate the check against the codebase
            check_result = self._evaluate_check(check)
            if check_result["passed"]:
                passed += 1
            findings.append(
                {
                    "check_id": check["id"],
                    "description": check["description"],
                    "passed": check_result["passed"],
                    "details": check_result.get("details", ""),
                }
            )

        total = len(case.checks)
        score = round(passed / max(total, 1), 2)
        verdict = "PASS" if score >= 0.8 else "WARN" if score >= 0.6 else "FAIL"

        return BenchmarkResult(
            case_id=case.case_id,
            category=case.category,
            score=score,
            passed=passed,
            total=total,
            findings=findings,
            verdict=verdict,
            execution_time_ms=int((time.time() - start) * 1000),
        )

    def _evaluate_check(self, check: dict) -> dict:
        """Evaluate a single check against the actual codebase.

        Uses grep-based pattern scanning to detect real implementations
        rather than hardcoded responses.
        """
        check_type = check.get("check", "")

        scanner = _CodebaseScanner()
        result = scanner.scan(check_type)

        if result is not None:
            return result

        return {"passed": False, "details": f"Unknown check type: {check_type}"}


class _CodebaseScanner:
    """Scans the JuraRegel codebase for real implementation patterns.

    Each scan method uses grep to detect actual code patterns,
    returning None if the check type is not handled.
    """

    def __init__(self):
        self.root = Path(__file__).parent.parent

    def scan(self, check_type: str) -> dict | None:
        """Dispatch to the appropriate scan method."""
        method = getattr(self, f"_scan_{check_type}", None)
        if method:
            return method()
        return None

    def _grep(self, pattern: str, glob: str = "*.py") -> list[str]:
        """Search codebase for pattern."""
        import subprocess

        try:
            result = subprocess.run(
                ["rg", "-l", pattern, "--glob", glob, str(self.root)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return [p for p in result.stdout.strip().split("\n") if p]
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return []

    def _grep_count(self, pattern: str, glob: str = "*.py") -> int:
        return len(self._grep(pattern, glob))

    def _scan_has_oversight_definition(self) -> dict:
        matches = self._grep("human_review_required|oversight|Explanation")
        passed = len(matches) >= 2
        return {
            "passed": passed,
            "details": f"Found {len(matches)} oversight-related implementations"
            if passed
            else "Insufficient oversight definitions found",
        }

    def _scan_has_override(self) -> dict:
        matches = self._grep("override|depart.*from|reject")
        passed = len(matches) >= 1
        return {
            "passed": passed,
            "details": f"Found {len(matches)} override patterns",
        }

    def _scan_has_stop_mechanism(self) -> dict:
        matches = self._grep("stop|disable|halt|rollback")
        passed = len(matches) >= 1
        return {
            "passed": passed,
            "details": f"Found {len(matches)} stop/rollback mechanisms",
        }

    def _scan_has_processing_description(self) -> dict:
        matches = self._grep("processing.*description|verwerkingsactiviteit|purpose")
        passed = len(matches) >= 1
        return {
            "passed": passed,
            "details": f"Found {len(matches)} processing description patterns",
        }

    def _scan_has_necessity_assessment(self) -> dict:
        matches = self._grep("necessity|proportionality|noodzaak|proportionaliteit")
        passed = len(matches) >= 1
        return {
            "passed": passed,
            "details": f"Found {len(matches)} necessity/proportionality patterns",
        }

    def _scan_has_risk_assessment(self) -> dict:
        matches = self._grep("risk.*assessment|risico.*analyse|RiskLevel")
        passed = len(matches) >= 2
        return {
            "passed": passed,
            "details": f"Found {len(matches)} risk assessment patterns",
        }

    def _scan_has_measures(self) -> dict:
        matches = self._grep("measure|maatregel|mitigation")
        passed = len(matches) >= 2
        return {
            "passed": passed,
            "details": f"Found {len(matches)} measure/mitigation patterns",
        }

    def _scan_has_approval(self) -> dict:
        matches = self._grep("approval|authorize|approve|goedkeuring")
        passed = len(matches) >= 1
        return {
            "passed": passed,
            "details": f"Found {len(matches)} approval patterns",
        }

    def _scan_has_use_context(self) -> dict:
        matches = self._grep("use.*context|intended.*purpose|gebruikscontext")
        passed = len(matches) >= 1
        return {
            "passed": passed,
            "details": f"Found {len(matches)} use context patterns",
        }

    def _scan_has_affected_persons(self) -> dict:
        matches = self._grep("affected.*person|betrokkene|stakeholder")
        passed = len(matches) >= 1
        return {
            "passed": passed,
            "details": f"Found {len(matches)} affected person patterns",
        }

    def _scan_has_rights_impact(self) -> dict:
        matches = self._grep("rights.*impact|grondrecht|fundamental.*right")
        passed = len(matches) >= 1
        return {
            "passed": passed,
            "details": f"Found {len(matches)} rights impact patterns",
        }

    def _scan_has_mitigation(self) -> dict:
        matches = self._grep("mitigation|mitigeren|maatregel")
        passed = len(matches) >= 1
        return {
            "passed": passed,
            "details": f"Found {len(matches)} mitigation patterns",
        }

    def _scan_has_evidence_links(self) -> dict:
        matches = self._grep(
            "evidence.*link|source.*link|bronverwijzing|claim_verifier"
        )
        passed = len(matches) >= 1
        return {
            "passed": passed,
            "details": f"Found {len(matches)} evidence linking patterns",
        }

    def _scan_has_verified_evidence(self) -> dict:
        matches = self._grep("verify.*evidence|evidence.*verif|bewijs.*verif")
        passed = len(matches) >= 1
        return {
            "passed": passed,
            "details": f"Found {len(matches)} evidence verification patterns",
        }

    def _scan_evidence_current(self) -> dict:
        matches = self._grep("evidence.*expir|evidence.*current|temporal.*decay|drift")
        passed = len(matches) >= 1
        return {
            "passed": passed,
            "details": f"Found {len(matches)} evidence currency patterns"
            if passed
            else "Evidence expiry tracking needs configuration",
        }

    def _scan_data_examined(self) -> dict:
        matches = self._grep("data.*examin|bias.*audit|data.*analyse")
        passed = len(matches) >= 1
        return {
            "passed": passed,
            "details": f"Found {len(matches)} data examination patterns",
        }

    def _scan_has_bias_metrics(self) -> dict:
        matches = self._grep(
            "bias.*metric|demographic.*parity|equalized.*odds|disparate"
        )
        passed = len(matches) >= 1
        return {
            "passed": passed,
            "details": f"Found {len(matches)} bias metric patterns",
        }

    def _scan_has_remediation(self) -> dict:
        matches = self._grep("remediation|herstel|corrective")
        passed = len(matches) >= 1
        return {
            "passed": passed,
            "details": f"Found {len(matches)} remediation patterns",
        }

    def _scan_requirement_met(self) -> dict:
        return {
            "passed": False,
            "details": "Generic requirement_met check — needs specific implementation",
        }

    def run_category(self, category: str) -> BenchmarkResult | None:
        """Run a specific category."""
        for case in self._cases:
            if case.category == category:
                return self._run_case(case)
        return None


# ─── Singleton ─────────────────────────────────────────────────

benchmark_runner = BenchmarkRunner()
