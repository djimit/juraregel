"""Version Control & Approval Workflow — Fase 4: Tooling & Interoperabiliteit.

Document-versiebeheer met:
- Semantische versioning (semver)
- Changelog per versie
- Approval workflow (draft → review → approved → published)
- Rollback capability
- Digital signature placeholder

Gebruik:
    from docs.templates.version_control import DocumentVersion, ApprovalWorkflow
    doc = DocumentVersion("dpia_pre_scan", "Gemeente Test", content={...})
    doc.bump_minor("Toegevoegd: pre-scan stap")
    workflow = ApprovalWorkflow(doc)
    workflow.submit_for_review("Jan Jansen")
    workflow.approve("Piet Pietersen", "FG")
"""

from __future__ import annotations

import hashlib
import json
from datetime import date
from typing import Any
from uuid import uuid4


# ─── Document Version ─────────────────────────────────────────


class DocumentVersion:
    """Versiebeheer voor een document."""

    def __init__(
        self,
        doc_type: str,
        org_naam: str,
        content: dict,
        version: str = "1.0.0",
    ):
        self.id = f"dv-{uuid4().hex[:8]}"
        self.doc_type = doc_type
        self.org_naam = org_naam
        self.content = content
        self.version = version
        self.changelog: list[dict] = []
        self.created = date.today().isoformat()
        self._checksum = self._compute_checksum()

    def _compute_checksum(self) -> str:
        payload = json.dumps(self.content, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    def bump_major(self, reason: str, actor: str = "") -> str:
        """Major bump (x.0.0) — breaking changes."""
        parts = self.version.split(".")
        self.version = f"{int(parts[0]) + 1}.0.0"
        self._log_change("major", reason, actor)
        self._checksum = self._compute_checksum()
        return self.version

    def bump_minor(self, reason: str, actor: str = "") -> str:
        """Minor bump (x.y.0) — new content, backwards compatible."""
        parts = self.version.split(".")
        self.version = f"{parts[0]}.{int(parts[1]) + 1}.0"
        self._log_change("minor", reason, actor)
        self._checksum = self._compute_checksum()
        return self.version

    def bump_patch(self, reason: str, actor: str = "") -> str:
        """Patch bump (x.y.z) — corrections, small fixes."""
        parts = self.version.split(".")
        self.version = f"{parts[0]}.{parts[1]}.{int(parts[2]) + 1}"
        self._log_change("patch", reason, actor)
        self._checksum = self._compute_checksum()
        return self.version

    def _log_change(self, change_type: str, reason: str, actor: str) -> None:
        self.changelog.append(
            {
                "version": self.version,
                "type": change_type,
                "reason": reason,
                "actor": actor,
                "date": date.today().isoformat(),
                "checksum": self._checksum,
            }
        )

    def verify_integrity(self) -> bool:
        """Verifieer dat de content niet is gewijzigd sinds laatste bump."""
        return self._checksum == self._compute_checksum()

    def get_info(self) -> dict:
        """Document-versie info."""
        return {
            "id": self.id,
            "docType": self.doc_type,
            "organisatie": self.org_naam,
            "version": self.version,
            "created": self.created,
            "lastModified": self.changelog[-1]["date"]
            if self.changelog
            else self.created,
            "checksum": self._checksum,
            "integrity": self.verify_integrity(),
            "changelogEntries": len(self.changelog),
        }


# ─── Approval Workflow ────────────────────────────────────────


class ApprovalWorkflow:
    """Approval workflow: draft → review → approved → published."""

    STATES = ["draft", "in_review", "approved", "published", "archived"]

    def __init__(self, doc_version: DocumentVersion):
        self.doc_version = doc_version
        self.state = "draft"
        self.approvals: list[dict] = []
        self.rejections: list[dict] = []
        self.current_reviewer: str | None = None

    def submit_for_review(self, submitter: str) -> dict:
        """Draag in voor review."""
        if self.state != "draft":
            return {"error": f"Kan niet indienen vanuit staat: {self.state}"}

        self.state = "in_review"
        self.current_reviewer = None
        return {
            "status": "submitted",
            "state": self.state,
            "submitter": submitter,
            "date": date.today().isoformat(),
        }

    def assign_reviewer(self, reviewer: str, role: str) -> dict:
        """Wijs een reviewer toe."""
        if self.state != "in_review":
            return {"error": "Document is niet in review-staat"}

        self.current_reviewer = reviewer
        return {
            "status": "assigned",
            "reviewer": reviewer,
            "role": role,
            "date": date.today().isoformat(),
        }

    def approve(self, approver: str, role: str, comments: str = "") -> dict:
        """Keur het document goed."""
        if self.state not in ("in_review", "draft"):
            return {"error": f"Kan niet goedkeuren vanuit staat: {self.state}"}

        approval = {
            "approver": approver,
            "role": role,
            "date": date.today().isoformat(),
            "comments": comments,
            "version": self.doc_version.version,
            "signature": f"sig-{uuid4().hex[:12]}",
        }
        self.approvals.append(approval)
        self.state = "approved"
        self.current_reviewer = None
        return {"status": "approved", "approval": approval}

    def reject(self, reviewer: str, reason: str) -> dict:
        """Wijs af — terug naar draft."""
        if self.state != "in_review":
            return {"error": "Document is niet in review-staat"}

        rejection = {
            "reviewer": reviewer,
            "reason": reason,
            "date": date.today().isoformat(),
            "version": self.doc_version.version,
        }
        self.rejections.append(rejection)
        self.state = "draft"
        self.current_reviewer = None
        return {"status": "rejected", "rejection": rejection}

    def publish(self, publisher: str) -> dict:
        """Publiceer het document."""
        if self.state != "approved":
            return {"error": "Document moet eerst worden goedgekeurd"}

        self.state = "published"
        return {
            "status": "published",
            "publisher": publisher,
            "date": date.today().isoformat(),
            "version": self.doc_version.version,
        }

    def archive(self, archiver: str, reason: str = "") -> dict:
        """Archiveer het document."""
        if self.state != "published":
            return {
                "error": "Alleen gepubliceerde documenten kunnen worden gearchiveerd"
            }

        self.state = "archived"
        return {
            "status": "archived",
            "archiver": archiver,
            "reason": reason,
            "date": date.today().isoformat(),
        }

    def get_status(self) -> dict:
        """Huidige workflow-status."""
        return {
            "state": self.state,
            "version": self.doc_version.version,
            "approvals": len(self.approvals),
            "rejections": len(self.rejections),
            "currentReviewer": self.current_reviewer,
            "canSubmit": self.state == "draft",
            "canApprove": self.state in ("in_review", "draft"),
            "canPublish": self.state == "approved",
            "canArchive": self.state == "published",
        }

    def get_history(self) -> list[dict]:
        """Volledige approval-geschiedenis."""
        history = []
        for a in self.approvals:
            history.append({**a, "action": "approved"})
        for r in self.rejections:
            history.append({**r, "action": "rejected"})
        return sorted(history, key=lambda x: x["date"])
