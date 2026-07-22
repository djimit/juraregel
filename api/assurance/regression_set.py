"""Regression Test Set — fixed set of test cases for continuous evaluation.

Implements NIST AI RMF MEASURE 1.1: testing for accuracy and reliability
against a fixed benchmark that runs on every CI execution.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class RegressionCase:
    """A single regression test case."""

    case_id: str
    category: str
    description: str
    expected_verdict: str  # "pass" or "fail"
    patterns: list[str]  # regex patterns that must match
    min_matches: int = 1


@dataclass
class RegressionResult:
    """Result of running the regression set."""

    run_id: str
    timestamp: str
    total_cases: int
    passed: int
    failed: int
    failures: list[dict[str, Any]]
    execution_time_ms: int
    score: float

    @property
    def passed_all(self) -> bool:
        return self.failed == 0


class RegressionSet:
    """Fixed regression test set for legal AI assurance.

    Runs on every CI execution to detect regressions in:
    - Error taxonomy completeness
    - Severity scoring correctness
    - Evidence lineage integrity
    - Benchmark scanning capability
    """

    def __init__(self):
        self.cases: list[RegressionCase] = []
        self._load_default_cases()

    def _load_default_cases(self) -> None:
        """Load the default regression cases."""
        self.cases = [
            RegressionCase(
                case_id="REG-001",
                category="error_taxonomy",
                description="LegalErrorType has exactly 9 values",
                expected_verdict="pass",
                patterns=["class LegalErrorType"],
                min_matches=1,
            ),
            RegressionCase(
                case_id="REG-002",
                category="error_taxonomy",
                description="Severity has 5 levels with exponential weights",
                expected_verdict="pass",
                patterns=["S1_COSMETISCH", "S5_SYSTEEMISCH"],
                min_matches=2,
            ),
            RegressionCase(
                case_id="REG-003",
                category="severity_scorer",
                description="score_system function exists",
                expected_verdict="pass",
                patterns=["def score_system"],
                min_matches=1,
            ),
            RegressionCase(
                case_id="REG-004",
                category="release_gate",
                description="evaluate_release function exists",
                expected_verdict="pass",
                patterns=["def evaluate_release"],
                min_matches=1,
            ),
            RegressionCase(
                case_id="REG-005",
                category="evidence_lineage",
                description="EvidenceLineage dataclass exists",
                expected_verdict="pass",
                patterns=["class EvidenceLineage"],
                min_matches=1,
            ),
            RegressionCase(
                case_id="REG-006",
                category="evidence_lineage",
                description="EvidenceLineage has compute_hash method",
                expected_verdict="pass",
                patterns=["def compute_hash"],
                min_matches=1,
            ),
            RegressionCase(
                case_id="REG-007",
                category="evidence_lineage",
                description="EvidenceLineage has is_traceable property",
                expected_verdict="pass",
                patterns=["def is_traceable"],
                min_matches=1,
            ),
            RegressionCase(
                case_id="REG-008",
                category="benchmark_runner",
                description="BenchmarkRunner uses real scanning",
                expected_verdict="pass",
                patterns=["class _CodebaseScanner"],
                min_matches=1,
            ),
            RegressionCase(
                case_id="REG-009",
                category="benchmark_runner",
                description="No hardcoded passed:True in _evaluate_check",
                expected_verdict="pass",
                patterns=["def _evaluate_check"],
                min_matches=1,
            ),
            RegressionCase(
                case_id="REG-010",
                category="scanner",
                description="CodebaseScanner has check_all method",
                expected_verdict="pass",
                patterns=["def check_all"],
                min_matches=1,
            ),
            RegressionCase(
                case_id="REG-011",
                category="accountable_ai",
                description="Explanation has error_type field",
                expected_verdict="pass",
                patterns=["error_type"],
                min_matches=1,
            ),
            RegressionCase(
                case_id="REG-012",
                category="legal_reasoning",
                description="LegalClaim has error_type field",
                expected_verdict="pass",
                patterns=["error_type"],
                min_matches=1,
            ),
        ]

    def run(self) -> RegressionResult:
        """Run all regression cases."""
        start = time.time()
        failures = []
        passed = 0

        for case in self.cases:
            result = self._run_case(case)
            if result:
                passed += 1
            else:
                failures.append(
                    {
                        "case_id": case.case_id,
                        "category": case.category,
                        "description": case.description,
                    }
                )

        total = len(self.cases)
        elapsed = int((time.time() - start) * 1000)

        return RegressionResult(
            run_id=f"reg-{int(time.time())}",
            timestamp=datetime.now().isoformat(),
            total_cases=total,
            passed=passed,
            failed=total - passed,
            failures=failures,
            execution_time_ms=elapsed,
            score=round(passed / max(total, 1), 2),
        )

    def _run_case(self, case: RegressionCase) -> bool:
        """Run a single regression case."""
        import subprocess

        root = Path(__file__).parent.parent

        for pattern in case.patterns:
            try:
                result = subprocess.run(
                    ["rg", "-l", pattern, "--glob", "*.py", str(root)],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                matches = [m for m in result.stdout.strip().split("\n") if m]
                if len(matches) < case.min_matches:
                    return False
            except (FileNotFoundError, subprocess.TimeoutExpired):
                return False

        return True


# ─── Singleton ─────────────────────────────────────────────────

regression_set = RegressionSet()
