"""Djimitflo Bridge — push assurance results to Djimitflo compliance platform.

Implements the connection between JuraRegel's Legal AI Assurance Framework
and Djimitflo's compliance task management system.

Maps:
- JuraRegel assurance failures → Djimitflo compliance tasks
- Severity S4/S5 → High/Critical priority tasks
- L4/L5 use cases → 2-approval workflow
- Evidence lineage → Djimitflo audit events
"""

from __future__ import annotations

import hashlib
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .error_taxonomy import LegalError, Severity
from .severity_scorer import UseCaseProfile

logger = logging.getLogger(__name__)

DJIMITFLO_API_URL = os.getenv("DJIMITFLO_API_URL", "")
DJIMITFLO_API_KEY = os.getenv("DJIMITFLO_API_KEY", "")


@dataclass
class ComplianceTask:
    """A compliance task for Djimitflo."""

    title: str
    description: str
    priority: str  # "low", "medium", "high", "critical"
    control_id: str
    evidence_refs: list[str] = field(default_factory=list)
    approvers: int = 1
    due_date: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditEvent:
    """A compliance-evaluated event for Djimitflo."""

    event_id: str
    timestamp: str
    control_id: str
    result: str  # "pass", "fail", "warning"
    evidence_refs: list[str] = field(default_factory=list)
    evaluator: str = "juraregel-assurance"
    details: str = ""


@dataclass
class ApprovalGate:
    """An approval gate for high-severity findings."""

    gate_id: str
    task_id: str
    required_approvers: int
    approvers: list[str] = field(default_factory=list)
    status: str = "pending"  # "pending", "approved", "rejected"


class DjimitfloBridge:
    """Bridge between JuraRegel assurance and Djimitflo compliance."""

    def __init__(self):
        self._tasks: list[ComplianceTask] = []
        self._events: list[AuditEvent] = []
        self._gates: list[ApprovalGate] = []

    def create_task_from_error(
        self, error: LegalError, use_case: UseCaseProfile
    ) -> ComplianceTask | None:
        """Create a compliance task from a legal AI error."""
        if error.severity in (Severity.S4_RECHTSVERLIES, Severity.S5_SYSTEEMISCH):
            priority = "critical"
            approvers = 2
        elif error.severity == Severity.S3_MATERIEEL:
            priority = "high"
            approvers = 1
        elif error.severity == Severity.S2_HERSTELBAAR:
            priority = "medium"
            approvers = 1
        else:
            return None  # S1 don't create tasks

        # Map error type to NEDERUS control
        control_map = {
            "feitelijke_fout": "NED-01",
            "bronfout": "NED-04",
            "interpretatiefout": "NED-01",
            "jurisdictiefout": "NED-03",
            "temporaliteitsfout": "NED-03",
            "procedurefout": "NED-05",
            "omissiefout": "NED-01",
            "bias_ongelijke_behandeling": "NED-02",
            "vertrouwelijkheidsincident": "NED-05",
        }
        control_id = control_map.get(error.error_type.value, "NED-01")

        task = ComplianceTask(
            title=f"[{error.severity.value}] {error.error_type.value}: {error.description[:60]}",
            description=error.description,
            priority=priority,
            control_id=control_id,
            evidence_refs=[error.source_claim] if error.source_claim else [],
            approvers=approvers,
            due_date="",
            metadata={
                "error_type": error.error_type.value,
                "severity": error.severity.value,
                "use_case": use_case.name,
                "autonomy_level": use_case.autonomy_level,
            },
        )
        self._tasks.append(task)
        return task

    def create_tasks_from_audit_report(
        self,
        audit_report: dict[str, Any],
        use_case: UseCaseProfile,
    ) -> list[ComplianceTask]:
        """Create compliance tasks from a full audit report."""
        tasks = []
        from .error_taxonomy import LegalError, Severity

        for finding in audit_report.get("findings", []):
            severity_map = {
                "S1": Severity.S1_COSMETISCH,
                "S2": Severity.S2_HERSTELBAAR,
                "S3": Severity.S3_MATERIEEL,
                "S4": Severity.S4_RECHTSVERLIES,
                "S5": Severity.S5_SYSTEEMISCH,
            }
            severity = severity_map.get(
                finding.get("severity", "S1"), Severity.S1_COSMETISCH
            )

            from .error_taxonomy import LegalErrorType

            error_type_map = {
                "feitelijke_fout": LegalErrorType.FACTUAL,
                "bronfout": LegalErrorType.SOURCE,
                "interpretatiefout": LegalErrorType.INTERPRETATION,
                "jurisdictiefout": LegalErrorType.JURISDICTION,
                "temporaliteitsfout": LegalErrorType.TEMPORAL,
                "procedurefout": LegalErrorType.PROCEDURAL,
                "omissiefout": LegalErrorType.OMISSION,
                "bias_ongelijke_behandeling": LegalErrorType.BIAS,
                "vertrouwelijkheidsincident": LegalErrorType.CONFIDENTIALITY,
            }
            error_type = error_type_map.get(
                finding.get("type", ""), LegalErrorType.FACTUAL
            )

            error = LegalError(
                error_type=error_type,
                severity=severity,
                description=finding.get("description", ""),
                source_claim=finding.get("evidence", ""),
            )
            task = self.create_task_from_error(error, use_case)
            if task:
                tasks.append(task)

        return tasks

    def create_audit_event(
        self,
        control_id: str,
        result: str,
        evidence_refs: list[str],
        details: str = "",
    ) -> AuditEvent:
        """Create a compliance-evaluated audit event."""
        event = AuditEvent(
            event_id=f"evt-{hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]}",
            timestamp=datetime.now().isoformat(),
            control_id=control_id,
            result=result,
            evidence_refs=evidence_refs,
            details=details,
        )
        self._events.append(event)
        return event

    def create_approval_gate(self, task: ComplianceTask) -> ApprovalGate | None:
        """Create an approval gate for tasks requiring 2+ approvers."""
        if task.approvers < 2:
            return None

        gate = ApprovalGate(
            gate_id=f"gate-{hashlib.sha256(task.title.encode()).hexdigest()[:12]}",
            task_id=task.title,
            required_approvers=task.approvers,
        )
        self._gates.append(gate)
        return gate

    def get_tasks(self) -> list[ComplianceTask]:
        """Get all compliance tasks."""
        return self._tasks

    def get_events(self) -> list[AuditEvent]:
        """Get all audit events."""
        return self._events

    def get_gates(self) -> list[ApprovalGate]:
        """Get all approval gates."""
        return self._gates

    def to_report(self) -> dict[str, Any]:
        """Generate a full Djimitflo integration report."""
        return {
            "tasks": [
                {
                    "title": t.title,
                    "priority": t.priority,
                    "control_id": t.control_id,
                    "approvers": t.approvers,
                }
                for t in self._tasks
            ],
            "events": [
                {
                    "event_id": e.event_id,
                    "control_id": e.control_id,
                    "result": e.result,
                }
                for e in self._events
            ],
            "gates": [
                {
                    "gate_id": g.gate_id,
                    "status": g.status,
                    "required": g.required_approvers,
                    "current": len(g.approvers),
                }
                for g in self._gates
            ],
        }


# ─── Singleton ─────────────────────────────────────────────────

djimitflo_bridge = DjimitfloBridge()
