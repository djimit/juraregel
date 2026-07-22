"""Regulatory Monitor Audit Demo — JLAIF toegepast op Regulatory Monitor."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from api.assurance.regulatory_monitor_auditor import regulatory_monitor_auditor
from api.assurance.severity_scorer import UseCaseProfile


TEST_RESULTS = [
    {
        "changes_detected": 3,
        "sources_scanned": 4,
        "changes": [
            {
                "title": "EU AI Act uitvoeringsbesluit 2026",
                "impact_level": "critical",
                "impact_score": 0.9,
                "effective_date": "2026-08-02",
                "affected_frameworks": ["EU AI Act"],
            },
            {
                "title": "AVG richtlijn update",
                "impact_level": "medium",
                "impact_score": 0.5,
                "effective_date": "2025-01-15",
                "affected_frameworks": ["AVG"],
            },
            {
                "title": "NIS2 implementatie wijziging",
                "impact_level": "low",
                "impact_score": 0.8,
                "effective_date": "2024-10-17",
                "affected_frameworks": ["NIS2"],
            },
        ],
        "errors": [],
    },
    {
        "changes_detected": 1,
        "sources_scanned": 2,
        "changes": [
            {
                "title": "Verouderde wijziging",
                "impact_level": None,
                "impact_score": 0.3,
                "effective_date": "2022-06-01",
                "affected_frameworks": ["AVG"],
            },
        ],
        "errors": ["EUR-Lex timeout", "Staatsblad 404"],
    },
    {
        "changes_detected": 0,
        "sources_scanned": 4,
        "changes": [],
        "errors": [],
    },
]


def run_demo():
    print("=" * 70)
    print("JLAIF — Regulatory Monitor Audit Demo")
    print("Regulatory change detection auditeren")
    print("=" * 70)
    print()

    uc = UseCaseProfile("regulatory_demo", 3, "algemeen", "compliance_officer")

    all_findings = []
    reports = []

    for i, result in enumerate(TEST_RESULTS, 1):
        report = regulatory_monitor_auditor.audit(result, use_case=uc)
        reports.append(report)
        all_findings.extend(report.findings)

        print(f"Scan {i}:")
        print(
            f"  Changes: {report.changes_detected} | Errors: {report.errors_count} | Sources: {report.sources_scanned}"
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
        "audit_demo": "regulatory_monitor_jlaif",
        "timestamp": reports[0].timestamp if reports else "",
        "test_cases": len(TEST_RESULTS),
        "total_findings": len(all_findings),
        "by_type": by_type,
        "by_severity": by_severity,
        "reports": [r.to_dict() for r in reports],
    }

    output_path = Path(__file__).parent / "regulatory-monitor-audit-report.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nRapport: {output_path}")


if __name__ == "__main__":
    run_demo()
