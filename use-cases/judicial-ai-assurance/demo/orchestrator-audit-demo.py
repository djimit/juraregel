"""Orchestrator Audit Demo — JLAIF toegepast op Compliance Orchestrator."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from api.assurance.orchestrator_auditor import orchestrator_auditor
from api.assurance.severity_scorer import UseCaseProfile


# ─── Test cases ────────────────────────────────────────────────

TEST_ASSESSMENTS = [
    {
        "assessment_id": "asm-001",
        "steps_completed": 7,
        "steps": [
            {"name": "jurisdiction_analysis", "status": "completed"},
            {"name": "risk_prediction", "status": "completed"},
            {"name": "knowledge_graph", "status": "completed"},
            {"name": "drift_detection", "status": "completed"},
            {"name": "rag_search", "status": "completed"},
            {"name": "synthese", "status": "completed"},
            {"name": "audit_logging", "status": "completed"},
        ],
        "jurisdiction_analysis": {"primary": "nederland", "secondary": ["eu"]},
        "conclusion": (
            "De verwerkking voldoet aan de verplichtingen uit de AVG. "
            "Art. 6 lid 1 sub b (rechtmatigheid) is van toepassing. "
            "De bewaartermijn van 5 jaar is conform de wet."
        ),
        "confidence": 0.92,
        "human_review_required": False,
        "risk_predictions": [
            {"risk_score": 0.8, "description": "Datalek"},
            {"risk_score": 0.75, "description": "Onvoldoende toestemming"},
            {"risk_score": 0.82, "description": "PII-lek"},
        ],
    },
    {
        "assessment_id": "asm-002",
        "steps_completed": 5,
        "steps": [
            {"name": "jurisdiction_analysis", "status": "completed"},
            {"name": "risk_prediction", "status": "completed"},
            {"name": "knowledge_graph", "status": "completed"},
            {"name": "rag_search", "status": "completed"},
            {"name": "synthese", "status": "completed"},
        ],
        "jurisdiction_analysis": {"primary": "nederland"},
        "conclusion": (
            "Het AI-systeem valt onder de EU AI Act als hoog-risico systeem. "
            "Er is een conformiteitsbeoordeling vereist."
        ),
        "confidence": 0.78,
        "human_review_required": False,
        "risk_predictions": [
            {"risk_score": 0.6, "description": "Bias in training data"},
        ],
    },
    {
        "assessment_id": "asm-003",
        "steps_completed": 7,
        "steps": [
            {"name": "jurisdiction_analysis", "status": "completed"},
            {"name": "risk_prediction", "status": "completed"},
            {"name": "knowledge_graph", "status": "completed"},
            {"name": "drift_detection", "status": "completed"},
            {"name": "rag_search", "status": "completed"},
            {"name": "synthese", "status": "completed"},
            {"name": "audit_logging", "status": "completed"},
        ],
        "jurisdiction_analysis": {"primary": "eu"},
        "conclusion": "",
        "confidence": 0.65,
        "human_review_required": None,
        "risk_predictions": [],
    },
]


def run_demo() -> None:
    """Run orchestrator audit demo."""
    print("=" * 70)
    print("JLAIF — Orchestrator Audit Demo")
    print("Autonome compliance assessments auditeren")
    print("=" * 70)
    print()

    uc = UseCaseProfile(
        name="orchestrator_demo",
        autonomy_level=4,
        legal_domain="algemeen",
        user_group="compliance_officer",
    )

    all_findings = []
    reports = []

    for i, assessment in enumerate(TEST_ASSESSMENTS, 1):
        report = orchestrator_auditor.audit(assessment, uc)
        reports.append(report)
        all_findings.extend(report.findings)

        print(f"Assessment {i}: {assessment['assessment_id']}")
        print(f"  Stappen: {report.steps_completed}/{report.steps_expected}")
        print(f"  Confidence: {assessment.get('confidence', 'N/A')}")
        print(f"  Bevindingen: {len(report.findings)}")
        for f in report.findings:
            print(f"    [{f.severity.value}] {f.error_type.value}: {f.description}")
        print(
            f"  Release: {report.release_decision} | Review: {'Ja' if report.human_review_required else 'Nee'}"
        )
        print()

    # Aggregate
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

    # Save
    output = {
        "audit_demo": "orchestrator_jlaif",
        "timestamp": reports[0].timestamp if reports else "",
        "test_cases": len(TEST_ASSESSMENTS),
        "total_findings": len(all_findings),
        "by_type": by_type,
        "by_severity": by_severity,
        "reports": [r.to_dict() for r in reports],
    }

    output_path = Path(__file__).parent / "orchestrator-audit-report.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nRapport: {output_path}")


if __name__ == "__main__":
    run_demo()
