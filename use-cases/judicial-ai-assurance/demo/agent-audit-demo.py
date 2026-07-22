"""Agent Audit Demo — JLAIF toegepast op Agentic AI Workflows."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from api.assurance.agent_auditor import agent_auditor
from api.assurance.severity_scorer import UseCaseProfile


TEST_RESULTS = [
    {
        "agent": "DPIA Agent",
        "status": "success",
        "confidence": 0.92,
        "trace": [
            {"step": "pre_scan", "status": "complete"},
            {"step": "generate", "status": "complete"},
            {"step": "risk_analysis", "status": "complete"},
            {"step": "measures", "status": "complete"},
        ],
        "citations": [
            {"source": "AVG Art. 35", "passage": "DPIA verplicht"},
        ],
        "hallucination_flags": [],
        "recommendations": ["Implementeer encryptie", "Voer DPIA uit"],
    },
    {
        "agent": "FRIA Agent",
        "status": "success",
        "confidence": 0.97,
        "trace": [
            {"step": "pre_scan", "status": "complete"},
            {"step": "generate", "status": "complete"},
        ],
        "citations": [],
        "hallucination_flags": [
            {"claim": "AI Act is al in werking", "actual": "Nog niet volledig"}
        ],
        "recommendations": [],
    },
    {
        "agent": "Incident Agent",
        "status": "partial",
        "confidence": 0.45,
        "trace": [
            {"step": "detect", "status": "complete"},
        ],
        "citations": [{"source": "Art. 33 AVG", "passage": "72u melding"}],
        "hallucination_flags": [],
        "recommendations": ["Meld bij AP", "Informeer betrokkenen"],
    },
]


def run_demo():
    print("=" * 70)
    print("JLAIF — Agent Audit Demo")
    print("Agentic AI workflows auditeren")
    print("=" * 70)
    print()

    uc = UseCaseProfile("agent_demo", 4, "algemeen", "compliance_officer")

    all_findings = []
    reports = []

    for i, result in enumerate(TEST_RESULTS, 1):
        report = agent_auditor.audit(result, expected_steps=4, use_case=uc)
        reports.append(report)
        all_findings.extend(report.findings)

        print(f"Agent {i}: {result['agent']}")
        print(f"  Status: {result['status']} | Confidence: {result['confidence']}")
        print(f"  Steps: {report.steps_completed}/{report.steps_expected}")
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
        "audit_demo": "agent_jlaif",
        "timestamp": reports[0].timestamp if reports else "",
        "test_cases": len(TEST_RESULTS),
        "total_findings": len(all_findings),
        "by_type": by_type,
        "by_severity": by_severity,
        "reports": [r.to_dict() for r in reports],
    }

    output_path = Path(__file__).parent / "agent-audit-report.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nRapport: {output_path}")


if __name__ == "__main__":
    run_demo()
