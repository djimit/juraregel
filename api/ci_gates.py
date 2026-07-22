"""CI Gates — Compliance-as-Code integration for CI/CD pipelines.

Provides:
- Pre-commit compliance checks
- PR compliance gates
- Automated policy evaluation
- Drift detection in CI
- Benchmark scoring in CI

Integrates with GitHub Actions, GitLab CI, and local pre-commit hooks.
"""

from __future__ import annotations

import json
import logging
import sys
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

# ─── Data Models ──────────────────────────────────────────────


@dataclass
class GateResult:
    """Result of a CI gate check."""

    gate: str
    passed: bool
    score: float
    findings: list[dict]
    duration_ms: int


@dataclass
class CIGateReport:
    """Complete CI gate report."""

    commit_sha: str
    branch: str
    timestamp: str
    results: list[GateResult]
    overall_passed: bool
    overall_score: float


# ─── CI Gates ─────────────────────────────────────────────────


class CIGates:
    """Compliance gates for CI/CD."""

    def __init__(self):
        self.gates = [
            self._gate_policy_evaluation,
            self._gate_drift_detection,
            self._gate_evidence_check,
            self._gate_benchmark_score,
            self._gate_template_validation,
            self._gate_regression,
            self._gate_challenge,
            self._gate_performance_drift,
        ]

    def run_all(self, context: dict | None = None) -> CIGateReport:
        """Run all CI gates."""
        import time

        ctx = context or {}
        results = []

        for gate_fn in self.gates:
            gate_start = time.time()
            try:
                result = gate_fn(ctx)
                result.duration_ms = int((time.time() - gate_start) * 1000)
                results.append(result)
            except Exception as e:
                results.append(
                    GateResult(
                        gate=gate_fn.__name__,
                        passed=False,
                        score=0.0,
                        findings=[{"error": str(e)}],
                        duration_ms=int((time.time() - gate_start) * 1000),
                    )
                )

        overall_score = sum(r.score for r in results) / max(len(results), 1)
        overall_passed = all(r.passed for r in results)

        return CIGateReport(
            commit_sha=ctx.get("commit_sha", "unknown"),
            branch=ctx.get("branch", "unknown"),
            timestamp=datetime.utcnow().isoformat(),
            results=results,
            overall_passed=overall_passed,
            overall_score=round(overall_score, 3),
        )

    def _gate_policy_evaluation(self, ctx: dict) -> GateResult:
        """Evaluate compliance policies."""
        from .policy_engine import PolicyEngine

        engine = PolicyEngine()
        context = ctx.get(
            "policy_context",
            {
                "purpose": "CI/CD check",
                "data_categories": ["Naam", "Contact"],
                "security_measures": ["encryptie", "toegangscontrole"],
                "ai_systems": False,
            },
        )

        summary = engine.get_compliance_summary(context)
        passed = summary["critical_violations"] == 0

        return GateResult(
            gate="policy_evaluation",
            passed=passed,
            score=summary["compliance_rate"] / 100,
            findings=summary.get("violations", []),
            duration_ms=0,
        )

    def _gate_drift_detection(self, ctx: dict) -> GateResult:
        """Check for compliance drift."""
        from .drift_detector import drift_detector

        assessment_id = ctx.get("assessment_id", "ci-check")
        current_state = ctx.get(
            "current_state",
            {
                "measures": {"encryptie": "implemented"},
                "evidence": [],
                "compliance_score": 80,
            },
        )

        if assessment_id in drift_detector._baselines:
            report = drift_detector.detect_drift(assessment_id, current_state)
            passed = report.drift_score < 30
            return GateResult(
                gate="drift_detection",
                passed=passed,
                score=max(0, 100 - report.drift_score) / 100,
                findings=[
                    {"type": item.type.value, "description": item.description}
                    for item in report.drift_items
                ],
                duration_ms=0,
            )

        # No baseline yet — pass
        return GateResult(
            gate="drift_detection",
            passed=True,
            score=1.0,
            findings=[{"info": "No baseline set — skipping drift check"}],
            duration_ms=0,
        )

    def _gate_evidence_check(self, ctx: dict) -> GateResult:
        """Check evidence validity."""
        evidence_list = ctx.get("evidence", [])
        if not evidence_list:
            return GateResult(
                gate="evidence_check",
                passed=True,
                score=1.0,
                findings=[{"info": "No evidence to check"}],
                duration_ms=0,
            )

        from .compliance_score import calculate_evidence_actuality

        score = calculate_evidence_actuality(evidence_list)
        passed = score >= 0.8

        return GateResult(
            gate="evidence_check",
            passed=passed,
            score=score,
            findings=[
                {
                    "evidence_count": len(evidence_list),
                    "actuality": f"{score * 100:.0f}%",
                }
            ],
            duration_ms=0,
        )

    def _gate_benchmark_score(self, ctx: dict) -> GateResult:
        """Run OpenMythos benchmark."""
        from .benchmark_runner import benchmark_runner

        category = ctx.get("benchmark_category")
        if category:
            result = benchmark_runner.run_category(category)
            if result:
                return GateResult(
                    gate="benchmark_score",
                    passed=result.verdict == "PASS",
                    score=result.score,
                    findings=result.findings,
                    duration_ms=0,
                )

        # Run all
        report = benchmark_runner.run_all()
        return GateResult(
            gate="benchmark_score",
            passed=report.overall_verdict == "PASS",
            score=report.overall_score,
            findings=[{"summary": report.summary}],
            duration_ms=0,
        )

    def _gate_template_validation(self, ctx: dict) -> GateResult:
        """Validate templates against schema."""
        from .template_schema import validate_template
        from . import generate_document

        template_id = ctx.get("template_id", "dpia_pre_scan")
        try:
            doc = generate_document(template_id, "CI Test")
            validate_template(doc)
            return GateResult(
                gate="template_validation",
                passed=True,
                score=1.0,
                findings=[{"template": template_id, "status": "valid"}],
                duration_ms=0,
            )
        except Exception as e:
            return GateResult(
                gate="template_validation",
                passed=False,
                score=0.0,
                findings=[{"template": template_id, "error": str(e)}],
                duration_ms=0,
            )

    def _gate_regression(self, ctx: dict) -> GateResult:
        """Run regression test set."""
        from .assurance.regression_set import regression_set

        result = regression_set.run()
        return GateResult(
            gate="regression",
            passed=result.passed_all,
            score=result.score,
            findings=[
                {
                    "total": result.total_cases,
                    "passed": result.passed,
                    "failed": result.failed,
                }
            ]
            + result.failures,
            duration_ms=result.execution_time_ms,
        )

    def _gate_challenge(self, ctx: dict) -> GateResult:
        """Run challenge test set."""
        from .assurance.challenge_set import challenge_set

        result = challenge_set.run()
        findings = [
            {
                "total": result.total_cases,
                "passed": result.passed,
                "failed": result.failed,
            }
        ]
        if result.canary_triggered:
            findings.append(
                {"warning": "Canary triggered — possible benchmark leakage"}
            )
        findings.extend(result.failures)

        return GateResult(
            gate="challenge",
            passed=result.passed_all,
            score=result.score,
            findings=findings,
            duration_ms=result.execution_time_ms,
        )

    def _gate_performance_drift(self, ctx: dict) -> GateResult:
        """Check for performance drift."""
        from .assurance.drift_monitor import drift_monitor
        from .assurance.regression_set import regression_set
        from .assurance.challenge_set import challenge_set

        reg_result = regression_set.run()
        chal_result = challenge_set.run()

        current_metrics = {
            "regression_score": reg_result.score,
            "challenge_score": chal_result.score,
        }

        report = drift_monitor.check(current_metrics)

        findings = []
        if report.has_drift:
            for alert in report.alerts:
                findings.append(
                    {
                        "metric": alert.metric,
                        "delta": alert.delta,
                        "severity": alert.severity,
                    }
                )
        else:
            findings.append({"info": "No drift detected"})

        return GateResult(
            gate="performance_drift",
            passed=not report.has_drift,
            score=1.0 if not report.has_drift else 0.5,
            findings=findings,
            duration_ms=0,
        )


# ─── CLI Entry Point ──────────────────────────────────────────


def main():
    """Run CI gates from command line."""
    import argparse

    parser = argparse.ArgumentParser(description="JuraRegel CI Gates")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    parser.add_argument("--gate", type=str, help="Run specific gate")
    args = parser.parse_args()

    gates = CIGates()
    report = gates.run_all()

    if args.format == "json":
        print(
            json.dumps(
                {
                    "passed": report.overall_passed,
                    "score": report.overall_score,
                    "results": [
                        {
                            "gate": r.gate,
                            "passed": r.passed,
                            "score": r.score,
                            "findings": r.findings,
                        }
                        for r in report.results
                    ],
                },
                indent=2,
            )
        )
    else:
        status = "PASS" if report.overall_passed else "FAIL"
        print(f"CI Gates: {status} (score: {report.overall_score})")
        for r in report.results:
            icon = "PASS" if r.passed else "FAIL"
            print(f"  [{icon}] {r.gate}: {r.score:.2f}")

    sys.exit(0 if report.overall_passed else 1)


if __name__ == "__main__":
    main()
