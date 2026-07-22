"""Evidence Lineage — complete audit trail from model to decision.

Implements Stanford's requirement that every material answer must be
traceable to: model version, prompt template, retrieval results,
source versions, generated answer, human modifications, and final decision.

Aligned with CEPEJ JAI-06: statement-level source lineage.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SourceRef:
    """A referenced legal source."""

    document_id: str
    passage_id: str = ""
    source_version: str = ""
    source_hash: str = ""
    url: str = ""
    retrieved_at: str = ""
    authority_rank: int = 0  # 1=binding-law, 5=context-only


@dataclass
class RetrievalRecord:
    """Record of a retrieval operation."""

    query: str
    results: list[SourceRef] = field(default_factory=list)
    retrieval_model: str = ""
    index_version: str = ""
    timestamp: str = ""


@dataclass
class HumanEdit:
    """A human modification to AI output."""

    actor: str
    role: str
    action: str  # "modified", "approved", "rejected"
    original_text: str = ""
    modified_text: str = ""
    reason: str = ""
    timestamp: str = ""


@dataclass
class EvidenceLineage:
    """Complete evidence lineage for a single AI-generated output.

    Every substantive claim must be reducible to this chain.
    Non-traceable content cannot be professionally verified.
    """

    # Generation context
    model_version: str = ""
    prompt_template_id: str = ""
    prompt_hash: str = ""

    # Retrieval context
    retrieval: RetrievalRecord | None = None
    sources: list[SourceRef] = field(default_factory=list)

    # Output
    generated_answer: str = ""
    generated_at: str = ""

    # Human review
    human_edits: list[HumanEdit] = field(default_factory=list)
    human_review_required: bool = True
    human_review_completed: bool = False

    # Final decision
    final_answer: str = ""
    final_decision: str = ""  # "approved", "modified", "rejected"

    # Integrity
    receipt_id: str = ""
    lineage_hash: str = ""

    def compute_hash(self) -> str:
        """Compute deterministic hash of the lineage chain."""
        content = json.dumps(
            {
                "model_version": self.model_version,
                "prompt_template_id": self.prompt_template_id,
                "retrieval": {
                    "query": self.retrieval.query if self.retrieval else "",
                    "model": self.retrieval.retrieval_model if self.retrieval else "",
                },
                "sources": [
                    {
                        "doc": s.document_id,
                        "ver": s.source_version,
                        "hash": s.source_hash,
                    }
                    for s in self.sources
                ],
                "generated_answer": self.generated_answer,
                "human_edits": [
                    {
                        "actor": e.actor,
                        "action": e.action,
                        "modified": e.modified_text,
                    }
                    for e in self.human_edits
                ],
                "final_answer": self.final_answer,
            },
            sort_keys=True,
        )
        self.lineage_hash = hashlib.sha256(content.encode()).hexdigest()
        return self.lineage_hash

    @property
    def is_complete(self) -> bool:
        """Check if the lineage chain is complete."""
        return (
            bool(self.model_version)
            and bool(self.generated_answer)
            and bool(self.sources)
            and self.human_review_completed
            and bool(self.final_answer)
            and bool(self.lineage_hash)
        )

    @property
    def is_traceable(self) -> bool:
        """CEPEJ JAI-06: every claim must be traceable to an authentic source."""
        return all(bool(s.document_id) and bool(s.source_hash) for s in self.sources)

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_version": self.model_version,
            "prompt_template_id": self.prompt_template_id,
            "prompt_hash": self.prompt_hash,
            "retrieval": {
                "query": self.retrieval.query if self.retrieval else "",
                "results_count": len(self.retrieval.results) if self.retrieval else 0,
                "retrieval_model": self.retrieval.retrieval_model
                if self.retrieval
                else "",
            },
            "sources": [
                {
                    "document_id": s.document_id,
                    "passage_id": s.passage_id,
                    "source_version": s.source_version,
                    "source_hash": s.source_hash,
                    "authority_rank": s.authority_rank,
                }
                for s in self.sources
            ],
            "generated_answer": self.generated_answer,
            "generated_at": self.generated_at,
            "human_edits": [
                {
                    "actor": e.actor,
                    "role": e.role,
                    "action": e.action,
                    "reason": e.reason,
                    "timestamp": e.timestamp,
                }
                for e in self.human_edits
            ],
            "human_review_required": self.human_review_required,
            "human_review_completed": self.human_review_completed,
            "final_answer": self.final_answer,
            "final_decision": self.final_decision,
            "receipt_id": self.receipt_id,
            "lineage_hash": self.lineage_hash,
            "is_complete": self.is_complete,
            "is_traceable": self.is_traceable,
        }
