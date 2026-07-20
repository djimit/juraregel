"""Self-Learning API — Feedback en patroon-herkenning."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

from ..self_learning import self_learning, FeedbackEntry

router = APIRouter()


class FeedbackRequest(BaseModel):
    """User feedback."""

    assessment_id: str
    section_id: str
    original_content: str
    corrected_content: str
    feedback_type: str = "correction"


@router.get("/")
async def learning_status():
    """Get learning system status."""
    report = self_learning.get_learning_report()
    return {
        "status": "active",
        "feedback_count": report.feedback_count,
        "patterns_learned": report.patterns_learned,
        "templates_updated": report.templates_updated,
    }


@router.get("/patterns")
async def get_patterns(min_confidence: float = 0.0):
    """Get learned patterns."""
    patterns = self_learning.get_patterns(min_confidence)
    return {"patterns": patterns, "count": len(patterns)}


@router.get("/recommendations")
async def get_recommendations():
    """Get AI-generated recommendations."""
    recs = self_learning.get_recommendations({})
    return {"recommendations": recs}


@router.post("/feedback")
async def record_feedback(request: FeedbackRequest):
    """Record user feedback."""
    feedback = FeedbackEntry(
        assessment_id=request.assessment_id,
        section_id=request.section_id,
        original_content=request.original_content,
        corrected_content=request.corrected_content,
        feedback_type=request.feedback_type,
    )
    result = self_learning.record_feedback(feedback)
    return result


@router.post("/learn-from-enforcement")
async def learn_from_enforcement(enforcement: dict):
    """Learn from enforcement actions."""
    result = self_learning.learn_from_enforcement(enforcement)
    return result
