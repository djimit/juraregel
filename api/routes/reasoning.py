"""Legal Reasoning API — Juridische redenering met Toulmin-argumentatie."""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Any

from ..legal_reasoning_engine import legal_reasoning_engine

router = APIRouter()


class ReasoningRequest(BaseModel):
    """Request for legal reasoning."""

    question: str = Field(..., min_length=1, description="De juridische vraag")
    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Context (verwerkingsactiviteit, AI-systeem, etc.)",
    )


@router.get("/")
async def reasoning_status():
    """Get reasoning engine status."""
    return {
        "status": "active",
        "schemes": [s.__class__.__name__ for s in legal_reasoning_engine.schemes],
    }


@router.post("/analyze")
async def analyze(request: ReasoningRequest):
    """Perform legal reasoning on a question."""
    result = legal_reasoning_engine.reason(request.question, request.context)

    return {
        "question": result.question,
        "conclusion": result.conclusion,
        "overall_confidence": result.overall_confidence,
        "human_review_required": result.human_review_required,
        "arguments": [
            {
                "claim": arg.claim,
                "grounds": arg.grounds,
                "warrant": arg.warrant,
                "backing": arg.backing,
                "qualifier": arg.qualifier.value,
                "confidence": arg.confidence,
                "articles": arg.articles,
                "rebuttal": arg.rebuttal,
            }
            for arg in result.arguments
        ],
        "counter_arguments": [
            {
                "claim": arg.claim,
                "confidence": arg.confidence,
            }
            for arg in result.counter_arguments
        ],
        "gaps": result.gaps,
        "reasoning_chain": result.reasoning_chain,
        "model": result.model,
        "execution_time_ms": result.execution_time_ms,
    }
