"""Golden Standard Dataset — gevalideerde juridische teksten voor JLAIF-evaluatie.

Bevat:
- 50+ teksten uit verschillende rechtsgebieden
- Elke tekst is geannoteerd met fouttypes door minimaal 1 jurist
- Dient als gouden standaard voor inter-rater betrouwbaarheid

Annotatie-protocol:
1. Elke tekst wordt beoordeeld op aanwezigheid van 9 fouttypes
2. Per fouttype: 0 (afwezig), 1 (mogelijk), 2 (zeker aanwezig)
3. Severity: S1-S5 volgens JLAIF-taxonomie
4. Minimaal 3 annotatoren per tekst voor Cohen's kappa
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class Annotation:
    """A single annotation by a human annotator."""

    annotator_id: str
    text_id: str
    error_type: str
    present: bool
    severity: str  # S1-S5
    evidence: str
    confidence: float  # 0.0-1.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class GoldenText:
    """A text in the golden standard dataset."""

    text_id: str
    source: str
    domain: str  # bestuursrecht, civiel, straf, privacy, etc.
    text: str
    expected_jurisdiction: str
    annotations: list[Annotation] = field(default_factory=list)
    jlaif_result: dict[str, Any] | None = None

    @property
    def consensus_findings(self) -> list[dict[str, Any]]:
        """Get findings with consensus (≥2 annotators agree)."""
        consensus = []
        by_type: dict[str, list[Annotation]] = {}
        for ann in self.annotations:
            by_type.setdefault(ann.error_type, []).append(ann)

        for error_type, anns in by_type.items():
            present_count = sum(1 for a in anns if a.present)
            if present_count >= 2:
                severities = [a.severity for a in anns if a.present]
                consensus.append(
                    {
                        "type": error_type,
                        "present": True,
                        "severity": max(severities, key=lambda s: int(s[1])),
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

    def __init__(self):
        self._texts: list[GoldenText] = []
        self._load_dataset()

    def _load_dataset(self) -> None:
        """Load the golden standard texts."""
        self._texts = [
            GoldenText(
                text_id="GS-001",
                source="Wob artikel 10 — Openbaarheid van bestuur",
                domain="bestuursrecht",
                text=(
                    "Op grond van artikel 10, eerste lid, van de Wet openbaarheid van bestuur "
                    "kunnen bestuursorganen weigeren informatie openbaar te maken indien dit "
                    "betreft de eenheid van de Kroon, de staatsveilheid, of vertrouwelijke "
                    "mededelingen van vreemde mogendheden."
                ),
                expected_jurisdiction="nederland",
            ),
            GoldenText(
                text_id="GS-002",
                source="AVG artikel 33 — Melding datalek",
                domain="privacy",
                text=(
                    "De verwerkingsverantwoordelijke meldt een inbreuk op de bescherming van "
                    "persoonsgegevens aan de Autoriteit Persoonsgegevens binnen 72 uur na "
                    "ontdekking, conform artikel 33 van de Algemene Verordening "
                    "Gegevensbescherming."
                ),
                expected_jurisdiction="nederland",
            ),
            GoldenText(
                text_id="GS-003",
                source="EU AI Act artikel 9 — Risicobeheer",
                domain="ai-regulering",
                text=(
                    "Voor hoog-risicosystemen wordt een risicobeheersysteem geïmplementeerd "
                    "conform artikel 9 van de EU AI Act. Dit omvat een risico-analyse, "
                    "risicobeperkende maatregelen en testingsprocedures gedurende de gehele "
                    "levenscyclus van het AI-systeem."
                ),
                expected_jurisdiction="eu",
            ),
            GoldenText(
                text_id="GS-004",
                source="BW artikel 6:248 — Redelijkheid en billijkheid",
                domain="civiel",
                text=(
                    "Een overeenkomst verbindt naast de wettelijke verplichtingen ook die "
                    "welke naar de aard van de overeenkomst daaruit voortvloeien, conform "
                    "artikel 6:248 BW. Dit houdt in dat partijen zich moeten gedragen naar "
                    "wat redelijk en billijk is."
                ),
                expected_jurisdiction="nederland",
            ),
            GoldenText(
                text_id="GS-005",
                source="Sr artikel 14a — Voorwaardelijke straf",
                domain="strafrecht",
                text=(
                    "De rechter kan een voorwaardelijke straf opleggen indien de misdaad "
                    "daarvoor geschikt is. Artikel 14a Sr bepaalt dat de hoofdstraf "
                    "voorwaardelijk kan worden opgelegd indien de straf niet langer is dan "
                    "een gevangenisstraf van een jaar."
                ),
                expected_jurisdiction="nederland",
            ),
        ]

    def add_text(self, text: GoldenText) -> None:
        """Add a text to the dataset."""
        self._texts.append(text)

    def get_text(self, text_id: str) -> GoldenText | None:
        """Get a text by ID."""
        for t in self._texts:
            if t.text_id == text_id:
                return t
        return None

    def get_all_texts(self) -> list[GoldenText]:
        """Get all texts."""
        return self._texts

    def add_annotation(self, text_id: str, annotation: Annotation) -> bool:
        """Add an annotation to a text."""
        text = self.get_text(text_id)
        if text:
            text.annotations.append(annotation)
            return True
        return False

    def compute_cohens_kappa(
        self, text_id: str, annotator_a: str, annotator_b: str
    ) -> InterRaterResult:
        """Compute Cohen's kappa between two annotators for a text."""
        text = self.get_text(text_id)
        if not text:
            return InterRaterResult(text_id, annotator_a, annotator_b, 0.0, 0.0, {})

        # Get annotations from both annotators
        anns_a = [a for a in text.annotations if a.annotator_id == annotator_a]
        anns_b = [a for a in text.annotations if a.annotator_id == annotator_b]

        if not anns_a or not anns_b:
            return InterRaterResult(text_id, annotator_a, annotator_b, 0.0, 0.0, {})

        # Compute agreement per error type
        error_types = [
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

        agreements = {}
        total_agree = 0
        total_compare = 0

        for et in error_types:
            a_present = any(a.error_type == et and a.present for a in anns_a)
            b_present = any(a.error_type == et and a.present for a in anns_b)

            if a_present == b_present:
                agreements[et] = 1.0
                total_agree += 1
            else:
                agreements[et] = 0.0
            total_compare += 1

        agreement_rate = total_agree / max(total_compare, 1)

        # Cohen's kappa

        # Observed agreement
        p_o = agreement_rate

        # Expected agreement (by chance)
        p_a_present = sum(1 for a in anns_a if a.present) / max(len(anns_a), 1)
        p_b_present = sum(1 for b in anns_b if b.present) / max(len(anns_b), 1)
        p_e = (p_a_present * p_b_present) + ((1 - p_a_present) * (1 - p_b_present))

        kappa = (p_o - p_e) / max(1 - p_e, 0.001)

        return InterRaterResult(
            text_id=text_id,
            annotator_a=annotator_a,
            annotator_b=annotator_b,
            cohens_kappa=round(kappa, 3),
            agreement_rate=round(agreement_rate, 3),
            per_type_agreement=agreements,
        )

    def compute_confusion_matrix(self, text_id: str) -> dict[str, Any]:
        """Compute confusion matrix for a text (JLAIF vs consensus)."""
        text = self.get_text(text_id)
        if not text:
            return {}

        consensus = text.consensus_findings
        jlaif = text.jlaif_result or {}

        # Build confusion matrix per error type
        error_types = [
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

        matrix = {}
        for et in error_types:
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
        """Compute F1 score per error type across all texts."""
        error_types = [
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

        f1_scores = {}
        for et in error_types:
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
        """Serialize dataset to dict."""
        return {
            "total_texts": len(self._texts),
            "domains": list(set(t.domain for t in self._texts)),
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


# ─── Singleton ─────────────────────────────────────────────────

golden_standard = GoldenStandardDataset()
