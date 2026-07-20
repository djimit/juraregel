"""Policy-as-Code API — Evaluate compliance policies."""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Any

router = APIRouter()


class PolicyEvalRequest(BaseModel):
    """Request to evaluate policies."""

    context: dict[str, Any] = Field(..., description="Context for policy evaluation")


@router.get("/")
async def list_policies():
    """List all available policies."""
    from ..policy_engine import PolicyEngine

    engine = PolicyEngine()
    return {
        "policies": [
            {
                "id": p.policy_id,
                "article": p.article,
                "description": p.description,
            }
            for p in engine.policies
        ]
    }


@router.post("/evaluate")
async def evaluate_all(request: PolicyEvalRequest):
    """Evaluate all policies against the context."""
    from ..policy_engine import PolicyEngine

    engine = PolicyEngine()
    return engine.get_compliance_summary(request.context)


@router.post("/evaluate/{policy_id}")
async def evaluate_policy(policy_id: str, request: PolicyEvalRequest):
    """Evaluate a specific policy."""
    from ..policy_engine import PolicyEngine

    engine = PolicyEngine()
    result = engine.evaluate_policy(policy_id, request.context)
    if result is None:
        return {"error": f"Policy not found: {policy_id}"}
    return {
        "policy_id": result.policy_id,
        "compliant": result.compliant,
        "violations": [
            {
                "article": v.article,
                "message": v.message,
                "severity": v.severity.value,
                "remediation": v.remediation,
                "citation": v.citation,
            }
            for v in result.violations
        ],
        "evidence": result.evidence,
    }
