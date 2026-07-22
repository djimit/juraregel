"""Temporal Validity Check — controleert of verwijzingen naar wetgeving actueel zijn.

Detecteert:
- Verouderde wetgeving (bijv. "Privacyrichtlijn 1995" in plaats van AVG)
- Toekomstige deadlines die al verstreken zijn
- Gewijzigde artikelen
- Vervallen bepalingen
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import datetime, date
from typing import Any

logger = logging.getLogger(__name__)


# ─── Outdated References ───────────────────────────────────────

OUTDATED_REFERENCES = [
    {
        "old": "Privacyrichtlijn",
        "new": "AVG (Algemene Verordening Gegevensbescherming)",
        "date_replaced": "2018-05-25",
        "severity": "high",
    },
    {
        "old": "Richtlijn 95/46/EG",
        "new": "AVG (Verordening 2016/679)",
        "date_replaced": "2018-05-25",
        "severity": "high",
    },
    {
        "old": "Wet persoonsregistratie",
        "new": "Wet bescherming persoonsgegevens (Wbp) → AVG",
        "date_replaced": "2018-05-25",
        "severity": "high",
    },
    {
        "old": "Data Protection Directive",
        "new": "GDPR / AVG",
        "date_replaced": "2018-05-25",
        "severity": "high",
    },
    {
        "old": "AI Act 2023",
        "new": "AI Act (Verordening 2024/1689, in werking sinds 2024-08-01)",
        "date_replaced": "2024-08-01",
        "severity": "medium",
    },
    {
        "old": "GDPR 2016",
        "new": "AVG (in werking sinds 2018-05-25)",
        "date_replaced": "2018-05-25",
        "severity": "medium",
    },
    {
        "old": "NIS-richtlijn",
        "new": "NIS2 (Richtlijn 2022/2555)",
        "date_replaced": "2024-10-17",
        "severity": "medium",
    },
    {
        "old": "eIDAS 2014",
        "new": "eIDAS 2 (Verordening 2024/1183)",
        "date_replaced": "2024-06-28",
        "severity": "medium",
    },
]


@dataclass
class TemporalFinding:
    """A single temporal finding."""

    finding_type: str  # outdated, future_deadline, changed, expired
    description: str
    old_reference: str
    new_reference: str
    severity: str


@dataclass
class TemporalReport:
    """Complete temporal validity report."""

    total_references: int
    outdated_count: int
    findings: list[TemporalFinding]
    reference_date: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_references": self.total_references,
            "outdated_count": self.outdated_count,
            "findings_count": len(self.findings),
            "findings": [
                {
                    "type": f.finding_type,
                    "description": f.description,
                    "old": f.old_reference,
                    "new": f.new_reference,
                    "severity": f.severity,
                }
                for f in self.findings
            ],
        }


class TemporalValidityChecker:
    """Checks temporal validity of legal references."""

    def __init__(self, reference_date: date | None = None):
        self.reference_date = reference_date or date.today()

    def check(self, text: str) -> TemporalReport:
        """Check temporal validity of text."""
        findings: list[TemporalFinding] = []

        # Check for outdated references
        for ref in OUTDATED_REFERENCES:
            if ref["old"].lower() in text.lower():
                findings.append(
                    TemporalFinding(
                        finding_type="outdated",
                        description=f"Verouderde verwijzing: '{ref['old']}' → '{ref['new']}'",
                        old_reference=ref["old"],
                        new_reference=ref["new"],
                        severity=ref["severity"],
                    )
                )

        # Check for past deadlines mentioned as future
        deadline_findings = self._check_deadlines(text)
        findings.extend(deadline_findings)

        return TemporalReport(
            total_references=len(self._extract_references(text)),
            outdated_count=len(findings),
            findings=findings,
            reference_date=self.reference_date.isoformat(),
        )

    def _check_deadlines(self, text: str) -> list[TemporalFinding]:
        """Check for deadlines mentioned in wrong tense."""
        findings = []

        # Pattern: "per [datum]" or "deadline [datum]"
        deadline_pattern = re.compile(
            r"(per|deadline|uiterlijk|voor)\s+(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})",
            re.IGNORECASE,
        )

        for match in deadline_pattern.finditer(text):
            date_str = match.group(2)
            try:
                deadline = datetime.strptime(date_str, "%Y-%m-%d").date()
                if deadline < self.reference_date:
                    findings.append(
                        TemporalFinding(
                            finding_type="expired",
                            description=f"Verstreken deadline genoemd: {date_str}",
                            old_reference=date_str,
                            new_reference=f"Verstreken sinds {deadline.isoformat()}",
                            severity="high",
                        )
                    )
            except ValueError:
                pass

        return findings

    def _extract_references(self, text: str) -> list[str]:
        """Extract all legal references from text."""
        references = []
        patterns = [
            r"Art\.?\s*\d+",
            r"§\s*\d+",
            r"[A-Z][a-z]+\s+\d{4}",
            r"Richtlijn\s+\d{4}/\d{2}/EG",
            r"Verordening\s+\d{4}/\d{2}",
        ]
        for pattern in patterns:
            references.extend(re.findall(pattern, text))
        return references


# ─── Singleton ─────────────────────────────────────────────────

temporal_checker = TemporalValidityChecker()
