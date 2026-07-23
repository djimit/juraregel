"""Golden Standard Dataset — uitgebreide dataset met 50+ juridische teksten.

Elke tekst heeft:
- Unieke ID, bron, domein, verwachte jurisdictie
- Annotaties voor de 9 fouttypes (gesimuleerd voor demo)
- Consensus berekening voor inter-rater betrouwbaarheid
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class GoldenText:
    """A text in the golden standard dataset."""

    text_id: str
    source: str
    domain: str
    text: str
    expected_jurisdiction: str
    annotations: list[dict[str, Any]] = field(default_factory=list)
    jlaif_result: dict[str, Any] | None = None

    @property
    def consensus_findings(self) -> list[dict[str, Any]]:
        """Get findings with consensus (≥2 annotators agree)."""
        consensus = []
        by_type: dict[str, list[dict]] = {}
        for ann in self.annotations:
            by_type.setdefault(ann["error_type"], []).append(ann)

        for error_type, anns in by_type.items():
            present_count = sum(1 for a in anns if a.get("present", False))
            if present_count >= 2:
                severities = [a.get("severity", "S1") for a in anns if a.get("present")]
                consensus.append(
                    {
                        "type": error_type,
                        "present": True,
                        "severity": max(severities, key=lambda s: int(s[1]))
                        if severities
                        else "S1",
                        "annotator_count": present_count,
                        "total_annotators": len(anns),
                    }
                )

        return consensus


@dataclass
class InterRaterResult:
    """Result of inter-rater reliability analysis."""

    text_id: str
    annotator_a: str
    annotator_b: str
    cohens_kappa: float
    agreement_rate: float
    per_type_agreement: dict[str, float]


class GoldenStandardDataset:
    """Manages the golden standard dataset."""

    ERROR_TYPES = [
        "feitelijke_fout",
        "bronfout",
        "interpretatiefout",
        "jurisdictiefout",
        "temporaliteitsfout",
        "procedurefout",
        "omissiefout",
        "bias_ongelijke_behandeling",
        "vertrouwelijkheidsincident",
    ]

    DOMAINS = [
        "bestuursrecht",
        "civiel",
        "strafrecht",
        "privacy",
        "ai-regulering",
        "fiscaal",
        "internationaal",
        "arbeidsrecht",
        "omgevingsrecht",
        "bestuursstrafrecht",
    ]

    def __init__(self):
        self._texts: list[GoldenText] = []
        self._load_dataset()

    def _load_dataset(self) -> None:
        """Load the golden standard texts."""
        self._texts = [
            # ─── Bestuursrecht (1-8) ──────────────────────────────
            GoldenText(
                "GS-001",
                "Wob artikel 10 — Openbaarheid",
                "bestuursrecht",
                "Op grond van artikel 10, eerste lid, van de Wet openbaarheid van bestuur kunnen bestuursorganen weigeren informatie openbaar te maken indien dit betreft de eenheid van de Kroon, de staatsveilheid, of vertrouwelijke mededelingen van vreemde mogendheden.",
                "nederland",
            ),
            GoldenText(
                "GS-002",
                "Awb artikel 7:10 — Beslistermijn bezwaarschrift",
                "bestuursrecht",
                "Het bestuursorgaan moet beslissen op het bezwaarschrift binnen 6 weken van ontvangst. De termijn kan eenmaal worden verlengd met 4 weken, mits tijdig geïnformeerd.",
                "nederland",
            ),
            GoldenText(
                "GS-003",
                "Awb artikel 4:19 — Ambtshalve vernietiging",
                "bestuursrecht",
                "Het bestuursorgaan kan een besluit ambtshalve vernietigen indien het in strijd is met een rechtsregel. De vernietiging kan met terugwerkende kracht geschieden.",
                "nederland",
            ),
            GoldenText(
                "GS-004",
                "Wob artikel 11 — Persoonsgegevens uitzondering",
                "bestuursrecht",
                "Informatie die persoonsgegevens bevat kan worden geweigerd indien openbaarheid niet in verhouding zou staan tot de privacy van de betrokkene.",
                "nederland",
            ),
            GoldenText(
                "GS-005",
                "Awb artikel 2:3 — Algemene beginselen van behoorlijk bestuur",
                "bestuursrecht",
                "Bij de voorbereiding van een besluit behoort het bestuursorgaan een behoorlijk onderzoek te doen. Het zorgbeginsel vereist dat alle relevante feiten en belangen worden meegenomen.",
                "nederland",
            ),
            GoldenText(
                "GS-006",
                "Wet ruimtelijke ordening artikel 2.1 — Bestemmingsplan",
                "omgevingsrecht",
                "De gemeenteraad stelt een bestemmingsplan vast voor het grondgebied van de gemeente. Het plan bevat bestemmingen voor wonen, werken, recreatie en natuur.",
                "nederland",
            ),
            GoldenText(
                "GS-007",
                "Wet milieubeheer artikel 8.10 — Vergunning",
                "omgevingsrecht",
                "Het college van burgemeester en wethouders verleent een milieuvergunning voor een inrichting. De vergunning stelt eisen aan emissies en geluid.",
                "nederland",
            ),
            GoldenText(
                "GS-008",
                "Awb artikel 6:2 — Belanghebbenden",
                "bestuursrecht",
                "Bij de voorbereiding van een besluit behoort het bestuursorgaan de belangbbenden te horen. Dit geldt voor zover hun belangen rechtstreeks bij het besvuit betrokken zijn.",
                "nederland",
            ),
            # ─── Privacy (9-14) ───────────────────────────────────
            GoldenText(
                "GS-009",
                "AVG artikel 33 — Melding datalek",
                "privacy",
                "De verwerkingsverantwoordelijke meldt een inbreuk op de bescherming van persoonsgegevens aan de Autoriteit Persoonsgegevens binnen 72 uur na ontdekking, conform artikel 33 van de Algemene Verordening Gegevensbescherming.",
                "nederland",
            ),
            GoldenText(
                "GS-010",
                "AVG artikel 15 — Recht op inzage",
                "privacy",
                "De betrokkene heeft het recht om van de verwerkingsverantwoordelijke een bevestiging te verkrijgen of persoonsgegevens betreffende hem worden verwerkt en heeft in dat geval toegang tot die gegevens.",
                "nederland",
            ),
            GoldenText(
                "GS-011",
                "AVG artikel 17 — Recht op vergetelheid",
                "privacy",
                "De betrokkene heeft het recht om van de verwerkingsverantwoordelijke de wissing van hem betreffende persoonsgegevens te verkrijgen. Dit recht is niet absoluut en kan worden beperkt door andere wettelijke verplichtingen.",
                "nederland",
            ),
            GoldenText(
                "GS-012",
                "AVG artikel 35 — DPIA",
                "privacy",
                "Wanneer een verwerking waarschijnlijk een hoog risico inhoudt voor de rechten en vrijheden van natuurlijke personen, verricht de verwerkingsverantwoordelijke een beoordeling van de gevolgen van de verwerking.",
                "nederland",
            ),
            GoldenText(
                "GS-013",
                "AVG artikel 27 — FRIA",
                "privacy",
                "Voor hoog-risico AI-systemen is een Fundamental Rights Impact Assessment verplicht vóór inzet. De FRIA beoordeelt de impact op grondrechten zoals non-discriminatie en privacy.",
                "eu",
            ),
            GoldenText(
                "GS-014",
                "Privacyrichtlijn 1995 — Verouderde verwijzing",
                "privacy",
                "De Privacyrichtlijn uit 1995 is hier van toepassing. De richtlijn is vervangen door de AVG sinds 25 mei 2018.",
                "nederland",
            ),
            # ─── AI-regulering (15-20) ────────────────────────────
            GoldenText(
                "GS-015",
                "EU AI Act artikel 9 — Risicobeheer",
                "ai-regulering",
                "Voor hoog-risicosystemen wordt een risicobeheersysteem geïmplementeerd conform artikel 9 van de EU AI Act. Dit omvat een risico-analyse, risicobeperkende maatregelen en testingsprocedures gedurende de gehele levenscyclus van het AI-systeem.",
                "eu",
            ),
            GoldenText(
                "GS-016",
                "EU AI Act artikel 14 — Menselijk toezicht",
                "ai-regulering",
                "AI-systemen moeten zodanig worden ontworpen dat effectieve menselijke tussenkomst mogelijk is. De gebruiker moet in staat zijn om het AI-systeem te overschrijven of stop te zetten.",
                "eu",
            ),
            GoldenText(
                "GS-017",
                "EU AI Act artikel 10 — Data governance",
                "ai-regulering",
                "Trainings-, validatie- en testdata moeten relevant, voldoende representatief en zo vrij mogelijk van fouten. Bias in data moet worden geïdentificeerd en gemitigeerd.",
                "eu",
            ),
            GoldenText(
                "GS-018",
                "EU AI Act artikel 5 — Verboden praktijken",
                "ai-regulering",
                "Bepaalde AI-praktijken zijn verboden, waaronder subliminale technieken, exploitatie van zwakheden, en sociale scoring door overheden.",
                "eu",
            ),
            GoldenText(
                "GS-019",
                "EU AI Act artikel 13 — Transparantie",
                "ai-regulering",
                "AI-systemen moeten zodanig worden ontworpen dat de output voor de gebruiker transparant en begrijpelijk is. De gebruiker moet worden geïnformeerd dat hij met een AI-systeem communiceert.",
                "eu",
            ),
            GoldenText(
                "GS-020",
                "AI Act 2023 — Verouderde verwijzing",
                "ai-regulering",
                "Het AI Act 2023 is hier van toepassing. De verordening is Verordening (EU) 2024/1689 en is in werking sinds 1 augustus 2024.",
                "eu",
            ),
            # ─── Civiel recht (21-26) ─────────────────────────────
            GoldenText(
                "GS-021",
                "BW artikel 6:248 — Redelijkheid en billijkheid",
                "civiel",
                "Een overeenkomst verbindt naast de wettelijke verplichtingen ook die welke naar de aard van de overeenkomst daaruit voortvloeien, conform artikel 6:248 BW.",
                "nederland",
            ),
            GoldenText(
                "GS-022",
                "BW artikel 6:213 — Overeenkomst",
                "civiel",
                "Een overeenkomst wordt gevormd door een aanvaarding van een aanbod. De overeenkomst heeft de werking tussen partijen die is overeengekomen.",
                "nederland",
            ),
            GoldenText(
                "GS-023",
                "BW artikel 6:74 — Onrechtmatige daad",
                "civiel",
                "Hij die jegens een ander een onrechtmatige daad pleegt, is verplicht de schade die de ander daardoor lijdt te vergoeden. Een onrechtmatige daad kan bestaan uit een inbreuk op een recht.",
                "nederland",
            ),
            GoldenText(
                "GS-024",
                "BW artikel 7:611 — Arbeidsovereenkomst",
                "arbeidsrecht",
                "De arbeidsovereenkomst verplicht de werknemer tot het verrichten van arbeid voor de werkgever. De werkgever is verplicht het loon te betalen en zorg te dragen voor een veilige werkomgeving.",
                "nederland",
            ),
            GoldenText(
                "GS-025",
                "BW artikel 7:658 — Werkgeversaansprakelijkheid",
                "arbeidsrecht",
                "De werkgever is jegens de werknemer aansprakelijk voor schade die de werknemer in de uitoefening van zijn arbeid lijdt. Deze aansprakelijkheid kan worden uitgesloten door een beding.",
                "nederland",
            ),
            GoldenText(
                "GS-026",
                "BW artikel 9:104 — Onrechtmatige daad buiten overeenkomst",
                "civiel",
                "De schadeverplichting ontstaat niet alleen uit overeenkomst maar ook uit onrechtmatige daad. De rechter kan de schadevergoeding matigen indien toerekening in redelijkheid niet kan geschieden.",
                "nederland",
            ),
            # ─── Strafrecht (27-32) ───────────────────────────────
            GoldenText(
                "GS-027",
                "Sr artikel 14a — Voorwaardelijke straf",
                "strafrecht",
                "De rechter kan een voorwaardelijke straf opleggen indien de misdaad daarvoor geschikt is. Artikel 14a Sr bepaalt dat de hoofdstraf voorwaardelijk kan worden opgelegd indien de straf niet langer is dan een gevangenisstraf van een jaar.",
                "nederland",
            ),
            GoldenText(
                "GS-028",
                "Sr artikel 33 — Melding strafbaar feit",
                "strafrecht",
                "Een ieder die kennis heeft van een strafbaar feit kan dit melden bij de politie. De melding kan anoniem worden gedaan.",
                "nederland",
            ),
            GoldenText(
                "GS-029",
                "Sv artikel 55 — Voorlopige hechtenis",
                "strafrecht",
                "De rechter-commissaris kan een bevel tot voorlopige hechtenis geven indien er gegronde verdenking van een misdrijf. De voorlopige hechtenis kan worden opgehecht indien de vervalgronden vervallen.",
                "nederland",
            ),
            GoldenText(
                "GS-030",
                "Sr artikel 41 — TBS",
                "strafrecht",
                "De rechter kan een maatregel van terbeschikkingstelling opleggen indien de verdachte lijdt aan een geestesstoornis. De TBS kan worden verlengd met telkens maximaal 2 jaar.",
                "nederland",
            ),
            GoldenText(
                "GS-031",
                "Wetboek van Strafrecht artikel 293 — Doodslag",
                "strafrecht",
                "Doodslag wordt gestraft met levenslange gevangenisstraf of gevangenisstraf van ten hoogste 30 jaar. Poging tot doodslag wordt gestraft met gevangenisstraf van ten hoogste 15 jaar.",
                "nederland",
            ),
            GoldenText(
                "GS-032",
                "Sr artikel 350 — Schadevergoeding in strafzaak",
                "strafrecht",
                "De rechter kan in de strafzaak een schadevergoedingsmaatregel opleggen. De schadevergoeding wordt vastgesteld op basis van de geleden schade.",
                "nederland",
            ),
            # ─── Fiscaal recht (33-37) ────────────────────────────
            GoldenText(
                "GS-033",
                "AWR artikel 1 — Algemene wet rijksbelastingen",
                "fiscaal",
                "De belastingplichtige is verplicht aangifte te doen van zijn inkomen. De inspecteur van de belastingen kan de aangifte navorderen binnen 5 jaar na het kalenderjaar.",
                "nederland",
            ),
            GoldenText(
                "GS-034",
                "IB-wet 1990 — Inkomstenbelasting",
                "fiscaal",
                "De inkomstenbelasting wordt geheven over het inkomen van natuurlijke personen. Het tarief is progressief: 36,97% tot EUR 75.518 en 49,50% daarboven (2024).",
                "nederland",
            ),
            GoldenText(
                "GS-035",
                "Vpb-wet 1969 — Vennootschapsbelasting",
                "fiscaal",
                "De vennootschapsbelasting wordt geheven over de winst van rechtspersonen. Het tarief is 19% over de eerste EUR 200.000 en 25,8% daarboven (2024).",
                "nederland",
            ),
            GoldenText(
                "GS-036",
                "Wbtv 1990 — Wet belastingen op diensten",
                "fiscaal",
                "De belasting over de toegevoegde waarde wordt geheven over leveringen en diensten. Het algemene BTW-tarief is 21% (2024).",
                "nederland",
            ),
            GoldenText(
                "GS-037",
                "Invorderingswet 1990 — Belastinginvordering",
                "fiscaal",
                "De inspecteur kan een dwangbrief uitbrengen indien de belastingplichtige niet betaalt. De dwangbrief geeft bevoegdheid tot beslag op goederen en inkomsten.",
                "nederland",
            ),
            # ─── Internationaal recht (38-42) ──────────────────────
            GoldenText(
                "GS-038",
                "EVRM artikel 8 — Recht op privéleven",
                "internationaal",
                "Een ieder heeft recht op respect voor zijn privéleven. Dit omvat ook de bescherming van persoonsgegevens. De Raad van Europa heeft Verdrag 108+ vastgesteld.",
                "eu",
            ),
            GoldenText(
                "GS-039",
                "EVRM artikel 6 — Recht op een eerlijk proces",
                "internationaal",
                "Een ieder heeft recht op een eerlijke en openbare behandeling van zijn zaak. Dit omvat de toegang tot de rechter en de mogelijkheid om zich te verdedigen.",
                "eu",
            ),
            GoldenText(
                "GS-040",
                "OECD AI Principles — AI-governance",
                "internationaal",
                "De OECD AI Principles bevatten vijf principes voor verantwoorde AI: inclusieve groei, menselijke waarden, transparantie, robuustheid en verantwoordelijkheid.",
                "internationaal",
            ),
            GoldenText(
                "GS-041",
                "Council of Europe AI Treaty — AI-verdrag",
                "internationaal",
                "Het Verdrag inzake kunstmatige intelligentie van de Raad van Europa is het eerste internationale verdrag over AI. Het verdrag is ondertekend door 46 lidstaten.",
                "internationaal",
            ),
            GoldenText(
                "GS-042",
                "UK Data Protection Act 2018 — UK privacy",
                "internationaal",
                "Het UK Data Protection Act 2018 implementeert de GDPR in het Verenigd Koninkrijk. Na Brexit is de UK-GDPR in werking getreden met gelijkbepalingen.",
                "internationaal",
            ),
            # ─── Bestuursstrafrecht (43-46) ────────────────────────
            GoldenText(
                "GS-043",
                "Wet bestuursstrafrecht artikel 1 — Bestuurlijke straf",
                "bestuursstrafrecht",
                "Een bestuurlijke sanctie kan worden opgelegd voor een overtreding. De sanctie kan bestaan uit een bestuursboete van ten hoogste EUR 410.000.",
                "nederland",
            ),
            GoldenText(
                "GS-044",
                "Wet milieubeheer artikel 18.13 — Milieuboete",
                "bestuursstrafrecht",
                "Het college kan een bestuursboete opleggen voor overtreding van milieuregels. De boete kan oplopen tot EUR 410.000.",
                "nederland",
            ),
            GoldenText(
                "GS-045",
                "Wet economische delicten — Economische sanctie",
                "bestuursstrafrecht",
                "De economische sanctie kan worden opgelegd voor overtreding van economische regels. De sanctie kan bestaan uit een geldboete of ontneming van het wederrechtelijk verkregen voordeel.",
                "nederland",
            ),
            GoldenText(
                "GS-046",
                "Wet op de belastingen — Fiscale sanctie",
                "bestuursstrafrecht",
                "De inspecteur kan een fiscale sanctie opleggen voor onjuiste aangifte. De sanctie kan bestaan uit een verhoging van de belasting van ten hoogste 100%.",
                "nederland",
            ),
            # ─── Arbeidsrecht (47-50) ──────────────────────────────
            GoldenText(
                "GS-047",
                "BW artikel 7:629 — Ontslag",
                "arbeidsrecht",
                "De werkgever kan de arbeidsovereenkomst ontbinden met toestemming van het UWV of vonnis van de kantonrechter. De opzegtermijn is minimaal 1 maand.",
                "nederland",
            ),
            GoldenText(
                "GS-048",
                "BW artikel 7:669 — Transitievergoeding",
                "arbeidsrecht",
                "Bij ontslag heeft de werknemer recht op een transitievergoeding. De vergoeding bedraagt 1/3 maandsalaris per gewerkt jaar.",
                "nederland",
            ),
            GoldenText(
                "GS-049",
                "BW artikel 7:671a — Onredelijk ontslag",
                "arbeidsrecht",
                "Ontslag is onredelijk indien het plaatsvindt zonder redelijke grond of indien de gevolgen voor de werknemer onevenredig zijn. De rechter kan herstel of vergoeding toekennen.",
                "nederland",
            ),
            GoldenText(
                "GS-050",
                "Ziektewet artikel 3 — Ziekteverzuim",
                "arbeidsrecht",
                "De werkgever is verplicht de werknemer tijdens ziekte door te betalen. De doorbetalingsplicht bedraagt minimaal 70% van het loon gedurende 104 weken.",
                "nederland",
            ),
            # ─── Extra cases met PII (51-55) ──────────────────────
            GoldenText(
                "GS-051",
                "AVG casus — PII-lek met BSN",
                "privacy",
                "De patiënt met BSN 987654321 heeft recht op inzage in zijn medisch dossier. Contact via jan.de.vries@email.nl of telefoon 06-12345678.",
                "nederland",
            ),
            GoldenText(
                "GS-052",
                "Civiel casus — IBAN in vonnis",
                "civiel",
                "De eiser heeft een vordering van EUR 50.000 tegen de gedaagde. Betaling dient te geschieden op rekening NL12ABCD1234567890 bij ING Bank.",
                "nederland",
            ),
            GoldenText(
                "GS-053",
                "Straf casus — PII in strafvordering",
                "strafrecht",
                "De verdachte, geboren op 15-03-1985, woont aan de Hoofdstraat 12, 1000 AB Amsterdam. Zijn BSN is 123456789.",
                "nederland",
            ),
            GoldenText(
                "GS-054",
                "Fiscaal casus — PII in belastingbrief",
                "fiscaal",
                "De belastingplichtige met BSN 111222333 heeft een inkomen van EUR 75.000. Contact via belastingplichtige@email.nl.",
                "nederland",
            ),
            GoldenText(
                "GS-055",
                "Bestuursrecht casus — PII in besluit",
                "bestuursrecht",
                "Het besluit is gericht aan de aanvrager met BSN 444555666. De aanvrager kan bezwaar maken binnen 6 weken.",
                "nederland",
            ),
        ]

    def add_text(self, text: GoldenText) -> None:
        self._texts.append(text)

    def get_text(self, text_id: str) -> GoldenText | None:
        for t in self._texts:
            if t.text_id == text_id:
                return t
        return None

    def get_all_texts(self) -> list[GoldenText]:
        return self._texts

    def get_texts_by_domain(self, domain: str) -> list[GoldenText]:
        return [t for t in self._texts if t.domain == domain]

    def add_annotation(self, text_id: str, annotation: dict) -> bool:
        text = self.get_text(text_id)
        if text:
            text.annotations.append(annotation)
            return True
        return False

    def compute_cohens_kappa(
        self, text_id: str, annotator_a: str, annotator_b: str
    ) -> InterRaterResult:
        text = self.get_text(text_id)
        if not text:
            return InterRaterResult(text_id, annotator_a, annotator_b, 0.0, 0.0, {})

        anns_a = [a for a in text.annotations if a.get("annotator_id") == annotator_a]
        anns_b = [a for a in text.annotations if a.get("annotator_id") == annotator_b]

        if not anns_a or not anns_b:
            return InterRaterResult(text_id, annotator_a, annotator_b, 0.0, 0.0, {})

        agreements = {}
        total_agree = 0
        total_compare = 0

        for et in self.ERROR_TYPES:
            a_present = any(
                a.get("error_type") == et and a.get("present") for a in anns_a
            )
            b_present = any(
                b.get("error_type") == et and b.get("present") for b in anns_b
            )

            if a_present == b_present:
                agreements[et] = 1.0
                total_agree += 1
            else:
                agreements[et] = 0.0
            total_compare += 1

        agreement_rate = total_agree / max(total_compare, 1)

        p_a_present = sum(1 for a in anns_a if a.get("present")) / max(len(anns_a), 1)
        p_b_present = sum(1 for b in anns_b if b.get("present")) / max(len(anns_b), 1)
        p_e = (p_a_present * p_b_present) + ((1 - p_a_present) * (1 - p_b_present))

        kappa = (agreement_rate - p_e) / max(1 - p_e, 0.001)

        return InterRaterResult(
            text_id=text_id,
            annotator_a=annotator_a,
            annotator_b=annotator_b,
            cohens_kappa=round(kappa, 3),
            agreement_rate=round(agreement_rate, 3),
            per_type_agreement=agreements,
        )

    def compute_confusion_matrix(self, text_id: str) -> dict[str, Any]:
        text = self.get_text(text_id)
        if not text:
            return {}

        consensus = text.consensus_findings
        jlaif = text.jlaif_result or {}

        matrix = {}
        for et in self.ERROR_TYPES:
            consensus_present = any(c["type"] == et for c in consensus)
            jlaif_present = any(f.get("type") == et for f in jlaif.get("findings", []))

            if consensus_present and jlaif_present:
                matrix[et] = "TP"
            elif not consensus_present and not jlaif_present:
                matrix[et] = "TN"
            elif not consensus_present and jlaif_present:
                matrix[et] = "FP"
            else:
                matrix[et] = "FN"

        return matrix

    def compute_f1_per_type(self) -> dict[str, float]:
        f1_scores = {}
        for et in self.ERROR_TYPES:
            tp = fp = fn = 0
            for text in self._texts:
                consensus = text.consensus_findings
                jlaif = text.jlaif_result or {}

                consensus_present = any(c["type"] == et for c in consensus)
                jlaif_present = any(
                    f.get("type") == et for f in jlaif.get("findings", [])
                )

                if consensus_present and jlaif_present:
                    tp += 1
                elif not consensus_present and jlaif_present:
                    fp += 1
                elif consensus_present and not jlaif_present:
                    fn += 1

            precision = tp / max(tp + fp, 1)
            recall = tp / max(tp + fn, 1)
            f1 = 2 * (precision * recall) / max(precision + recall, 0.001)
            f1_scores[et] = round(f1, 2)

        return f1_scores

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_texts": len(self._texts),
            "domains": list(set(t.domain for t in self._texts)),
            "jurisdictions": list(set(t.expected_jurisdiction for t in self._texts)),
            "texts": [
                {
                    "text_id": t.text_id,
                    "source": t.source,
                    "domain": t.domain,
                    "expected_jurisdiction": t.expected_jurisdiction,
                    "annotation_count": len(t.annotations),
                }
                for t in self._texts
            ],
        }


golden_standard = GoldenStandardDataset()
