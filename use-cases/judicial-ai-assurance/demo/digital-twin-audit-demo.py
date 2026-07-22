"""Digital Twin Audit Demo — JLAIF toegepast op de Compliance Digital Twin."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from api.assurance.digital_twin_auditor import digital_twin_auditor
from api.assurance.severity_scorer import UseCaseProfile


TEST_REPORTS = [
    {
        "organisation_id": "org-001",
        "nodes": [
            {
                "node_id": "pa-0",
                "node_type": "processing",
                "name": "CRM",
                "status": "compliant",
                "score": 85,
            },
            {
                "node_id": "risk-datalek",
                "node_type": "risk",
                "name": "Datalek",
                "status": "at_risk",
                "score": 30,
            },
            {
                "node_id": "fw-avg",
                "node_type": "framework",
                "name": "AVG",
                "status": "active",
                "score": 75,
            },
            {
                "node_id": "fw-ai",
                "node_type": "framework",
                "name": "AI Act",
                "status": "active",
                "score": 60,
            },
        ],
        "edges": [],
        "overall_score": 72,
        "framework_scores": {"AVG": 75, "AI Act": 60},
        "scenarios": [
            {
                "scenario_id": "scen-1",
                "description": "Implementeer encryptie",
                "predicted_impact": {"AVG": +15, "NIS2": +20},
                "predicted_risks": ["Verlaagd datalek"],
            },
            {
                "scenario_id": "scen-2",
                "description": "Voer DPIA uit",
                "predicted_impact": {"AVG": +20, "AI Act": +10},
                "predicted_risks": ["Identificatie risico's"],
            },
        ],
        "alerts": [
            "WARNING: AI Act score is onder de norm (60/100)",
            "RISICO: Datalek vereist aandacht",
        ],
    },
    {
        "organisation_id": "org-002",
        "nodes": [
            {
                "node_id": "fw-avg",
                "node_type": "framework",
                "name": "AVG",
                "status": "active",
                "score": 90,
            },
        ],
        "edges": [],
        "overall_score": 90,
        "framework_scores": {"AVG": 90},
        "scenarios": [],
        "alerts": [],
    },
    {
        "organisation_id": "org-003",
        "nodes": [
            {
                "node_id": "pa-0",
                "node_type": "processing",
                "name": "AI-systeem",
                "status": "at_risk",
                "score": 40,
            },
            {
                "node_id": "risk-disc",
                "node_type": "risk",
                "name": "Discriminatie",
                "status": "at_risk",
                "score": 25,
            },
            {
                "node_id": "fw-ai",
                "node_type": "framework",
                "name": "AI Act",
                "status": "active",
                "score": 45,
            },
        ],
        "edges": [],
        "overall_score": 35,
        "framework_scores": {"AI Act": 45},
        "scenarios": [
            {
                "scenario_id": "scen-1",
                "description": "Implementeer human oversight",
                "predicted_impact": {"AI Act": +35},
                "predicted_risks": ["Verlaagd discriminatie"],
            },
        ],
        "alerts": ["CRITICAL: AI Act score is kritiek laag (45/100)"],
    },
]


def run_demo() -> None:
    print("=" * 70)
    print("JLAIF — Digital Twin Audit Demo")
    print("Digitale tweeling auditeren op realisme en bias")
    print("=" * 70)
    print()

    uc = UseCaseProfile("digital_twin_demo", 3, "algemeen", "compliance_officer")

    all_findings = []
    reports = []

    for i, report_data in enumerate(TEST_REPORTS, 1):
        report = digital_twin_auditor.audit(report_data, uc)
        reports.append(report)
        all_findings.extend(report.findings)

        print(f"Organisatie {i}: {report_data['organisation_id']}")
        print(
            f"  Nodes: {report.node_count} | Scenarios: {report.scenario_count} | Alerts: {report.alert_count}"
        )
        print(f"  Overall Score: {report.overall_score}")
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
        "audit_demo": "digital_twin_jlaif",
        "timestamp": reports[0].timestamp if reports else "",
        "test_cases": len(TEST_REPORTS),
        "total_findings": len(all_findings),
        "by_type": by_type,
        "by_severity": by_severity,
        "reports": [r.to_dict() for r in reports],
    }

    output_path = Path(__file__).parent / "digital-twin-audit-report.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nRapport: {output_path}")


if __name__ == "__main__":
    run_demo()
