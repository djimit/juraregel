"""Approval Gate — workflow voor high-risk AI outputs (L4/L5).

Implementeert:
- 2-regel approval voor L4 (besluitnabij)
- 3-regel approval voor L5 (beslissend)
- Escalatie bij S4/S5 bevindingen
- Audit trail van alle approvals
"""

from __future__ import annotations

import hashlib
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


logger = logging.getLogger(__name__)


@dataclass
class ApprovalRequest:
    """An approval request."""

    request_id: str
    timestamp: str
    autonomy_level: int
    product_name: str
    output_summary: str
    findings_count: int
    max_severity: str
    required_approvers: int
    approvers: list[str] = field(default_factory=list)
    status: str = "pending"  # pending, approved, rejected, escalated
    rejection_reason: str = ""


@dataclass
class ApprovalGateConfig:
    """Configuration for approval gates."""

    l4_required_approvers: int = 2
    l5_required_approvers: int = 3
    s4_auto_escalate: bool = True
    s5_auto_block: bool = True
    approver_roles: list[str] = field(
        default_factory=lambda: ["compliance_officer", "legal_counsel", "dpo"]
    )


class ApprovalGate:
    """Manages approval workflow for high-risk AI outputs."""

    def __init__(self, config: ApprovalGateConfig | None = None):
        self.config = config or ApprovalGateConfig()
        self._requests: list[ApprovalRequest] = []

    def submit(
        self,
        autonomy_level: int,
        product_name: str,
        output_summary: str,
        findings_count: int,
        max_severity: str,
    ) -> ApprovalRequest:
        """Submit an approval request."""
        required = self._get_required_approvers(autonomy_level, max_severity)

        request = ApprovalRequest(
            request_id=f"approve-{hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]}",
            timestamp=datetime.now().isoformat(),
            autonomy_level=autonomy_level,
            product_name=product_name,
            output_summary=output_summary[:200],
            findings_count=findings_count,
            max_severity=max_severity,
            required_approvers=required,
        )

        # Auto-escalate S4
        if self.config.s4_auto_escalate and max_severity in ("S4",):
            request.status = "escalated"
            logger.warning(f"Request {request.request_id} auto-escalated (S4)")

        # Auto-block S5
        if self.config.s5_auto_block and max_severity == "S5":
            request.status = "rejected"
            request.rejection_reason = "S5 bevinding — automatisch geblokkeerd"
            logger.warning(f"Request {request.request_id} auto-blocked (S5)")

        self._requests.append(request)
        return request

    def approve(self, request_id: str, approver: str) -> ApprovalRequest | None:
        """Approve a request."""
        request = self._find_request(request_id)
        if not request or request.status in ("rejected", "escalated"):
            return None

        if approver not in request.approvers:
            request.approvers.append(approver)

        if len(request.approvers) >= request.required_approvers:
            request.status = "approved"

        return request

    def reject(
        self, request_id: str, approver: str, reason: str
    ) -> ApprovalRequest | None:
        """Reject a request."""
        request = self._find_request(request_id)
        if not request:
            return None

        request.status = "rejected"
        request.rejection_reason = reason
        return request

    def _get_required_approvers(self, autonomy_level: int, max_severity: str) -> int:
        """Get required number of approvers."""
        if autonomy_level >= 5 or max_severity == "S5":
            return self.config.l5_required_approvers
        elif autonomy_level >= 4 or max_severity == "S4":
            return self.config.l4_required_approvers
        return 1

    def _find_request(self, request_id: str) -> ApprovalRequest | None:
        """Find a request by ID."""
        for r in self._requests:
            if r.request_id == request_id:
                return r
        return None

    def get_pending(self) -> list[ApprovalRequest]:
        """Get all pending requests."""
        return [r for r in self._requests if r.status == "pending"]

    def get_status(self) -> dict[str, Any]:
        """Get approval gate status."""
        return {
            "total": len(self._requests),
            "pending": sum(1 for r in self._requests if r.status == "pending"),
            "approved": sum(1 for r in self._requests if r.status == "approved"),
            "rejected": sum(1 for r in self._requests if r.status == "rejected"),
            "escalated": sum(1 for r in self._requests if r.status == "escalated"),
        }


# ─── Singleton ─────────────────────────────────────────────────

approval_gate = ApprovalGate()
