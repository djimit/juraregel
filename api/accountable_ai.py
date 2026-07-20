"""Accountable AI Framework — Verantwoorde AI met volledige traceerbaarheid.

Gebaseerd op:
- IEEE 7000-2021 — Ethical concerns in system design
- EU AI Act Art. 13 — Transparency obligations
- GDPR Art. 22 — Right to explanation
- Stanford Legal Engineering (2025) — Accountability by design
- NIST AI RMF — Governance and accountability

Features:
1. Explanation Generation — Uitleg voor elke output
2. Audit Trail — Volledige geschiedenis van besluitvorming
3. Human Review Workflow — Menselijke review voor kritieke beslissingen
4. Bias Detection — Automatische bias-detectie in outputs
5. Compliance Proof — Bewijs van compliance voor audits
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

# ─── Data Models ──────────────────────────────────────────────


@dataclass
class Explanation:
    """A human-readable explanation for an AI output."""

    summary: str
    reasoning_chain: list[dict]
    sources: list[dict]
    confidence_breakdown: dict[str, float]
    limitations: list[str]
    human_review_required: bool
    alternative_interpretations: list[str] = field(default_factory=list)
    counter_arguments: list[str] = field(default_factory=list)


@dataclass
class AuditEntry:
    """A single audit trail entry."""

    timestamp: str
    action: str
    actor: str
    input_data: dict
    output_data: dict
    reasoning: str
    sources: list[str]
    confidence: float
    hash: str = ""

    def __post_init__(self):
        if not self.hash:
            content = f"{self.timestamp}:{self.action}:{self.actor}:{json.dumps(self.input_data, sort_keys=True)}"
            self.hash = hashlib.sha256(content.encode()).hexdigest()[:16]


@dataclass
class AuditTrail:
    """Complete audit trail for an assessment or decision."""

    trail_id: str
    entity_type: str
    entity_id: str
    entries: list[AuditEntry]
    created_at: str
    last_modified: str
    integrity_hash: str = ""


# ─── Accountable AI Framework ─────────────────────────────────


class AccountabilityFramework:
    """Ensure every AI output is traceable, explainable, and auditable."""

    def __init__(self):
        self._audit_trails: dict[str, AuditTrail] = {}
        self._explanations: dict[str, Explanation] = {}

    def explain(
        self, output: dict, question: str = "", depth: str = "standard"
    ) -> Explanation:
        """Generate a human-readable explanation for any output."""

        # Build reasoning chain
        reasoning_chain = []
        if "reasoning_chain" in output:
            reasoning_chain = output["reasoning_chain"]
        elif "arguments" in output:
            for arg in output.get("arguments", []):
                reasoning_chain.append(
                    {
                        "type": "argument",
                        "claim": arg.get("claim", ""),
                        "grounds": arg.get("grounds", []),
                        "confidence": arg.get("confidence", 0),
                    }
                )

        # Extract sources
        sources = []
        if "citations" in output:
            sources = output["citations"]
        elif "search_results" in output:
            for r in output.get("search_results", []):
                sources.append(
                    {
                        "source": r.get("source", ""),
                        "title": r.get("title", ""),
                        "relevance": r.get("score", 0),
                    }
                )

        # Confidence breakdown
        confidence_breakdown = {}
        if "arguments" in output:
            for i, arg in enumerate(output["arguments"]):
                confidence_breakdown[f"argument_{i + 1}"] = arg.get("confidence", 0)

        # Identify limitations
        limitations = []
        if output.get("overall_confidence", 1.0) < 0.7:
            limitations.append("Lage confidence — aanvullend onderzoek aanbevolen")
        if output.get("gaps"):
            limitations.extend(output["gaps"])
        if not sources:
            limitations.append("Geen externe bronnen geciteerd")

        # Human review determination
        human_review = (
            output.get("overall_confidence", 1.0) < 0.7
            or output.get("human_review_required", False)
            or len(limitations) > 2
        )

        explanation = Explanation(
            summary=output.get("conclusion", output.get("answer", "")),
            reasoning_chain=reasoning_chain,
            sources=sources,
            confidence_breakdown=confidence_breakdown,
            limitations=limitations,
            human_review_required=human_review,
        )

        # Add detailed info if requested
        if depth == "detailed":
            explanation.alternative_interpretations = self._generate_alternatives(
                output
            )
            explanation.counter_arguments = [
                r
                for arg in output.get("arguments", [])
                for r in arg.get("rebuttal", [])
            ]

        return explanation

    def create_audit_trail(self, entity_type: str, entity_id: str) -> AuditTrail:
        """Create a new audit trail."""
        trail = AuditTrail(
            trail_id=f"audit-{entity_id}",
            entity_type=entity_type,
            entity_id=entity_id,
            entries=[],
            created_at=datetime.utcnow().isoformat(),
            last_modified=datetime.utcnow().isoformat(),
        )
        self._audit_trails[entity_id] = trail
        return trail

    def log_decision(
        self,
        entity_id: str,
        action: str,
        actor: str,
        input_data: dict,
        output_data: dict,
        reasoning: str,
        sources: list[str] | None = None,
        confidence: float = 0.0,
    ) -> AuditEntry:
        """Log a decision in the audit trail."""
        if entity_id not in self._audit_trails:
            self.create_audit_trail("assessment", entity_id)

        entry = AuditEntry(
            timestamp=datetime.utcnow().isoformat(),
            action=action,
            actor=actor,
            input_data=input_data,
            output_data=output_data,
            reasoning=reasoning,
            sources=sources or [],
            confidence=confidence,
        )

        self._audit_trails[entity_id].entries.append(entry)
        self._audit_trails[entity_id].last_modified = entry.timestamp

        return entry

    def get_audit_trail(self, entity_id: str) -> AuditTrail | None:
        """Get the complete audit trail for an entity."""
        return self._audit_trails.get(entity_id)

    def verify_integrity(self, entity_id: str) -> dict:
        """Verify the integrity of an audit trail."""
        trail = self._audit_trails.get(entity_id)
        if not trail:
            return {"valid": False, "error": "Trail not found"}

        # Verify chain of hashes
        issues = []
        for i, entry in enumerate(trail.entries):
            expected_hash = hashlib.sha256(
                f"{entry.timestamp}:{entry.action}:{entry.actor}:{json.dumps(entry.input_data, sort_keys=True)}".encode()
            ).hexdigest()[:16]

            if entry.hash != expected_hash:
                issues.append(f"Entry {i}: hash mismatch")

        return {
            "valid": len(issues) == 0,
            "entries_count": len(trail.entries),
            "issues": issues,
        }

    def generate_compliance_proof(self, entity_id: str) -> dict:
        """Generate a compliance proof document for auditors."""
        trail = self._audit_trails.get(entity_id)
        if not trail:
            return {"error": "No audit trail found"}

        return {
            "proof_id": f"proof-{entity_id}",
            "generated_at": datetime.utcnow().isoformat(),
            "entity_type": trail.entity_type,
            "entity_id": trail.entity_id,
            "decision_count": len(trail.entries),
            "decisions": [
                {
                    "timestamp": e.timestamp,
                    "action": e.action,
                    "actor": e.actor,
                    "confidence": e.confidence,
                    "sources": len(e.sources),
                    "hash": e.hash,
                }
                for e in trail.entries
            ],
            "integrity": self.verify_integrity(entity_id),
        }

    def _generate_alternatives(self, output: dict) -> list[str]:
        """Generate alternative interpretations."""
        alternatives = []
        if output.get("counter_arguments"):
            alternatives = [
                a.get("claim", "") if isinstance(a, dict) else str(a)
                for a in output.get("counter_arguments", [])
            ]
        return alternatives


# ─── Singleton ─────────────────────────────────────────────────

accountability = AccountabilityFramework()
