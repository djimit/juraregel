"""Drift Detection API — Continuous compliance monitoring."""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Any

from ..drift_detector import drift_detector

router = APIRouter()


class BaselineRequest(BaseModel):
    """Set baseline for drift detection."""

    assessment_id: str
    measures: dict[str, str] = Field(default_factory=dict)
    evidence: list[dict] = Field(default_factory=list)
    next_review_date: str | None = None
    compliance_score: float | None = None


class DriftCheckRequest(BaseModel):
    """Check for drift."""

    assessment_id: str
    organisation_id: str = ""
    measures: dict[str, str] = Field(default_factory=dict)
    evidence: list[dict] = Field(default_factory=list)
    compliance_score: float = 0
    next_review_date: str | None = None


@router.get("/")
async def drift_info():
    """Get drift detector status."""
    return {
        "status": "active",
        "baselines_count": len(drift_detector._baselines),
        "history_count": sum(len(h) for h in drift_detector._history.values()),
    }


@router.post("/baseline")
async def set_baseline(request: BaselineRequest):
    """Set baseline for an assessment."""
    drift_detector.set_baseline(request.assessment_id, request.dict())
    return {"status": "baseline_set", "assessment_id": request.assessment_id}


@router.post("/check")
async def check_drift(request: DriftCheckRequest):
    """Check for drift between baseline and current state."""
    report = drift_detector.detect_drift(request.assessment_id, request.dict())

    return {
        "assessment_id": report.assessment_id,
        "drift_score": report.drift_score,
        "drift_count": len(report.drift_items),
        "score_trend": report.score_trend,
        "previous_score": report.previous_score,
        "drift_items": [
            {
                "type": item.type.value,
                "severity": item.severity.value,
                "description": item.description,
                "expected": item.expected,
                "actual": item.actual,
                "remediation": item.remediation,
                "citation": item.citation,
            }
            for item in report.drift_items
        ],
        "generated_at": report.generated_at,
    }


@router.get("/trend/{assessment_id}")
async def get_trend(assessment_id: str, window: int = 10):
    """Get drift trend over time."""
    trend = drift_detector.get_trend(assessment_id, window)
    return {"assessment_id": assessment_id, "trend": trend}
