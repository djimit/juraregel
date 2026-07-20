"""Report Generator API — Professionele compliance-documenten."""

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import Any

from ..report_generator import report_generator

router = APIRouter()


class ReportRequest(BaseModel):
    """Report generation request."""

    report_type: str = "dpia"  # dpia, fria, iama, compliance_declaration
    organisation: str = "Organisatie"
    processing_activity: dict[str, Any]


@router.get("/")
async def report_types():
    """List available report types."""
    return {
        "types": [
            {"id": k, "title": v["title"], "framework": v["framework"]}
            for k, v in report_generator.REPORT_TYPES.items()
        ]
    }


@router.post("/generate")
async def generate_report(request: ReportRequest):
    """Generate a compliance report."""
    report = report_generator.generate(
        report_type=request.report_type,
        organisation=request.organisation,
        processing_activity=request.processing_activity,
    )

    return {
        "report_id": report.report_id,
        "type": report.report_type,
        "title": report.title,
        "organisation": report.organisation,
        "confidence": report.overall_confidence,
        "model_used": report.model_used,
        "sections": [
            {
                "title": s.title,
                "content": s.content,
                "citations": s.citations,
                "confidence": s.confidence,
            }
            for s in report.sections
        ],
        "generated_at": report.generated_at,
    }


@router.post("/generate/markdown", response_class=PlainTextResponse)
async def generate_markdown(request: ReportRequest):
    """Generate a compliance report as Markdown."""
    report = report_generator.generate(
        report_type=request.report_type,
        organisation=request.organisation,
        processing_activity=request.processing_activity,
    )

    return report_generator.render_markdown(report)
