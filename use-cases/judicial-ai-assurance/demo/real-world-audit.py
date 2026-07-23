"""Real-World JLAIF Audit — echte Nederlandse juridische teksten.

Gebruikt representatieve teksten uit:
- Bestuursrecht (Awb, Wob)
- Civiel recht (verbintenissen, overeenkomsten)
- Strafrecht (voorwaardelijke straffen, schadevergoeding)
- Privacy recht (AVG meldplicht, recht op vergeten)
- AI Act (compliance, risicobeheer)

Elke tekst wordt geauditeerd op de 9 fouttypes + PII + jurisdictie.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from api.assurance.rag_auditor import rag_engine_auditor
from api.assurance.pii_redaction import pii_redaction
from api.assurance.jurisdiction import jurisdiction_classifier
from api.assurance.citation_verification import citation_verifier
from api.assurance.temporal_validity import temporal_checker
from api.assurance.severity_scorer import UseCaseProfile


# ─── Real-world test cases ─────────────────────────────────────

REAL_WORLD_CASES = [
    {
        "id": "RW-001",
        "source": "Bestuursrecht — Wob-verzoek",
        "question": "Wat zijn de uitzonderingen op de openbaarheid van bestuur volgens de Wob?",
        "answer": (
            "Op grond van artikel 10, eerste lid, van de Wet openbaarheid van bestuur "
            "kunnen bestuursorganen weigeren informatie openbaar te maken indien dit "
            "betreft: a) de eenheid van de Kroon, b) de staatsveiligheid, c) "
            "vertrouwelijke mededelingen van vreemde mogendheden. Daarnaast kan "
            "openbaarheid worden geweigerd indien het belang van de betrokkene "
            "dit vereist, conform artikel 10, tweede lid sub c. De minister heeft "
            "bepaald dat dit ook van toepassing is op BSN-nummers zoals 987654321 "
            "en email-adressen zoals ambtenaar@overheid.nl."
        ),
        "jurisdiction": "nederland",
        "autonomy_level": 2,
    },
    {
        "id": "RW-002",
        "source": "Civiel recht — Overeenkomst",
        "question": "Wat is de betekenis van redelijkheid en billijkheid in het verbintenissenrecht?",
        "answer": (
            "De redelijkheid en billijkheid spelen een centrale rol in het "
            "Nederlandse verbintenissenrecht. Artikel 6:248 BW bepaalt dat een "
            "overeenkomst niet alleen verplichtingen inhoudt die in de wet staan, "
            "maar ook die welke naar de aard van de overeenkomst daaruit voortvloeien. "
            "Een aanbieder kan zich niet beroepen op een beperkingsclausule indien "
            "dit in de gegeven omstandigheden onaanvaardbaar is. Dit is ook van "
            "toepassing op consumentenovereenkomsten conform artikel 6:233 BW. "
            "Bijvoorbeeld: een die een schuld van EUR 50.000 heeft bij "
            "ING Bank NL12ABCD1234567890."
        ),
        "jurisdiction": "nederland",
        "autonomy_level": 3,
    },
    {
        "id": "RW-003",
        "source": "Privacy recht — AVG meldplicht",
        "question": "Wat zijn de verplichtingen bij een datalek?",
        "answer": (
            "Bij een datalek gelden strenge meldplichten. De verwerkingsverantwoordelijke "
            "moet binnen 72 uur na ontdekking melding doen aan de Autoriteit "
            "Persoonsgegevens (AP). Dit is gebaseerd op artikel 33 van de Algemene "
            "Verordening Gegevensbescherming. De melding moet minimaal bevatten: "
            "de aard van het lek, de categorieën betrokkenen, het geschatte aantal, "
            "en de genomen maatregelen. Bij een hoog risico voor de rechten van "
            "betrokkenen moeten ook de betrokkenen zelf worden geïnformeerd "
            "(artikel 34 AVG). De Privacyrichtlijn van 1995 is hier niet meer van "
            "toepassing aangezien de AVG sinds 25 mei 2018 de Europese richtlijn heeft "
            "vervangen. De boete kan oplopen tot 4% van de wereldwijde jaaromzet."
        ),
        "jurisdiction": "nederland",
        "autonomy_level": 2,
    },
    {
        "id": "RW-004",
        "source": "AI Act — Compliance",
        "question": "Is een AI-systeem voor sollicitatie-screening hoog-risico?",
        "answer": (
            "Ja, AI-systemen voor sollicitatie-screening vallen onder de hoog-risico "
            "categorie van de EU AI Act. Dit volgt uit Bijlage III, punt 4 van "
            "Verordening (EU) 2024/1689. Voor hoog-risicosystemen gelden de volgende "
            "vereisten: een risicobeheersysteem conform artikel 9, datagovernance "
            "conform artikel 10, technische documentatie conform artikel 11, en "
            "menselijk toezicht conform artikel 14. Bovendien is een "
            "conformiteitsbeoordeling vereist voordat het systeem op de markt mag "
            "worden gebracht. De deadline voor implementatie is 2 augustus 2026. "
            "De boete voor non-conformiteit kan oplopen tot EUR 15.000.000 of 3% "
            "van de wereldwijde jaaromzet."
        ),
        "jurisdiction": "eu",
        "autonomy_level": 3,
    },
    {
        "id": "RW-005",
        "source": "Strafrecht — Voorwaardelijke straf",
        "question": "Wat zijn de voorwaarden voor een voorwaardelijke straf?",
        "answer": (
            "De rechter kan een voorwaardelijke straf opleggen indien de misdaad "
            "daarvoor geschikt is. Artikel 14a Sr bepaalt dat de hoofdstraf "
            "voorwaardelijk kan worden opgelegd indien de straf niet langer is dan "
            "een gevangenisstraf van een jaar. De voorwaarden omvatten: "
            "gedragingen van de veroordeelde, schadevergoeding, en een "
            "probation-termijn van maximaal 3 jaar. De Hoge Raad heeft in "
            "ECLI:NL:HR:2024:1 bepaald dat de rechter bij de keuze voor een "
            "voorwaardelijke straf rekening moet houden met de persoonlijke "
            "omstandigheden van de verdachte. Het Openbaar Ministerie kan "
            "de voorwaarden wijzigen conform artikel 14c Sr. "
            "Contact: officier@justitie.nl of telefoon 070-1234567."
        ),
        "jurisdiction": "nederland",
        "autonomy_level": 3,
    },
    {
        "id": "RW-006",
        "source": "Internationaal recht — EVRM",
        "question": "Wat is de betekenis van artikel 8 EVRM voor gegevensbescherming?",
        "answer": (
            "Artikel 8 van het Europees Verdrag voor de Rechten van de Mens "
            "beschermt het recht op respect voor het privéleven. Dit omvat ook de "
            "bescherming van persoonsgegevens. De Raad van Europa heeft in het "
            "Verdrag 108+ (geactualiseerd in 2025) specifieke regels vastgesteld "
            "voor gegevensverwerking. Het EHRM heeft in zaak Bărbulescu t. Roemenië "
            "bepaald dat werkgevers toezicht op internetgebruik van werknemers "
            "moeten beperken. De OECD AI Principles zijn hier complementeerend aan, "
            "hoewel deze geen bindende kracht hebben. Het AI Act 2023 is de "
            "bindende EU-regelgeving die artikel 8 EVRM implementeert voor "
            "AI-systemen."
        ),
        "jurisdiction": "eu",
        "autonomy_level": 2,
    },
    {
        "id": "RW-007",
        "source": "Bestuursrecht — AWB beslistermijn",
        "question": "Wat is de beslistermijn voor een bezwaarschrift?",
        "answer": (
            "Het bestuursorgaan moet beslissen op het bezwaarschrift binnen 6 weken "
            "van ontvangst. Dit volgt uit artikel 7:10 van de Algemene wet "
            "bestuursrecht (Awb). De termijn kan eenmaal worden verlengd met "
            "4 weken, mits tijdig geïnformeerd. Indien geen besluit wordt genomen "
            "binnen de termijn, kan de bezwaarde een bezwaarschrift indienen "
            "bij de bestuursrechter. De Afdeling bestuursrechtspraak van de Raad "
            "van State heeft geoordeeld dat het overschrijden van de beslistermijn "
            "niet leidt tot vernietiging van het besluit, maar wel tot een "
            "gedoogplicht. Het bezwaarschrift moet worden ingediend bij het "
            "betrokken bestuursorgaan."
        ),
        "jurisdiction": "nederland",
        "autonomy_level": 2,
    },
    {
        "id": "RW-008",
        "source": "Fiscaal recht — Belastingaangifte",
        "question": "Wat zijn de deadlines voor de belastingaangifte?",
        "answer": (
            "De belastingaangifte voor een kalenderjaar moet worden ingediend "
            "vóór 1 maart van het daaropvolgende jaar. Dit volgt uit de Algemene "
            "wet inzake rijksbelastingen. De Belastingdienst kan een verlening "
            "verlenen tot 1 mei. Bij geboekte aangifte kan de inspecteur "
            "nader inlichtingen vragen. De bezwaartermijn bedraagt 6 weken na "
            "dagte van de aanslag. De Hoge Raad heeft bepaald dat de "
            "bewijslast bij de inspecteur ligt voor de juistheid van de aanslag. "
            "Het BSN van de belastingplichtige wordt gebruikt voor verificatie: "
            "bijvoorbeeld 123456789."
        ),
        "jurisdiction": "nederland",
        "autonomy_level": 2,
    },
]


def run_real_world_audit() -> dict:
    """Run JLAIF audit on real-world Dutch legal texts."""
    all_results = []
    total_findings = 0
    total_pii = 0
    total_jurisdiction_issues = 0
    total_temporal_issues = 0

    print("=" * 70)
    print("JLAIF — Real-World Audit op Nederlandse juridische teksten")
    print("=" * 70)
    print()

    for case in REAL_WORLD_CASES:
        uc = UseCaseProfile(
            name=case["id"],
            autonomy_level=case["autonomy_level"],
            legal_domain="algemeen",
            user_group="advocaat",
        )

        # JLAIF audit
        report = rag_engine_auditor.audit(
            question=case["question"],
            answer=case["answer"],
            expected_jurisdiction=case["jurisdiction"],
            use_case=uc,
        )

        # PII check
        pii_result = pii_redaction.audit_only(case["answer"])

        # Jurisdiction check
        jur_result = jurisdiction_classifier.classify(case["answer"])

        # Citation check
        cit_result = citation_verifier.verify(case["answer"])

        # Temporal check
        temp_result = temporal_checker.check(case["answer"])

        # Aggregate findings
        case_findings = len(report.findings)
        case_pii = len(pii_result.detections)
        case_jur_issues = len(jur_result.warnings)
        case_temp_issues = temp_result.outdated_count

        total_findings += case_findings
        total_pii += case_pii
        total_jurisdiction_issues += case_jur_issues
        total_temporal_issues += case_temp_issues

        print(f"{case['id']}: {case['source']}")
        print(
            f"  Bevindingen: {case_findings} | PII: {case_pii} | "
            f"Jurisdictie: {case_jur_issues} | Temporeel: {case_temp_issues}"
        )
        print(
            f"  Release: {report.release_decision} | "
            f"Jurisdictie: {jur_result.primary} ({jur_result.confidence:.2f})"
        )
        print(
            f"  Citaties: {cit_result.citation_rate:.0%} | "
            f"PII densiteit: {pii_result.pii_density:.1f}%"
        )

        for f in report.findings:
            print(
                f"    [{f.severity.value}] {f.error_type.value}: {f.description[:60]}"
            )
        for d in pii_result.detections:
            print(f"    [PII] {d.pii_type}: {d.description}")
        for finding in temp_result.findings:
            print(f"    [TEMP] {finding.description[:60]}")

        print()

        all_results.append(
            {
                "case_id": case["id"],
                "source": case["source"],
                "release_decision": report.release_decision,
                "findings_count": case_findings,
                "pii_count": case_pii,
                "jurisdiction": jur_result.primary,
                "citation_rate": cit_result.citation_rate,
                "temporal_issues": case_temp_issues,
            }
        )

    # ─── Summary ─────────────────────────────────────────────────
    print("=" * 70)
    print("AGGREGAAT RAPPORT")
    print("=" * 70)
    print()

    total_cases = len(REAL_WORLD_CASES)
    nogo = sum(1 for r in all_results if r["release_decision"] == "NO-GO")
    go = total_cases - nogo

    print(f"Totaal cases:        {total_cases}")
    print(f"Totaal bevindingen:  {total_findings}")
    print(f"PII detecties:       {total_pii}")
    print(f"Jurisdictie issues:  {total_jurisdiction_issues}")
    print(f"Temporele issues:    {total_temporal_issues}")
    print(
        f"NO-GO:               {nogo}/{total_cases} ({nogo / total_cases * 100:.0f}%)"
    )
    print(f"GO:                  {go}/{total_cases} ({go / total_cases * 100:.0f}%)")
    print()
    print(f"Gem. bevindingen/case: {total_findings / total_cases:.1f}")
    print(f"Gem. PII/case:         {total_pii / total_cases:.1f}")

    output = {
        "audit_type": "real_world_jlaif",
        "timestamp": all_results[0]["source"] if all_results else "",
        "total_cases": total_cases,
        "total_findings": total_findings,
        "total_pii": total_pii,
        "jurisdiction_issues": total_jurisdiction_issues,
        "temporal_issues": total_temporal_issues,
        "nogo_rate": nogo / total_cases,
        "results": all_results,
    }

    output_path = Path(__file__).parent / "real-world-audit-report.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nRapport opgeslagen: {output_path}")

    return output


if __name__ == "__main__":
    run_real_world_audit()
