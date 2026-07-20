"""Evidence Linking System — Fase 4: Tooling & Interoperabiliteit.

Koppelt template-secties aan bewijsstukken:
- Wettelijke bronnen (artikelen, richtlijnen)
- Interne documentatie (beleid, procedures)
- Externe bewijslast (audits, certificaten)
- Audit trail (wie, wat, wanneer)

Gebruik:
    from docs.templates.evidence_linking import EvidenceLinker
    linker = EvidenceLinker("dpia_pre_scan", "Gemeente Test")
    linker.add_evidence("stap_1", "wetgeving", "AVG Art. 35", "https://eur-lex.europa.eu/...")
    report = linker.generate_report()
"""

from __future__ import annotations

import hashlib
import json
from datetime import date
from typing import Any
from uuid import uuid4


class EvidenceLinker:
    """Koppel bewijsstukken aan template-secties."""

    def __init__(self, doc_type: str, org_naam: str):
        self.doc_type = doc_type
        self.org_naam = org_naam
        self.links: list[dict] = []
        self.id = f"evl-{uuid4().hex[:8]}"

    def add_evidence(
        self,
        section_id: str,
        evidence_type: str,
        title: str,
        reference: str,
        description: str = "",
        verified_by: str = "",
        verified_at: str = "",
    ) -> dict:
        """Voeg een bewijsstuk toe gelinkt aan een template-sectie.

        Args:
            section_id: ID van de template-sectie (bijv. "stap_1")
            evidence_type: Type bewijs ("wetgeving", "beleid", "audit", "certificaat", "anders")
            title: Naam van het bewijsstuk
            reference: URL, document-ID, of pad naar het bewijs
            description: Toelichting
            verified_by: Naam van de verifierende persoon
            verified_at: Datum van verificatie (ISO format)

        Returns:
            Het aangemaakte evidence-record
        """
        record = {
            "id": f"ev-{uuid4().hex[:8]}",
            "linkerId": self.id,
            "docType": self.doc_type,
            "sectionId": section_id,
            "evidenceType": evidence_type,
            "title": title,
            "reference": reference,
            "description": description,
            "verifiedBy": verified_by,
            "verifiedAt": verified_at or date.today().isoformat(),
            "status": "active",
            "hash": hashlib.sha256(
                f"{section_id}:{evidence_type}:{title}:{reference}".encode()
            ).hexdigest()[:16],
        }
        self.links.append(record)
        return record

    def remove_evidence(self, evidence_id: str) -> bool:
        """Verwijder een bewijsstuk (soft delete)."""
        for link in self.links:
            if link["id"] == evidence_id:
                link["status"] = "removed"
                link["removedAt"] = date.today().isoformat()
                return True
        return False

    def get_evidence_for_section(self, section_id: str) -> list[dict]:
        """Haal alle bewijsstukken voor een sectie."""
        return [
            l
            for l in self.links
            if l["sectionId"] == section_id and l["status"] == "active"
        ]

    def get_evidence_by_type(self, evidence_type: str) -> list[dict]:
        """Haal alle bewijsstukken van een type."""
        return [
            l
            for l in self.links
            if l["evidenceType"] == evidence_type and l["status"] == "active"
        ]

    def get_coverage(self) -> dict:
        """Bereken bewijsdekking per sectie."""
        sections = set(l["sectionId"] for l in self.links if l["status"] == "active")
        total = len(sections)
        with_evidence = sum(
            1
            for s in sections
            if any(l["sectionId"] == s and l["status"] == "active" for l in self.links)
        )

        return {
            "totalSections": total,
            "sectionsWithEvidence": with_evidence,
            "coveragePercent": round((with_evidence / total * 100) if total > 0 else 0),
        }

    def generate_report(self) -> dict:
        """Genereer evidence-rapport."""
        return {
            "reportId": f"evr-{uuid4().hex[:8]}",
            "linkerId": self.id,
            "docType": self.doc_type,
            "organisatie": self.org_naam,
            "generated": date.today().isoformat(),
            "totalEvidence": len([l for l in self.links if l["status"] == "active"]),
            "removedEvidence": len([l for l in self.links if l["status"] == "removed"]),
            "coverage": self.get_coverage(),
            "evidence": [l for l in self.links if l["status"] == "active"],
            "byType": self._group_by_type(),
        }

    def _group_by_type(self) -> dict:
        """Groepeer bewijsstukken per type."""
        result: dict[str, list] = {}
        for link in self.links:
            if link["status"] == "active":
                etype = link["evidenceType"]
                if etype not in result:
                    result[etype] = []
                result[etype].append(link)
        return result

    def export_json(self) -> str:
        """Exporteer als JSON string."""
        return json.dumps(self.generate_report(), indent=2, ensure_ascii=False)


class AuditTrail:
    """Audit trail voor document-wijzigingen."""

    def __init__(self, doc_type: str, org_naam: str, version: str = "1.0"):
        self.doc_type = doc_type
        self.org_naam = org_naam
        self.version = version
        self.entries: list[dict] = []
        self.id = f"atl-{uuid4().hex[:8]}"

    def log(
        self,
        action: str,
        actor: str,
        details: str = "",
        section: str = "",
    ) -> dict:
        """Log een actie."""
        entry = {
            "id": f"ale-{uuid4().hex[:8]}",
            "trailId": self.id,
            "timestamp": date.today().isoformat(),
            "action": action,
            "actor": actor,
            "section": section,
            "details": details,
            "version": self.version,
        }
        self.entries.append(entry)
        return entry

    def get_history(self) -> list[dict]:
        """Haal volledige geschiedenis."""
        return self.entries

    def get_version_history(self) -> list[dict]:
        """Haal versie-overgangen."""
        return [
            e for e in self.entries if e["action"] in ("created", "approved", "revised")
        ]

    def generate_report(self) -> dict:
        """Genereer audit-rapport."""
        return {
            "reportId": f"atr-{uuid4().hex[:8]}",
            "trailId": self.id,
            "docType": self.doc_type,
            "organisatie": self.org_naam,
            "currentVersion": self.version,
            "totalEntries": len(self.entries),
            "created": self.entries[0]["timestamp"] if self.entries else None,
            "lastModified": self.entries[-1]["timestamp"] if self.entries else None,
            "entries": self.entries,
        }
