"""Multi-Jurisdiction API — Analyse over meerdere rechtsgebieden."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

from ..multi_jurisdiction import multi_jurisdiction_engine

router = APIRouter()


class JurisdictionRequest(BaseModel):
    """Multi-jurisdiction analysis request."""

    processing_activity: dict[str, Any]


@router.get("/")
async def jurisdiction_status():
    """Get jurisdiction engine status."""
    return {
        "status": "active",
        "jurisdictions": ["NL", "EU", "INT"],
        "frameworks": list(multi_jurisdiction_engine.FRAMEWORK_RULES.keys()),
    }


@router.post("/analyze")
async def analyze_jurisdictions(request: JurisdictionRequest):
    """Analyze compliance across multiple jurisdictions."""
    report = multi_jurisdiction_engine.analyze(request.processing_activity)

    return {
        "applicable_frameworks": report.applicable_frameworks,
        "obligations": [
            {
                "jurisdiction": ob.jurisdiction.value,
                "framework": ob.framework,
                "article": ob.article,
                "title": ob.title,
                "description": ob.description,
                "requirement": ob.requirement,
                "deadline": ob.deadline,
                "penalty": ob.penalty,
                "url": ob.url,
            }
            for ob in report.obligations
        ],
        "conflicts": [
            {
                "type": c.conflict_type,
                "severity": c.severity,
                "framework_a": c.obligation_a.framework,
                "framework_b": c.obligation_b.framework,
                "resolution": c.resolution_hint,
            }
            for c in report.conflicts
        ],
        "gaps": report.gaps,
        "recommendations": report.recommendations,
    }
