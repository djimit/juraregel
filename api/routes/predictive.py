"""Predictive Compliance API — Voorspellende compliance-analyse."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

from ..predictive_compliance import predictive_engine

router = APIRouter()


class PredictiveRequest(BaseModel):
    """Request for predictive analysis."""

    organisation_id: str = "default"
    compliance_score: float = 50
    previous_compliance_score: float | None = None
    ai_systems: bool = False
    data_categories: list[str] = []
    data_subjects: list[str] = []
    data_subject_count: int = 0
    security_measures: list[str] = []


@router.get("/")
async def predictive_status():
    """Get predictive engine status."""
    return {
        "status": "active",
        "risk_factors": list(predictive_engine.RISK_FACTORS.keys()),
    }


@router.post("/analyze")
async def predict(request: PredictiveRequest):
    """Generate a predictive compliance report."""
    report = predictive_engine.predict(request.organisation_id, request.dict())

    return {
        "organisation_id": report.organisation_id,
        "generated_at": report.generated_at,
        "overall_risk_score": report.overall_risk_score,
        "risk_predictions": [
            {
                "risk_id": r.risk_id,
                "description": r.description,
                "probability": r.probability,
                "impact": r.impact,
                "risk_score": r.risk_score,
                "timeframe": r.timeframe,
                "recommended_actions": r.recommended_actions,
                "related_frameworks": r.related_frameworks,
            }
            for r in report.risk_predictions
        ],
        "trend_analysis": {
            "current_score": report.trend_analysis.current_score,
            "previous_score": report.trend_analysis.previous_score,
            "trend": report.trend_analysis.trend,
            "forecast_30d": report.trend_analysis.forecast_30d,
            "forecast_90d": report.trend_analysis.forecast_90d,
            "forecast_180d": report.trend_analysis.forecast_180d,
        },
        "regulatory_forecast": report.regulatory_forecast,
        "priority_actions": report.priority_actions,
        "early_warnings": report.early_warnings,
    }
