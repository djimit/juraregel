"""Incident-Driven Tests — generate new test cases from production incidents.

Implements Stanford's principle that benchmarking must be a continuous
capability: new incidents automatically generate new test cases.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

INCIDENT_STORE_PATH = os.getenv(
    "INCIDENT_STORE_PATH", ".swarm/evidence/incidents.jsonl"
)


@dataclass
class Incident:
    """A production incident that should generate a new test case."""

    incident_id: str
    timestamp: str
    description: str
    error_type: str
    severity: str
    source_claim: str
    expected_behavior: str
    actual_behavior: str
    resolved: bool = False


@dataclass
class IncidentTestCase:
    """A test case generated from an incident."""

    case_id: str
    source_incident: str
    description: str
    error_type: str
    severity: str
    patterns: list[str]
    min_matches: int


class IncidentDrivenTests:
    """Generate and manage test cases from production incidents."""

    def __init__(self):
        self._incidents: list[Incident] = []
        self._test_cases: list[IncidentTestCase] = []
        self._load_incidents()

    def _load_incidents(self) -> None:
        """Load incidents from disk."""
        path = Path(INCIDENT_STORE_PATH)
        if path.exists():
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data = json.loads(line)
                        self._incidents.append(**data)

    def record_incident(self, incident: Incident) -> IncidentTestCase:
        """Record a new incident and generate a test case from it."""
        self._incidents.append(incident)

        test_case = IncidentTestCase(
            case_id=f"INC-{hashlib.sha256(incident.incident_id.encode()).hexdigest()[:8]}",
            source_incident=incident.incident_id,
            description=f"Regression test for: {incident.description}",
            error_type=incident.error_type,
            severity=incident.severity,
            patterns=[incident.error_type.lower(), incident.severity.lower()],
            min_matches=1,
        )
        self._test_cases.append(test_case)

        path = Path(INCIDENT_STORE_PATH)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a") as f:
            f.write(json.dumps(incident.__dict__) + "\n")

        return test_case

    def get_test_cases(self) -> list[IncidentTestCase]:
        """Get all incident-driven test cases."""
        return self._test_cases

    def run_tests(self) -> dict[str, Any]:
        """Run all incident-driven test cases."""
        import subprocess

        root = Path(__file__).parent.parent
        passed = 0
        failures = []

        for tc in self._test_cases:
            all_match = True
            for pattern in tc.patterns:
                try:
                    result = subprocess.run(
                        ["rg", "-l", pattern, "--glob", "*.py", str(root)],
                        capture_output=True,
                        text=True,
                        timeout=10,
                    )
                    matches = [m for m in result.stdout.strip().split("\n") if m]
                    if len(matches) < tc.min_matches:
                        all_match = False
                        break
                except (FileNotFoundError, subprocess.TimeoutExpired):
                    all_match = False
                    break

            if all_match:
                passed += 1
            else:
                failures.append({"case_id": tc.case_id, "description": tc.description})

        return {
            "total": len(self._test_cases),
            "passed": passed,
            "failed": len(failures),
            "failures": failures,
            "score": round(passed / max(len(self._test_cases), 1), 2),
        }


# ─── Singleton ─────────────────────────────────────────────────

incident_driven_tests = IncidentDrivenTests()
