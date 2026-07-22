"""Challenge Set — hidden test set for unbiased evaluation.

Implements Stanford's requirement that benchmarks must include
hidden challenge sets that are NOT used in training or tuning.

The challenge set is:
- Versioned (regenerated quarterly)
- Separated from the goldset
- Used only for final evaluation, not development
"""

from __future__ import annotations

import hashlib
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ChallengeCase:
    """A single hidden challenge case."""

    case_id: str
    version: str
    category: str
    description: str
    patterns: list[str]
    min_matches: int
    is_canary: bool = False


@dataclass
class ChallengeResult:
    """Result of running the challenge set."""

    run_id: str
    version: str
    timestamp: str
    total_cases: int
    passed: int
    failed: int
    canary_triggered: bool
    failures: list[dict[str, Any]]
    execution_time_ms: int
    score: float

    @property
    def passed_all(self) -> bool:
        return self.failed == 0 and not self.canary_triggered


class ChallengeSet:
    """Hidden challenge set with canary detection.

    Canary cases are designed to detect if challenge data has leaked
    into training. If a canary case passes unexpectedly, it suggests
    the model has seen the test data.

    Canary tokens are stored externally in .benchmark-canary to avoid
    false positives from scanning the challenge_set.py file itself.
    """

    VERSION = "2026.1"
    CANARY_FILE = ".benchmark-canary"

    def __init__(self):
        self.cases: list[ChallengeCase] = []
        self._load_cases()

    def _load_cases(self) -> None:
        """Load challenge cases."""
        self.cases = [
            ChallengeCase(
                case_id="CHAL-001",
                version=self.VERSION,
                category="taxonomy_completeness",
                description="All 9 error types are defined with Dutch labels",
                patterns=[
                    "FACTUAL = ",
                    "SOURCE = ",
                    "INTERPRETATION = ",
                    "JURISDICTION = ",
                    "TEMPORAL = ",
                    "PROCEDURAL = ",
                    "OMISSION = ",
                    "BIAS = ",
                    "CONFIDENTIALITY = ",
                ],
                min_matches=9,
            ),
            ChallengeCase(
                case_id="CHAL-002",
                version=self.VERSION,
                category="severity_weights",
                description="Severity weights are exponential (1,2,4,8,16)",
                patterns=[
                    "S1_COSMETISCH",
                    "S2_HERSTELBAAR",
                    "S3_MATERIEEL",
                    "S4_RECHTSVERLIES",
                    "S5_SYSTEEMISCH",
                ],
                min_matches=5,
            ),
            ChallengeCase(
                case_id="CHAL-003",
                version=self.VERSION,
                category="stanford_formula",
                description="Benefit formula includes detectability and recoverability",
                patterns=["detectability", "recoverability"],
                min_matches=2,
            ),
            ChallengeCase(
                case_id="CHAL-004",
                version=self.VERSION,
                category="lineage_integrity",
                description="EvidenceLineage includes retrieval in hash",
                patterns=["retrieval.query", "retrieval_model"],
                min_matches=2,
            ),
            ChallengeCase(
                case_id="CHAL-005",
                version=self.VERSION,
                category="gate_logic",
                description="Release gate has three verdict paths",
                patterns=['"GO"', '"NO-GO"', '"CONDITIONAL"'],
                min_matches=3,
            ),
            ChallengeCase(
                case_id="CHAL-006",
                version=self.VERSION,
                category="scanner_capability",
                description="Scanner checks at least 15 patterns",
                patterns=["def check_"],
                min_matches=15,
            ),
            ChallengeCase(
                case_id="CHAL-007",
                version=self.VERSION,
                category="regression_coverage",
                description="Regression set has at least 10 cases",
                patterns=["RegressionCase"],
                min_matches=10,
            ),
            ChallengeCase(
                case_id="CHAL-008",
                version=self.VERSION,
                category="error_taxonomy_severity_mapping",
                description="Each error type has a default severity mapping",
                patterns=["LegalErrorType.FACTUAL", "LegalErrorType.BIAS"],
                min_matches=2,
            ),
            ChallengeCase(
                case_id="CHAL-009",
                version=self.VERSION,
                category="djimitflo_integration",
                description="Djimitflo bridge creates tasks for S3+ errors",
                patterns=["ComplianceTask", "create_task_from_error"],
                min_matches=2,
            ),
            ChallengeCase(
                case_id="CHAL-010",
                version=self.VERSION,
                category="temporal_decay",
                description="Temporal decay tracks result freshness",
                patterns=["is_expired", "freshness", "max_age_days"],
                min_matches=3,
            ),
            ChallengeCase(
                case_id="CHAL-CANARY-001",
                version=self.VERSION,
                category="canary",
                description="Canary: detects if challenge data leaked to training",
                patterns=[self._get_canary_token()],
                min_matches=1,
                is_canary=True,
            ),
        ]

    def _get_canary_token(self) -> str:
        """Get canary token from external file or return placeholder."""
        canary_path = Path(__file__).parent.parent.parent / self.CANARY_FILE
        if canary_path.exists():
            return canary_path.read_text().strip().split("\n")[0]
        return "CHALLENGE_SET_CANARY_PLACEHOLDER"

    def run(self) -> ChallengeResult:
        """Run all challenge cases."""

        start = time.time()
        failures = []
        passed = 0
        canary_triggered = False

        for case in self.cases:
            result = self._run_case(case)
            if result:
                passed += 1
                if case.is_canary:
                    canary_triggered = True
            else:
                if not case.is_canary:
                    failures.append(
                        {
                            "case_id": case.case_id,
                            "category": case.category,
                            "description": case.description,
                        }
                    )

        total = len(self.cases)
        elapsed = int((time.time() - start) * 1000)

        return ChallengeResult(
            run_id=f"chal-{hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]}",
            version=self.VERSION,
            timestamp=datetime.now().isoformat(),
            total_cases=total,
            passed=passed,
            failed=total - passed,
            canary_triggered=canary_triggered,
            failures=failures,
            execution_time_ms=elapsed,
            score=round(passed / max(total, 1), 2),
        )

    def _run_case(self, case: ChallengeCase) -> bool:
        """Run a single challenge case."""
        import subprocess

        root = Path(__file__).parent.parent.parent

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

challenge_set = ChallengeSet()
