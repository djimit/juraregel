"""Continuous Evaluation Audit Demo — JLAIF toegepast op de Continuous Evaluation Engine."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from api.assurance.continuous_evaluation_auditor import continuous_evaluation_auditor
from api.assurance.severity_scorer import UseCaseProfile


TEST_REPORTS = [
    {
        "report_id": "eval-001",
        "results": [
            {"module": "rag_engine", "score": 1.0, "max_score": 1.0, "passed": True},
            {
                "module": "legal_reasoning",
                "score": 1.0,
                "max_score": 1.0,
                "passed": True,
            },
            {
                "module": "predictive_compliance",
                "score": 1.0,
                "max_score": 1.0,
                "passed": True,
            },
            {
                "module": "report_generator",
                "score": 1.0,
                "max_score": 1.0,
                "passed": True,
            },
            {
                "module": "accountability",
                "score": 1.0,
                "max_score": 1.0,
                "passed": True,
            },
            {"module": "orchestrator", "score": 1.0, "max_score": 1.0, "passed": True},
        ],
        "overall_score": 1.0,
        "overall_grade": "A",
        "improvements": ["rag_engine: 100%", "legal_reasoning: 100%"],
        "regressions": [],
        "action_items": [],
    },
    {
        "report_id": "eval-002",
        "results": [
            {"module": "rag_engine", "score": 0.8, "max_score": 1.0, "passed": True},
            {
                "module": "legal_reasoning",
                "score": 0.7,
                "max_score": 1.0,
                "passed": True,
            },
            {
                "module": "predictive_compliance",
                "score": 0.6,
                "max_score": 1.0,
                "passed": False,
            },
            {
                "module": "report_generator",
                "score": 0.9,
                "max_score": 1.0,
                "passed": True,
            },
        ],
        "overall_score": 0.75,
        "overall_grade": "C",
        "improvements": ["rag_engine: 80%", "report_generator: 90%"],
        "regressions": ["predictive_compliance: 60%"],
        "action_items": [
            {"module": "predictive_compliance", "priority": "medium", "actions": []}
        ],
    },
    {
        "report_id": "eval-003",
        "results": [],
        "overall_score": 0.0,
        "overall_grade": "F",
        "improvements": [],
        "regressions": [],
        "action_items": [],
    },
]


def run_demo() -> None:
    print("=" * 70)
    print("JLAIF — Continuous Evaluation Audit Demo")
    print("De auditor van de auditor")
    print("=" * 70)
    print()

    uc = UseCaseProfile("continuous_eval_demo", 4, "algemeen", "auditor")

    all_findings = []
    reports = []

    for i, report_data in enumerate(TEST_REPORTS, 1):
        report = continuous_evaluation_auditor.audit(report_data, uc)
        reports.append(report)
        all_findings.extend(report.findings)

        print(f"Evaluatie {i}: {report_data['report_id']}")
        print(
            f"  Modules: {report.modules_evaluated} | Grade: {report.overall_grade} | Score: {report.overall_score:.2f}"
        )
        print(f"  Bevindingen: {len(report.findings)}")
        for f in report.findings:
            print(f"    [{f.severity.value}] {f.error_type.value}: {f.description}")
        print(
            f"  Release: {report.release_decision} | Review: {'Ja' if report.human_review_required else 'Nee'}"
        )
        print()

    print("=" * 70)
    print("AGGREGAAT")
    print("=" * 70)
    print(f"Totaal bevindingen: {len(all_findings)}")

    by_type: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    for f in all_findings:
        by_type[f.error_type.value] = by_type.get(f.error_type.value, 0) + 1
        by_severity[f.severity.value] = by_severity.get(f.severity.value, 0) + 1

    print("Per fouttype:")
    for et, count in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {et}: {count}")
    print("Per severity:")
    for sev, count in sorted(by_severity.items()):
        print(f"  {sev}: {count}")
    print()

    decisions = {r.release_decision for r in reports}
    print(f"Release decisions: {', '.join(decisions)}")
    print(
        f"Human review: {sum(1 for r in reports if r.human_review_required)}/{len(reports)}"
    )

    output = {
        "audit_demo": "continuous_evaluation_jlaif",
        "timestamp": reports[0].timestamp if reports else "",
        "test_cases": len(TEST_REPORTS),
        "total_findings": len(all_findings),
        "by_type": by_type,
        "by_severity": by_severity,
        "reports": [r.to_dict() for r in reports],
    }

    output_path = Path(__file__).parent / "continuous-eval-audit-report.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nRapport: {output_path}")


if __name__ == "__main__":
    run_demo()
