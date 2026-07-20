"""Digital Twin API — Digitale kopie van compliance-postuur."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

from ..digital_twin import digital_twin_engine

router = APIRouter()


class TwinRequest(BaseModel):
    """Digital twin request."""

    organisation_id: str = "default"
    processing_activities: list[dict] = []
    ai_systems: bool = False
    security_measures: list[str] = []


@router.get("/")
async def twin_status():
    """Get digital twin status."""
    return {
        "status": "active",
        "capabilities": [
            "real-time monitoring",
            "what-if scenarios",
            "predictive alerts",
        ],
    }


@router.post("/create")
async def create_twin(request: TwinRequest):
    """Create a digital twin."""
    report = digital_twin_engine.create_twin(request.organisation_id, request.dict())

    return {
        "organisation_id": report.organisation_id,
        "generated_at": report.generated_at,
        "overall_score": report.overall_score,
        "framework_scores": report.framework_scores,
        "nodes_count": len(report.nodes),
        "edges_count": len(report.edges),
        "nodes": [
            {
                "id": n.node_id,
                "type": n.node_type,
                "name": n.name,
                "status": n.status,
                "score": n.score,
            }
            for n in report.nodes
        ],
        "scenarios": [
            {
                "id": s.scenario_id,
                "description": s.description,
                "predicted_impact": s.predicted_impact,
                "recommended_actions": s.recommended_actions,
            }
            for s in report.scenarios
        ],
        "alerts": report.alerts,
    }
