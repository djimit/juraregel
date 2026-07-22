"""Codebase Scanner — pattern-based compliance detection.

Scans the JuraRegel codebase for implementation patterns that
satisfy (or fail to satisfy) specific assurance requirements.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ScanFinding:
    """A single scan finding."""

    check_id: str
    passed: bool
    confidence: float  # 0.0-1.0
    evidence: list[str] = field(default_factory=list)
    details: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "passed": self.passed,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "details": self.details,
        }


class CodebaseScanner:
    """Scans JuraRegel codebase for compliance patterns."""

    def __init__(self, root: str | Path | None = None):
        self.root = Path(root) if root else Path(__file__).parent.parent.parent

    def grep(self, pattern: str, glob: str = "*.py") -> list[str]:
        """Search codebase for pattern using ripgrep."""
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

    def grep_in_file(self, pattern: str, file_path: str) -> list[str]:
        """Search a specific file for pattern."""
        try:
            result = subprocess.run(
                ["rg", "-n", pattern, str(self.root / file_path)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return [line for line in result.stdout.strip().split("\n") if line]
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return []

    def check_pattern_exists(self, pattern: str, min_matches: int = 1) -> ScanFinding:
        """Check if a pattern exists in the codebase."""
        matches = self.grep(pattern)
        return ScanFinding(
            check_id=f"pattern_exists:{pattern}",
            passed=len(matches) >= min_matches,
            confidence=min(len(matches) / max(min_matches, 1), 1.0),
            evidence=matches[:5],
            details=f"Found {len(matches)} matches for '{pattern}'",
        )

    def check_class_exists(self, class_name: str) -> ScanFinding:
        """Check if a class is defined in the codebase."""
        matches = self.grep(f"class {class_name}")
        return ScanFinding(
            check_id=f"class_exists:{class_name}",
            passed=len(matches) > 0,
            confidence=1.0 if matches else 0.0,
            evidence=matches,
            details=f"Class '{class_name}' {'found' if matches else 'not found'}",
        )

    def check_function_exists(self, function_name: str) -> ScanFinding:
        """Check if a function is defined in the codebase."""
        matches = self.grep(f"def {function_name}")
        return ScanFinding(
            check_id=f"function_exists:{function_name}",
            passed=len(matches) > 0,
            confidence=1.0 if matches else 0.0,
            evidence=matches,
            details=f"Function '{function_name}' {'found' if matches else 'not found'}",
        )

    def check_enum_value(self, enum_class: str, value: str) -> ScanFinding:
        """Check if an enum has a specific value."""
        matches = self.grep(f"class {enum_class}")
        if not matches:
            return ScanFinding(
                check_id=f"enum_value:{enum_class}.{value}",
                passed=False,
                confidence=0.0,
                details=f"Enum class '{enum_class}' not found",
            )

        # Search for the value within files containing the enum class
        value_matches = self.grep(value)
        in_enum_files = [m for m in value_matches if m in matches]

        return ScanFinding(
            check_id=f"enum_value:{enum_class}.{value}",
            passed=len(in_enum_files) > 0,
            confidence=1.0 if in_enum_files else 0.0,
            evidence=in_enum_files,
            details=f"Value '{value}' in '{enum_class}' {'found' if in_enum_files else 'not found'}",
        )

    def check_all(self) -> dict[str, ScanFinding]:
        """Run all standard checks."""
        checks = {
            "error_taxonomy": self.check_class_exists("LegalErrorType"),
            "severity_enum": self.check_class_exists("Severity"),
            "severity_s1_s5": self.check_pattern_exists("S1_COSMETISCH|S5_SYSTEEMISCH"),
            "severity_scorer": self.check_function_exists("score_system"),
            "release_gate": self.check_function_exists("evaluate_release"),
            "evidence_lineage": self.check_class_exists("EvidenceLineage"),
            "gate_seal": self.check_function_exists("seal"),
            "jai_rules": self.check_pattern_exists("JAI-0[0-9]{2}"),
            "accountable_ai": self.check_class_exists("Explanation"),
            "drift_detector": self.check_class_exists("DriftDetector"),
            "regulatory_monitor": self.check_class_exists("RegulatoryMonitor"),
            "knowledge_graph": self.check_class_exists("KnowledgeGraph"),
            "digital_twin": self.check_class_exists("TwinNode"),
            "predictive_compliance": self.check_class_exists("RiskPrediction"),
            "self_learning": self.check_function_exists("learn_from_feedback"),
            "ci_gates": self.check_function_exists("run_gates"),
            "benchmark_runner": self.check_class_exists("BenchmarkRunner"),
            "legal_reasoning": self.check_class_exists("LegalReasoningEngine"),
            "policy_engine": self.check_class_exists("Policy"),
            "multi_jurisdiction": self.check_class_exists("MultiJurisdiction"),
        }
        return checks

    def to_report(self) -> dict[str, Any]:
        """Generate a full scan report."""
        findings = self.check_all()
        passed = sum(1 for f in findings.values() if f.passed)
        total = len(findings)

        return {
            "total_checks": total,
            "passed": passed,
            "failed": total - passed,
            "score": round(passed / max(total, 1), 2),
            "findings": {k: v.to_dict() for k, v in findings.items()},
        }
