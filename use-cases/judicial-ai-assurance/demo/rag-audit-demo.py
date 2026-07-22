"""RAG Engine Audit Demo — apply JLAIF to real RAG engine output.

Demonstrates how the JLAIF framework audits the JuraRegel RAG engine
for all 9 error types with severity-weighted scoring.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from api.assurance.rag_auditor import rag_engine_auditor
from api.assurance.severity_scorer import UseCaseProfile


# ─── Test cases ────────────────────────────────────────────────

TEST_CASES = [
    {
        "question": "Wat zijn de verplichtingen bij een datalek onder de AVG?",
        "sample_answer": (
            "Bij een datalek moet de verwerkingsverantwoordelijke binnen 72 uur "
            "melding doen aan de Autoriteit Persoonsgegevens conform Art. 33 AVG. "
            "Ook moet worden geëvalueerd of het lek een hoog risico vormt voor de "
            "rechten en vrijheden van betrokkenen (Art. 34 AVG). "
            "De melding moet bevatten: aard van het lek, categorieën gegevens, "
            "geschatte aantallen, en genomen maatregelen. "
            "Daarentegen kan het ook nodig zijn om betrokkenen direct te informeren "
            "als er een hoog risico is."
        ),
        "jurisdiction": "nederland",
        "autonomy_level": 2,
    },
    {
        "question": "Is een AI-systeem voor CV-screening hoog-risico onder de EU AI Act?",
        "sample_answer": (
            "Ja, AI-systemen voor CV-screening worden geclassificeerd als hoog-risico "
            "conform de EU AI Act. Dit valt onder Annex III punt 4 (toegang tot werk). "
            "Voor hoog-risicosystemen gelden strenge eisen: risicomanagement, "
            "datagovernance, technische documentatie, transparantie, menselijk toezicht, "
            "en conformiteitsbeoordeling voordat het systeem op de markt mag."
        ),
        "jurisdiction": "eu",
        "autonomy_level": 3,
    },
    {
        "question": "Mag ik persoonsgegevens naar een land buiten de EU overdragen?",
        "sample_answer": (
            "Overdracht van persoonsgegevens naar een derdland is mogelijk als er "
            "een adequate beschermingsniveau is. De Europese Commissie kan een "
            "adequaatheidsbesluit nemen. Zonder adequaatheid zijn Standard Contractual "
            "Clauses of Binding Corporate Rules nodig. "
            "De privacyrichtlijn uit 1995 is hier niet meer van toepassing."
        ),
        "jurisdiction": "eu",
        "autonomy_level": 2,
    },
    {
        "question": "Wat is de bewaartermijn voor belastinggegevens?",
        "sample_answer": (
            "Belastinggegevens moeten 5 jaar worden bewaard conform de Algemene wet "
            "rijksbelastingen. Dit is een standaard termijn voor fiscale doeleinden."
        ),
        "jurisdiction": "nederland",
        "autonomy_level": 2,
    },
    {
        "question": "Een patiënt met BSN 123456789 en email jan@email.com heeft...",
        "sample_answer": (
            "De patiënt met BSN 123456789 heeft recht op inzage in zijn medisch dossier "
            "conform Art. 15 AVG. U kunt contact opnemen via jan@email.com."
        ),
        "jurisdiction": "nederland",
        "autonomy_level": 2,
    },
]


def run_audit_demo() -> None:
    """Run the RAG engine audit demo."""
    print("=" * 70)
    print("JLAIF — RAG Engine Audit Demo")
    print("Juridische AI auditeren op 9 fouttypes met severity-weighted scoring")
    print("=" * 70)
    print()

    all_findings = []
    reports = []

    for i, case in enumerate(TEST_CASES, 1):
        uc = UseCaseProfile(
            name=f"test-case-{i}",
            autonomy_level=case["autonomy_level"],
            legal_domain="algemeen",
            user_group="advocaat",
        )

        report = rag_engine_auditor.audit(
            question=case["question"],
            answer=case["sample_answer"],
            expected_jurisdiction=case["jurisdiction"],
            use_case=uc,
        )
        reports.append(report)
        all_findings.extend(report.findings)

        print(f"Test {i}: {case['question'][:60]}...")
        print(
            f"  Jurisdictie: {case['jurisdiction']} | Autonomie: L{case['autonomy_level']}"
        )
        print(f"  Bevindingen: {len(report.findings)}")
        for f in report.findings:
            print(f"    [{f.severity.value}] {f.error_type.value}: {f.description}")
        print(f"  Release Gate: {report.release_decision}")
        print(f"  Human Review:  {'Ja' if report.human_review_required else 'Nee'}")
        print()

    # ─── Aggregate report ─────────────────────────────────────────
    print("=" * 70)
    print("AGGREGAAT RAPPORT")
    print("=" * 70)
    print()

    total_findings = len(all_findings)
    by_type: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    for f in all_findings:
        by_type[f.error_type.value] = by_type.get(f.error_type.value, 0) + 1
        by_severity[f.severity.value] = by_severity.get(f.severity.value, 0) + 1

    print(f"Totaal bevindingen: {total_findings}")
    print()
    print("Per fouttype:")
    for error_type, count in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {error_type}: {count}")
    print()
    print("Per severity:")
    for sev, count in sorted(by_severity.items()):
        print(f"  {sev}: {count}")
    print()

    # Release decisions
    decisions = {r.release_decision for r in reports}
    print(f"Release decisions: {', '.join(decisions)}")
    print(
        f"Human review nodig: {sum(1 for r in reports if r.human_review_required)}/{len(reports)}"
    )
    print()

    # Save report
    output = {
        "audit_demo": "rag_engine_jlaif",
        "timestamp": reports[0].timestamp if reports else "",
        "test_cases": len(TEST_CASES),
        "total_findings": total_findings,
        "by_type": by_type,
        "by_severity": by_severity,
        "reports": [r.to_dict() for r in reports],
    }

    output_path = Path(__file__).parent / "rag-audit-report.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Rapport opgeslagen: {output_path}")


if __name__ == "__main__":
    run_audit_demo()
