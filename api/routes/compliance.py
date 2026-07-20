"""Compliance Scoring API — Real-time compliance scoring."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any

router = APIRouter()


# ─── Request Models ──────────────────────────────────────────


class ScoreRequest(BaseModel):
    """Request to calculate compliance score."""

    content: dict[str, Any] = Field(default_factory=dict)
    evidence_list: list[dict] = Field(default_factory=list)
    measures_implemented: int = 0
    measures_total: int = 0
    incidents_open: int = 0
    incidents_total: int = 0
    training_current: bool = False
    stakeholders_consulted: int = 0
    stakeholders_total: int = 0


# ─── Endpoints ────────────────────────────────────────────────


@router.post("/score")
async def calculate_score(request: ScoreRequest):
    """Calculate compliance score."""
    from ..compliance_score import (
        calculate_compliance_score,
        get_classification_color,
        get_classification_label,
    )

    score = calculate_compliance_score(
        content=request.content,
        evidence_list=request.evidence_list,
        measures_implemented=request.measures_implemented,
        measures_total=request.measures_total,
        incidents_open=request.incidents_open,
        incidents_total=request.incidents_total,
        training_current=request.training_current,
        stakeholders_consulted=request.stakeholders_consulted,
        stakeholders_total=request.stakeholders_total,
    )

    return {
        "score": score.total_score,
        "classification": score.classification,
        "classification_label": get_classification_label(score.classification),
        "classification_color": get_classification_color(score.classification),
        "criteria": [
            {
                "name": c.name,
                "weight": c.weight,
                "raw_score": c.raw_score,
                "weighted_score": c.weighted_score,
                "details": c.details,
            }
            for c in score.criteria
        ],
        "recommendations": score.recommendations,
        "calculated_at": score.calculated_at,
    }


@router.get("/criteria")
async def list_criteria():
    """List scoring criteria and weights."""
    from ..compliance_score import CRITERIA

    return {
        "criteria": [
            {
                "id": key,
                "description": value["description"],
                "weight": value["weight"],
            }
            for key, value in CRITERIA.items()
        ],
        "total_weight": sum(v["weight"] for v in CRITERIA.values()),
    }


@router.get("/classifications")
async def list_classifications():
    """List compliance classifications."""
    from ..compliance_score import get_classification_color, get_classification_label

    classifications = ["excellent", "good", "sufficient", "insufficient", "critical"]
    return {
        "classifications": [
            {
                "id": c,
                "label": get_classification_label(c),
                "color": get_classification_color(c),
            }
            for c in classifications
        ]
    }
