"""PII Redaction Middleware — detecteert en redacteert persoonsgegevens in AI-output.

S5-beveiligingsmaatregel: voorkomt dat BSN, email, paspoort, telefoon, en andere
PII in antwoorden van AI-producten terechtkomen.

Detecteert:
- BSN-nummers (9 cijfers)
- Email-adressen
- Telefoonnummers (NL format)
- Paspoortnummers
- Postcodes + huisnummer combinaties
- IBAN-nummers
- KvK-nummers
- Geboortedatums met naam-context
"""

from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


# ─── PII Detection Patterns ────────────────────────────────────

PII_PATTERNS = {
    "BSN": {
        "pattern": re.compile(r"\b\d{9}\b"),
        "replacement": "[BSN]",
        "severity": "critical",
        "description": "BSN-nummer",
    },
    "EMAIL": {
        "pattern": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Z|a-z]{2,}"),
        "replacement": "[EMAIL]",
        "severity": "high",
        "description": "Email-adres",
    },
    "PHONE_NL": {
        "pattern": re.compile(
            r"\b(?:\+31|0)[-\s]?(?:6[-\s]?\d{8}|[1-5]\d[-\s]?\d{7})\b"
        ),
        "replacement": "[TELEFOON]",
        "severity": "high",
        "description": "Telefoonnummer",
    },
    "PASPOORT": {
        "pattern": re.compile(r"\b[A-Z]{2}\d{6,9}\b"),
        "replacement": "[PASPOORT]",
        "severity": "critical",
        "description": "Paspoortnummer",
    },
    "POSTCODE_HUIS": {
        "pattern": re.compile(r"\b\d{4}\s?[A-Z]{2}\s+\d+[a-zA-Z]?\b"),
        "replacement": "[ADRES]",
        "severity": "medium",
        "description": "Postcode + huisnummer",
    },
    "IBAN": {
        "pattern": re.compile(r"\bNL\d{2}[A-Z]{4}\d{10}\b"),
        "replacement": "[IBAN]",
        "severity": "critical",
        "description": "IBAN-nummer",
    },
    "KVK": {
        "pattern": re.compile(r"\b\d{8}\b"),
        "replacement": "[KVK]",
        "severity": "low",
        "description": "Mogelijk KvK-nummer",
    },
    "GEBOORTEDATUM": {
        "pattern": re.compile(r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b"),
        "replacement": "[DATUM]",
        "severity": "medium",
        "description": "Geboortedatum",
    },
}


@dataclass
class PIIDetection:
    """A single PII detection."""

    pii_type: str
    severity: str
    description: str
    position: int
    original_hash: str  # SHA-256 hash van het origineel (voor audit, geen plaintext)


@dataclass
class PIIRedactionResult:
    """Result of PII redaction."""

    original_text: str
    redacted_text: str
    detections: list[PIIDetection]
    pii_density: float  # PII items per 100 words
    blocked: bool  # True if density > threshold

    @property
    def has_pii(self) -> bool:
        return len(self.detections) > 0

    @property
    def critical_count(self) -> int:
        return sum(1 for d in self.detections if d.severity == "critical")

    @property
    def to_dict(self) -> dict[str, Any]:
        return {
            "has_pii": self.has_pii,
            "detection_count": len(self.detections),
            "pii_density": round(self.pii_density, 2),
            "blocked": self.blocked,
            "critical_count": self.critical_count,
            "detections": [
                {
                    "type": d.pii_type,
                    "severity": d.severity,
                    "description": d.description,
                }
                for d in self.detections
            ],
        }


class PIIRedactionMiddleware:
    """Detects and redacts PII from AI output."""

    # Threshold: blokkeer output bij >3 PII items per 100 woorden
    DENSITY_THRESHOLD = 3.0

    def redact(self, text: str) -> PIIRedactionResult:
        """Detect and redact PII from text."""
        detections: list[PIIDetection] = []
        redacted = text

        for pii_type, config in PII_PATTERNS.items():
            matches = list(config["pattern"].finditer(text))
            for match in matches:
                original = match.group()
                original_hash = hashlib.sha256(original.encode()).hexdigest()[:16]

                detections.append(
                    PIIDetection(
                        pii_type=pii_type,
                        severity=config["severity"],
                        description=config["description"],
                        position=match.start(),
                        original_hash=original_hash,
                    )
                )

            # Replace all matches
            redacted = config["pattern"].sub(config["replacement"], redacted)

        # Calculate density
        word_count = len(text.split())
        pii_density = (len(detections) / max(word_count, 1)) * 100

        # Block if density too high
        blocked = pii_density > self.DENSITY_THRESHOLD

        if blocked:
            logger.warning(
                f"PII density {pii_density:.1f} exceeds threshold {self.DENSITY_THRESHOLD} — output blocked"
            )

        return PIIRedactionResult(
            original_text=text,
            redacted_text=redacted,
            detections=detections,
            pii_density=pii_density,
            blocked=blocked,
        )

    def audit_only(self, text: str) -> PIIRedactionResult:
        """Detect PII without redacting (for audit purposes)."""
        detections: list[PIIDetection] = []

        for pii_type, config in PII_PATTERNS.items():
            matches = list(config["pattern"].finditer(text))
            for match in matches:
                original = match.group()
                original_hash = hashlib.sha256(original.encode()).hexdigest()[:16]

                detections.append(
                    PIIDetection(
                        pii_type=pii_type,
                        severity=config["severity"],
                        description=config["description"],
                        position=match.start(),
                        original_hash=original_hash,
                    )
                )

        word_count = len(text.split())
        pii_density = (len(detections) / max(word_count, 1)) * 100

        return PIIRedactionResult(
            original_text=text,
            redacted_text=text,
            detections=detections,
            pii_density=pii_density,
            blocked=pii_density > self.DENSITY_THRESHOLD,
        )


# ─── Singleton ─────────────────────────────────────────────────

pii_redaction = PIIRedactionMiddleware()
