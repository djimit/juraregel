"""Jurisdiction Classifier — bepaalt automatisch het rechtsgebied per query/output.

Detecteert en classificeert:
- Nederland (NL) — AVG, UAI, AWB
- EU — AI Act, GDPR, eIDAS, NIS2
- Internationaal — OECD, Council of Europe
- Conflicten tussen rechtsgebieden
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


# ─── Jurisdiction Keywords ─────────────────────────────────────

JURISDICTION_MARKERS = {
    "NL": {
        "frameworks": [
            "AVG",
            "UAI",
            "Awb",
            "Wbp",
            "Wet op de rechterlijke organisatie",
        ],
        "articles": ["Art. 5 Awb", "Art. 3:12 Wbp", "Art. 8 Sv"],
        "keywords": [
            "nederland",
            "nederlandse",
            "amsterdam",
            "rotterdam",
            "den haag",
            "utrecht",
            "eindhoven",
            "groningen",
            "almere",
            "tilburg",
            "autoriteit persoonsgegevens",
            "ap",
            "college bescherming persoonsgegevens",
            "cbp",
            "rechtspraak",
            "raad van state",
            "kamer",
            "tweede kamer",
            "eerste kamer",
            "gemeente",
            "provincie",
            "rijksoverheid",
            "belastingdienst",
            "uwv",
            "svb",
            "nvwa",
            "igj",
            "automotive",
            "dnb",
        ],
        "penalties": ["bestuursboete", "bestuursrechtelijk", "boete omzet"],
    },
    "EU": {
        "frameworks": ["EU AI Act", "GDPR", "eIDAS", "NIS2", "Digital Markets Act"],
        "articles": ["Art. 5 AI Act", "Art. 9 AI Act", "Art. 14 AI Act"],
        "keywords": [
            "eu",
            "europees",
            "europese unie",
            "brussel",
            "straatsburg",
            "echt",
            "edpb",
            "europees toezicht",
            "eu ai office",
            "conformiteitsbeoordeling",
            "harmoniseerde norm",
            "cenelec",
            "eur-lex",
            "verordening",
            "richtlijn",
            "besluit",
            "aankondiging",
            "overgangsrecht",
            "wetgevingsprocedure",
        ],
        "penalties": ["boete tot EUR 35.000.000", "boete tot 7%"],
    },
    "INT": {
        "frameworks": ["OECD AI Principles", "Council of Europe AI Treaty", "ECHR"],
        "articles": ["Art. 8 EVRM", "Art. 14 EVRM"],
        "keywords": [
            "internationaal",
            "oecd",
            "verdrag",
            "echmr",
            "straatsburg",
            "raad van europa",
            "unesco",
            "wto",
            "icao",
            "fundamental rights",
            "human rights",
            "mensenrechten",
            "transborder",
            "derdland",
            "buitenland",
            "internationaal recht",
        ],
        "penalties": ["internationaal recht", "verdragen"],
    },
}

# Conflicten tussen rechtsgebieden
JURISDICTION_CONFLICTS = [
    {
        "a": "NL",
        "b": "EU",
        "type": "overlap",
        "description": "AVG (NL implementatie) vs GDPR (EU verordening)",
        "resolution": "GDPR heeft voorrang op nationale wetgeving (Art. 288 VU)",
    },
    {
        "a": "NL",
        "b": "EU",
        "type": "overlap",
        "description": "UAI (NL uitvoeringswet) vs EU AI Act",
        "resolution": "UAI voert EU AI Act uit op NL niveau — geen conflict",
    },
    {
        "a": "EU",
        "b": "INT",
        "type": "hierarchy",
        "description": "EU AI Act vs OECD AI Principles",
        "resolution": "EU AI Act is bindend, OECD Principles zijn soft law",
    },
]


@dataclass
class JurisdictionMatch:
    """A jurisdiction match."""

    jurisdiction: str
    confidence: float  # 0.0-1.0
    matched_keywords: list[str]
    matched_frameworks: list[str]


@dataclass
class JurisdictionClassification:
    """Complete jurisdiction classification."""

    primary: str
    secondary: list[str]
    confidence: float
    matches: list[JurisdictionMatch]
    conflicts: list[dict[str, Any]]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "primary": self.primary,
            "secondary": self.secondary,
            "confidence": round(self.confidence, 2),
            "matches": [
                {
                    "jurisdiction": m.jurisdiction,
                    "confidence": round(m.confidence, 2),
                    "keywords": m.matched_keywords[:5],
                    "frameworks": m.matched_frameworks,
                }
                for m in self.matches
            ],
            "conflicts": self.conflicts,
            "warnings": self.warnings,
        }


class JurisdictionClassifier:
    """Classifies text by jurisdiction."""

    def classify(self, text: str) -> JurisdictionClassification:
        """Classify text by jurisdiction."""
        text_lower = text.lower()

        matches = []
        for jurisdiction, markers in JURISDICTION_MARKERS.items():
            matched_keywords = [
                kw for kw in markers["keywords"] if kw.lower() in text_lower
            ]
            matched_frameworks = [
                fw for fw in markers["frameworks"] if fw.lower() in text_lower
            ]

            if matched_keywords or matched_frameworks:
                # Confidence based on number of matches
                total_markers = len(markers["keywords"]) + len(markers["frameworks"])
                confidence = min(
                    (len(matched_keywords) + len(matched_frameworks) * 2)
                    / max(total_markers * 0.1, 1),
                    1.0,
                )

                matches.append(
                    JurisdictionMatch(
                        jurisdiction=jurisdiction,
                        confidence=confidence,
                        matched_keywords=matched_keywords,
                        matched_frameworks=matched_frameworks,
                    )
                )

        # Sort by confidence
        matches.sort(key=lambda m: m.confidence, reverse=True)

        if not matches:
            return JurisdictionClassification(
                primary="unknown",
                secondary=[],
                confidence=0.0,
                matches=[],
                conflicts=[],
                warnings=["Geen rechtsgebied gedetecteerd — classificatie onzeker"],
            )

        primary = matches[0]
        secondary = [m.jurisdiction for m in matches[1:] if m.confidence > 0.2]

        # Check for conflicts
        conflicts = self._check_conflicts(
            [m.jurisdiction for m in matches if m.confidence > 0.2]
        )

        # Generate warnings
        warnings = self._generate_warnings(matches, conflicts)

        return JurisdictionClassification(
            primary=primary.jurisdiction,
            secondary=secondary,
            confidence=primary.confidence,
            matches=matches,
            conflicts=conflicts,
            warnings=warnings,
        )

    def _check_conflicts(self, jurisdictions: list[str]) -> list[dict[str, Any]]:
        """Check for conflicts between jurisdictions."""
        conflicts = []
        for conflict in JURISDICTION_CONFLICTS:
            if conflict["a"] in jurisdictions and conflict["b"] in jurisdictions:
                conflicts.append(conflict)
        return conflicts

    def _generate_warnings(
        self,
        matches: list[JurisdictionMatch],
        conflicts: list[dict],
    ) -> list[str]:
        """Generate warnings."""
        warnings = []

        if len(matches) > 1 and matches[0].confidence - matches[1].confidence < 0.1:
            warnings.append(
                f"Twijfelachtige classificatie: {matches[0].jurisdiction} vs {matches[1].jurisdiction}"
            )

        if conflicts:
            warnings.append(f"{len(conflicts)} jurisdictie-conflict(en) gedetecteerd")

        return warnings

    def validate_consistency(self, primary: str, text: str) -> tuple[bool, str]:
        """Validate that text is consistent with declared primary jurisdiction."""
        classification = self.classify(text)

        if classification.primary == "unknown":
            return True, "Geen jurisdictie gedetecteerd — kan niet valideren"

        if classification.primary != primary:
            return (
                False,
                f"Jurisdictie-mismatch: verwacht '{primary}' maar gedetecteerd '{classification.primary}'",
            )

        return True, "Jurisdictie consistent"


# ─── Singleton ─────────────────────────────────────────────────

jurisdiction_classifier = JurisdictionClassifier()
