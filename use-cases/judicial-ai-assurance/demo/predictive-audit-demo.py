"""Predictive Compliance Audit Demo — JLAIF toegepast op Predictive Engine."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from api.assurance.predictive_compliance_auditor import predictive_compliance_auditor
from api.assurance.severity_scorer import UseCaseProfile


# ─── Test cases ────────────────────────────────────────────────

TEST_REPORTS = [
    {
        "organisation_id": "org-001",
        "risk_predictions": [
            {
                "risk_id": "r1",
                "description": "Datalek door onvoldoende encryptie",
                "probability": 0.7,
                "impact": 0.8,
                "risk_score": 0.56,
                "timeframe": "90d",
            },
            {
                "risk_id": "r2",
                "description": "AVG-overtreding bij gegevensoverdracht",
                "probability": 0.4,
                "impact": 0.9,
                "risk_score": 0.36,
                "timeframe": "180d",
            },
            {
                "risk_id": "r3",
                "description": "AI Act non-conformiteit",
                "probability": 0.6,
                "impact": 0.7,
                "risk_score": 0.42,
                "timeframe": "90d",
            },
        ],
        "trend_analysis": {
            "current_score": 72,
            "previous_score": 75,
            "trend": "declining",
            "forecast_30d": 70,
            "forecast_90d": 65,
            "forecast_180d": 58,
            "confidence_interval": (60, 80),
        },
        "regulatory_forecast": [
            {"change": "EU AI Act fase-in", "date": "2026-08-01", "impact": "hoog"},
        ],
        "early_warnings": [
            "Compliance-score daalt 3 punten in 30 dagen",
            "AI Act vereisten worden per augustus bindend",
        ],
        "overall_risk_score": 0.45,
        "priority_actions": [
            "Implementeer encryptie-at-rest",
            "Voer DPIA uit voor gegevensoverdracht",
        ],
    },
    {
        "organisation_id": "org-002",
        "risk_predictions": [
            {
                "risk_id": "r1",
                "description": "Bias in AI-systeem",
                "probability": 0.5,
                "impact": 0.5,
                "risk_score": 0.30,
                "timeframe": "90d",
            },
            {
                "risk_id": "r2",
                "description": "Onvoldoende logging",
                "probability": 0.5,
                "impact": 0.5,
                "risk_score": 0.30,
                "timeframe": "90d",
            },
            {
                "risk_id": "r3",
                "description": "Geen menselijk toezicht",
                "probability": 0.5,
                "impact": 0.5,
                "risk_score": 0.30,
                "timeframe": "90d",
            },
        ],
        "trend_analysis": {
            "current_score": 80,
            "previous_score": 80,
            "trend": "stable",
            "forecast_30d": 80,
            "forecast_90d": 80,
            "forecast_180d": 80,
            "confidence_interval": (75, 85),
        },
        "regulatory_forecast": [],
        "early_warnings": [],
        "overall_risk_score": 0.30,
        "priority_actions": ["Review AI bias protocols"],
    },
    {
        "organisation_id": "org-003",
        "risk_predictions": [],
        "trend_analysis": {},
        "regulatory_forecast": [],
        "early_warnings": [],
        "overall_risk_score": 0.0,
        "priority_actions": [],
    },
]


def run_demo() -> None:
    """Run predictive compliance audit demo."""
    print("=" * 70)
    print("JLAIF — Predictive Compliance Audit Demo")
    print("Voorspellende compliance rapporten auditeren")
    print("=" * 70)
    print()

    uc = UseCaseProfile(
        name="predictive_demo",
        autonomy_level=3,
        legal_domain="algemeen",
        user_group="compliance_officer",
    )

    all_findings = []
    reports = []

    for i, report_data in enumerate(TEST_REPORTS, 1):
        report = predictive_compliance_auditor.audit(report_data, uc)
        reports.append(report)
        all_findings.extend(report.findings)

        print(f"Organisatie {i}: {report_data['organisation_id']}")
        print(f"  Risico's: {report.risk_count} | Warnings: {report.warning_count}")
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
        "audit_demo": "predictive_compliance_jlaif",
        "timestamp": reports[0].timestamp if reports else "",
        "test_cases": len(TEST_REPORTS),
        "total_findings": len(all_findings),
        "by_type": by_type,
        "by_severity": by_severity,
        "reports": [r.to_dict() for r in reports],
    }

    output_path = Path(__file__).parent / "predictive-audit-report.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nRapport: {output_path}")


if __name__ == "__main__":
    run_demo()
