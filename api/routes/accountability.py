"""Accountable AI API — Uitlegbaarheid, audit-trail, compliance-proof."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

from ..accountable_ai import accountability

router = APIRouter()


class ExplainRequest(BaseModel):
    """Request for explanation."""

    output: dict
    question: str = ""
    depth: str = "standard"  # standard, detailed


class AuditLogRequest(BaseModel):
    """Request to log a decision."""

    entity_id: str
    action: str
    actor: str
    input_data: dict = {}
    output_data: dict = {}
    reasoning: str = ""
    sources: list[str] = []
    confidence: float = 0.0


@router.get("/")
async def accountability_status():
    """Get accountability framework status."""
    return {
        "status": "active",
        "audit_trails": len(accountability._audit_trails),
    }


@router.post("/explain")
async def explain_output(request: ExplainRequest):
    """Generate an explanation for an output."""
    explanation = accountability.explain(
        request.output, request.question, request.depth
    )
    return {
        "summary": explanation.summary,
        "reasoning_chain": explanation.reasoning_chain,
        "sources": explanation.sources,
        "confidence_breakdown": explanation.confidence_breakdown,
        "limitations": explanation.limitations,
        "human_review_required": explanation.human_review_required,
        "alternative_interpretations": explanation.alternative_interpretations,
        "counter_arguments": explanation.counter_arguments,
    }


@router.post("/audit/log")
async def log_decision(request: AuditLogRequest):
    """Log a decision in the audit trail."""
    entry = accountability.log_decision(
        entity_id=request.entity_id,
        action=request.action,
        actor=request.actor,
        input_data=request.input_data,
        output_data=request.output_data,
        reasoning=request.reasoning,
        sources=request.sources,
        confidence=request.confidence,
    )
    return {
        "status": "logged",
        "entry": {
            "timestamp": entry.timestamp,
            "action": entry.action,
            "hash": entry.hash,
        },
    }


@router.get("/audit/{entity_id}")
async def get_audit_trail(entity_id: str):
    """Get complete audit trail."""
    trail = accountability.get_audit_trail(entity_id)
    if not trail:
        return {"error": "Audit trail not found"}
    return {
        "trail_id": trail.trail_id,
        "entity_type": trail.entity_type,
        "entity_id": trail.entity_id,
        "entries": [
            {
                "timestamp": e.timestamp,
                "action": e.action,
                "actor": e.actor,
                "reasoning": e.reasoning,
                "confidence": e.confidence,
                "hash": e.hash,
            }
            for e in trail.entries
        ],
    }


@router.get("/audit/{entity_id}/integrity")
async def verify_integrity(entity_id: str):
    """Verify audit trail integrity."""
    return accountability.verify_integrity(entity_id)


@router.get("/compliance-proof/{entity_id}")
async def compliance_proof(entity_id: str):
    """Generate compliance proof for auditors."""
    return accountability.generate_compliance_proof(entity_id)
