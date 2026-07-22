"""Benchmark Capture Prevention — canary mechanism to detect test data leakage.

Implements Stanford's principle of benchmark capture prevention:
canary tokens are placed in the challenge set to detect if test data
has been used in training or tuning.

If a canary case passes unexpectedly, it suggests the model has seen
the test data — indicating benchmark leakage.
"""

from __future__ import annotations

import hashlib
import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

CANARY_TOKEN = "CHALLENGE_SET_CANARY_TOKEN_2026"
CANARY_SEED = os.getenv("CANARY_SEED", "juraregel-assurance-2026")


@dataclass
class CanaryCase:
    """A canary case designed to detect benchmark leakage."""

    case_id: str
    token: str
    description: str
    expected_to_fail: bool = True


@dataclass
class CanaryReport:
    """Report from canary detection."""

    run_id: str
    timestamp: str
    total_canaries: int
    triggered: int
    safe: bool
    details: list[dict[str, Any]]

    @property
    def leakage_detected(self) -> bool:
        """If True, benchmark data may have leaked to training."""
        return self.triggered > 0


class BenchmarkCapturePrevention:
    """Detects and prevents benchmark capture using canary tokens."""

    def __init__(self):
        self._canaries: list[CanaryCase] = []
        self._load_canaries()

    def _load_canaries(self) -> None:
        """Load canary cases."""
        self._canaries = [
            CanaryCase(
                case_id="CANARY-001",
                token=CANARY_TOKEN,
                description="Token that should never appear in training data",
                expected_to_fail=True,
            ),
            CanaryCase(
                case_id="CANARY-002",
                token=hashlib.sha256(f"{CANARY_SEED}-alpha".encode()).hexdigest()[:16],
                description="Hashed canary for embedding detection",
                expected_to_fail=True,
            ),
            CanaryCase(
                case_id="CANARY-003",
                token=hashlib.sha256(f"{CANARY_SEED}-beta".encode()).hexdigest()[:16],
                description="Hashed canary for retrieval detection",
                expected_to_fail=True,
            ),
        ]

    def check_leakage(self, codebase_scan: dict[str, Any]) -> CanaryReport:
        """Check if canary tokens appear in the codebase (indicating leakage)."""
        triggered = 0
        details = []

        for canary in self._canaries:
            found = self._scan_for_token(canary.token, codebase_scan)
            if found:
                triggered += 1
                details.append(
                    {
                        "case_id": canary.case_id,
                        "triggered": True,
                        "description": f"Canary token found: {canary.description}",
                    }
                )
            else:
                details.append(
                    {
                        "case_id": canary.case_id,
                        "triggered": False,
                        "description": "Canary safe",
                    }
                )

        return CanaryReport(
            run_id=f"canary-{hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]}",
            timestamp=datetime.now().isoformat(),
            total_canaries=len(self._canaries),
            triggered=triggered,
            safe=triggered == 0,
            details=details,
        )

    def _scan_for_token(self, token: str, scan_results: dict[str, Any]) -> bool:
        """Scan for a canary token in the results."""
        scan_str = str(scan_results)
        return token in scan_str

    def generate_canary_file(self, output_path: str) -> str:
        """Generate a canary file to be placed in the challenge set directory."""
        content = "# BENCHMARK CANARY FILE — DO NOT INCLUDE IN TRAINING\n"
        content += f"# Token: {CANARY_TOKEN}\n"
        content += f"# Generated: {datetime.now().isoformat()}\n"
        content += "# Purpose: Detect benchmark leakage\n"

        for canary in self._canaries:
            content += f"# {canary.case_id}: {canary.token}\n"

        with open(output_path, "w") as f:
            f.write(content)

        return output_path


# ─── Singleton ─────────────────────────────────────────────────

benchmark_capture_prevention = BenchmarkCapturePrevention()
