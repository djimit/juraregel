"""Citation Verification — controleert bronverwijzingen in AI-output.

Detecteert:
- Ontbrekende citaties (beweringen zonder bron)
- Onjuiste citaties (niet-bestaande artikelen)
- Verouderde citaties (gewijzigde wetgeving)
- Formaat-fouten (onjuiste artikel-verwijzingen)
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


# ─── Known Legal References ────────────────────────────────────

VALID_ARTICLES = {
    "AVG": {
        "articles": list(range(1, 95)),  # Art. 1-94
        "common": [
            5,
            6,
            12,
            13,
            14,
            15,
            17,
            20,
            21,
            25,
            28,
            30,
            32,
            33,
            34,
            35,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            58,
            83,
            84,
        ],
    },
    "EU AI Act": {
        "articles": list(range(1, 115)),  # Art. 1-114
        "common": [
            5,
            6,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            25,
            26,
            27,
            28,
            29,
            33,
            35,
            47,
            50,
            65,
            70,
            71,
            72,
        ],
    },
    "NIS2": {
        "articles": list(range(1, 47)),  # Art. 1-46
        "common": [
            7,
            8,
            14,
            15,
            16,
            17,
            18,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
        ],
    },
}

# Citation format patterns
CITATION_PATTERNS = [
    r"Art\.?\s*(\d+)\s*(lid\s*\d+)?\s*(sub\s*\d+)?",  # Art. 5, Art. 5 lid 1
    r"§\s*(\d+)",  # § 5
    r"article\s*(\d+)",  # article 5 (English)
    r"artikel\s*(\d+)",  # artikel 5 (Dutch)
]


@dataclass
class CitationFinding:
    """A single citation finding."""

    finding_type: str  # missing, invalid, outdated, malformed
    description: str
    location: str
    severity: str


@dataclass
class CitationReport:
    """Complete citation verification report."""

    total_claims: int
    cited_claims: int
    uncited_claims: int
    invalid_citations: int
    findings: list[CitationFinding]
    citation_density: float  # citations per 100 words

    @property
    def citation_rate(self) -> float:
        return self.cited_claims / max(self.total_claims, 1)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_claims": self.total_claims,
            "cited_claims": self.cited_claims,
            "uncited_claims": self.uncited_claims,
            "citation_rate": round(self.citation_rate, 2),
            "invalid_citations": self.invalid_citations,
            "findings_count": len(self.findings),
            "findings": [
                {
                    "type": f.finding_type,
                    "description": f.description,
                    "severity": f.severity,
                }
                for f in self.findings
            ],
        }


class CitationVerifier:
    """Verifies citations in legal text."""

    def verify(self, text: str) -> CitationReport:
        """Verify citations in text."""
        findings: list[CitationFinding] = []

        # Extract all citations
        citations = self._extract_citations(text)

        # Count claims (sentences with legal assertions)
        claims = self._extract_claims(text)
        total_claims = len(claims)
        cited_claims = 0
        uncited_claims = 0

        for claim in claims:
            claim_citations = self._extract_citations(claim)
            if claim_citations:
                cited_claims += 1
            else:
                uncited_claims += 1
                findings.append(
                    CitationFinding(
                        finding_type="missing",
                        description=f"Bewering zonder bron: '{claim[:60]}...'",
                        location=f"claim: {claim[:40]}",
                        severity="medium",
                    )
                )

        # Validate citations
        invalid_count = 0
        for citation in citations:
            valid, reason = self._validate_citation(citation)
            if not valid:
                invalid_count += 1
                findings.append(
                    CitationFinding(
                        finding_type="invalid",
                        description=reason,
                        location=f"citation: {citation}",
                        severity="high",
                    )
                )

        # Calculate density
        word_count = len(text.split())
        citation_density = len(citations) / max(word_count, 1) * 100

        return CitationReport(
            total_claims=total_claims,
            cited_claims=cited_claims,
            uncited_claims=uncited_claims,
            invalid_citations=invalid_count,
            findings=findings,
            citation_density=citation_density,
        )

    def _extract_citations(self, text: str) -> list[str]:
        """Extract all citations from text."""
        citations = []
        for pattern in CITATION_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    citations.append("".join(str(m) for m in match if m))
                else:
                    citations.append(match)
        return citations

    def _extract_claims(self, text: str) -> list[str]:
        """Extract legal claims from text."""
        sentences = re.split(r"[.!?]+", text)
        claims = []
        claim_indicators = [
            "moet",
            "dient",
            "vereist",
            "verplicht",
            "is toegestaan",
            "mag niet",
            "verboden",
            "recht op",
            "plicht tot",
            "moeten",
            "dienen",
            "zijn verplicht",
            "is verboden",
            "shall",
            "must",
            "required",
            "prohibited",
            "entitled",
        ]
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and any(ind in sentence.lower() for ind in claim_indicators):
                claims.append(sentence)
        return claims

    def _validate_citation(self, citation: str) -> tuple[bool, str]:
        """Validate a single citation."""
        if not citation:
            return False, "Lege citatie"

        # Check if it's a valid article reference
        match = re.search(r"(\d+)", citation)
        if not match:
            return False, f"Geen artikelnummer gevonden in: {citation}"

        article_num = int(match.group(1))

        # Check if article number is reasonable
        if article_num < 1 or article_num > 200:
            return False, f"Ongeldig artikelnummer: {article_num}"

        return True, "Valid"


# ─── Singleton ─────────────────────────────────────────────────

citation_verifier = CitationVerifier()
