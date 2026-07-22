"""Multi-Jurisdiction Audit Demo — JLAIF toegepast op de Multi-Jurisdiction Engine."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from api.assurance.multi_jurisdiction_auditor import multi_jurisdiction_auditor
from api.assurance.severity_scorer import UseCaseProfile


TEST_REPORTS = [
    {
        "applicable_frameworks": ["AVG", "EU AI Act", "NIS2"],
        "obligations": [
            {
                "framework": "AVG",
                "jurisdiction": "NL",
                "article": "Art. 5",
                "title": "Beginselen",
                "penalty": "Boete tot EUR 20.000.000 of 4% van de wereldwijde jaaromzet",
                "deadline": None,
            },
            {
                "framework": "EU AI Act",
                "jurisdiction": "EU",
                "article": "Art. 9",
                "title": "Risicobeheer",
                "penalty": "Boete tot EUR 15.000.000 of 3% van de wereldwijde jaaromzet",
                "deadline": "2026-08-02",
            },
            {
                "framework": "NIS2",
                "jurisdiction": "EU",
                "article": "Art. 21",
                "title": "Cybersecurity",
                "penalty": "Boete tot EUR 10.000.000 of 2% van de wereldwijde jaaromzet",
                "deadline": "2024-10-17 (implementatie NL)",
            },
        ],
        "conflicts": [
            {
                "conflict_type": "overlap",
                "severity": "low",
                "resolution_hint": "Combineer DPIA en FRIA",
            }
        ],
        "gaps": [],
        "recommendations": ["URGENT: Geen DPIA-uitvoering gedocumenteerd"],
    },
    {
        "applicable_frameworks": ["AVG", "EU AI Act"],
        "obligations": [
            {
                "framework": "AVG",
                "jurisdiction": "INT",
                "article": "Art. 5",
                "title": "Beginselen",
                "penalty": "Boete tot EUR 25.000.000",
                "deadline": None,
            },
        ],
        "conflicts": [],
        "gaps": ["Geen DPIA-uitvoering gedocumenteerd"],
        "recommendations": [],
    },
    {
        "applicable_frameworks": ["AVG"],
        "obligations": [
            {
                "framework": "AVG",
                "jurisdiction": "NL",
                "article": "Art. 5",
                "title": "Beginselen",
                "penalty": None,
                "deadline": None,
            },
        ],
        "conflicts": [],
        "gaps": [],
        "recommendations": [],
    },
]


def run_demo() -> None:
    print("=" * 70)
    print("JLAIF — Multi-Jurisdiction Audit Demo")
    print("Juridische analyse over meerdere rechtsgebieden auditeren")
    print("=" * 70)
    print()

    uc = UseCaseProfile("multi_jurisdiction_demo", 3, "multi", "jurist")

    all_findings = []
    reports = []

    for i, report_data in enumerate(TEST_REPORTS, 1):
        report = multi_jurisdiction_auditor.audit(report_data, uc)
        reports.append(report)
        all_findings.extend(report.findings)

        print(f"Analyse {i}:")
        print(f"  Frameworks: {', '.join(report.frameworks)}")
        print(
            f"  Obligaties: {report.obligation_count} | Conflicten: {report.conflict_count} | Gaps: {report.gap_count}"
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
        "audit_demo": "multi_jurisdiction_jlaif",
        "timestamp": reports[0].timestamp if reports else "",
        "test_cases": len(TEST_REPORTS),
        "total_findings": len(all_findings),
        "by_type": by_type,
        "by_severity": by_severity,
        "reports": [r.to_dict() for r in reports],
    }

    output_path = Path(__file__).parent / "multi-jurisdiction-audit-report.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nRapport: {output_path}")


if __name__ == "__main__":
    run_demo()
