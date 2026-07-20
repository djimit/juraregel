"""Orchestrator API — Autonome compliance-assessment agent."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

from ..orchestrator import orchestrator

router = APIRouter()


class AssessmentRequest(BaseModel):
    """Full assessment request."""

    organisation_id: str = "default"
    processing_activity: dict[str, Any]


@router.get("/")
async def orchestrator_status():
    """Get orchestrator status."""
    return {
        "status": "active",
        "capabilities": [
            "multi-jurisdiction analysis",
            "legal reasoning (Toulmin)",
            "risk prediction",
            "knowledge graph analysis",
            "drift detection",
            "autonomous synthesis",
            "audit trail logging",
        ],
    }


@router.post("/assess")
async def run_assessment(request: AssessmentRequest):
    """Run a complete autonomous compliance assessment."""
    assessment = orchestrator.run_full_assessment(
        organisation_id=request.organisation_id,
        processing_activity=request.processing_activity,
    )

    return {
        "assessment_id": assessment.assessment_id,
        "organisation_id": assessment.organisation_id,
        "conclusion": assessment.conclusion,
        "confidence": assessment.confidence,
        "human_review_required": assessment.human_review_required,
        "required_actions": assessment.required_actions,
        "deadlines": assessment.deadlines,
        "steps": [
            {
                "step_id": s.step_id,
                "name": s.name,
                "status": s.status,
                "duration_ms": s.duration_ms,
            }
            for s in assessment.steps
        ],
        "analysis_summary": {
            "jurisdictions": assessment.jurisdiction_analysis.get("frameworks", []),
            "obligations": assessment.jurisdiction_analysis.get("obligations_count", 0),
            "risks": assessment.risk_predictions.get("risk_count", 0),
            "overall_risk": assessment.risk_predictions.get("overall_risk", 0),
            "drift": assessment.drift_status.get("drift_score", 0),
        },
        "audit_trail_id": assessment.audit_trail_id,
        "model_used": assessment.model_used,
        "total_duration_ms": assessment.total_duration_ms,
        "generated_at": assessment.generated_at,
    }
