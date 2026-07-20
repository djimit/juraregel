"""Assessment Service API — CRUD + workflow + export."""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Any
from datetime import date

router = APIRouter()


# ─── Request/Response Models ──────────────────────────────────


class CreateAssessmentRequest(BaseModel):
    """Request to create a new assessment."""

    organisation_id: str = Field(..., description="ID van de organisatie")
    processing_activity_id: str | None = Field(
        None, description="ID van de verwerkingsactiviteit"
    )
    assessment_type: str = Field(
        ..., description="Type: dpia, fria, iama, lia, tia, bias_audit"
    )
    template_id: str = Field(..., description="Template ID")
    parameters: dict[str, Any] = Field(default_factory=dict)


class ApprovalRequest(BaseModel):
    """Request to approve an assessment."""

    approver: str = Field(..., description="Naam van de goedkeurder")
    role: str = Field(..., description="Rol: FG, AI-verantwoordelijke, Management")
    comments: str = Field(default="")


class AssessmentResponse(BaseModel):
    """Assessment response."""

    id: str
    organisation_id: str
    assessment_type: str
    template_id: str
    status: str
    content: dict
    compliance_score: float | None
    created_at: str
    updated_at: str


# ─── In-memory store (placeholder for PostgreSQL) ─────────────

ASSESSMENTS: dict[str, dict] = {}


# ─── Endpoints ────────────────────────────────────────────────


@router.get("/")
async def list_assessments(
    organisation_id: str | None = Query(None),
    assessment_type: str | None = Query(None),
    status: str | None = Query(None),
):
    """List assessments with optional filters."""
    results = []
    for aid, assessment in ASSESSMENTS.items():
        if organisation_id and assessment["organisation_id"] != organisation_id:
            continue
        if assessment_type and assessment["assessment_type"] != assessment_type:
            continue
        if status and assessment["status"] != status:
            continue
        results.append(assessment)
    return results


@router.post("/", response_model=AssessmentResponse, status_code=201)
async def create_assessment(request: CreateAssessmentRequest):
    """Create a new assessment from a template."""
    import uuid
    from datetime import datetime
    from docs.templates import generate_document, enrich_document, validate_document

    # Generate document from template
    doc = generate_document(
        request.template_id, request.organisation_id, **request.parameters
    )
    if "error" in doc:
        raise HTTPException(status_code=404, detail=doc["error"])

    enriched = enrich_document(doc)

    assessment_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    assessment = {
        "id": assessment_id,
        "organisation_id": request.organisation_id,
        "processing_activity_id": request.processing_activity_id,
        "assessment_type": request.assessment_type,
        "template_id": request.template_id,
        "status": "draft",
        "content": enriched,
        "compliance_score": None,
        "approvals": [],
        "created_at": now,
        "updated_at": now,
    }

    ASSESSMENTS[assessment_id] = assessment
    return assessment


@router.get("/{assessment_id}")
async def get_assessment(assessment_id: str):
    """Get assessment by ID."""
    if assessment_id not in ASSESSMENTS:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return ASSESSMENTS[assessment_id]


@router.put("/{assessment_id}")
async def update_assessment(assessment_id: str, request: CreateAssessmentRequest):
    """Update assessment content."""
    if assessment_id not in ASSESSMENTS:
        raise HTTPException(status_code=404, detail="Assessment not found")

    assessment = ASSESSMENTS[assessment_id]
    if assessment["status"] not in ("draft",):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot update assessment in status: {assessment['status']}",
        )

    from docs.templates import generate_document, enrich_document

    doc = generate_document(
        request.template_id, request.organisation_id, **request.parameters
    )
    enriched = enrich_document(doc)

    assessment["content"] = enriched
    assessment["template_id"] = request.template_id
    assessment["updated_at"] = __import__("datetime").datetime.utcnow().isoformat()

    return assessment


@router.post("/{assessment_id}/submit")
async def submit_for_review(assessment_id: str):
    """Submit assessment for review."""
    if assessment_id not in ASSESSMENTS:
        raise HTTPException(status_code=404, detail="Assessment not found")

    assessment = ASSESSMENTS[assessment_id]
    if assessment["status"] != "draft":
        raise HTTPException(
            status_code=400, detail="Only draft assessments can be submitted"
        )

    assessment["status"] = "in_review"
    assessment["updated_at"] = __import__("datetime").datetime.utcnow().isoformat()
    return assessment


@router.post("/{assessment_id}/approve")
async def approve_assessment(assessment_id: str, request: ApprovalRequest):
    """Approve an assessment."""
    if assessment_id not in ASSESSMENTS:
        raise HTTPException(status_code=404, detail="Assessment not found")

    assessment = ASSESSMENTS[assessment_id]
    if assessment["status"] not in ("in_review", "draft"):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot approve assessment in status: {assessment['status']}",
        )

    from datetime import datetime

    approval = {
        "approver": request.approver,
        "role": request.role,
        "comments": request.comments,
        "date": datetime.utcnow().isoformat(),
    }
    assessment["approvals"].append(approval)
    assessment["status"] = "approved"
    assessment["updated_at"] = datetime.utcnow().isoformat()
    return assessment


@router.post("/{assessment_id}/publish")
async def publish_assessment(assessment_id: str):
    """Publish an approved assessment."""
    if assessment_id not in ASSESSMENTS:
        raise HTTPException(status_code=404, detail="Assessment not found")

    assessment = ASSESSMENTS[assessment_id]
    if assessment["status"] != "approved":
        raise HTTPException(
            status_code=400, detail="Only approved assessments can be published"
        )

    assessment["status"] = "published"
    assessment["updated_at"] = __import__("datetime").datetime.utcnow().isoformat()
    return assessment


@router.post("/{assessment_id}/archive")
async def archive_assessment(assessment_id: str):
    """Archive a published assessment."""
    if assessment_id not in ASSESSMENTS:
        raise HTTPException(status_code=404, detail="Assessment not found")

    assessment = ASSESSMENTS[assessment_id]
    if assessment["status"] != "published":
        raise HTTPException(
            status_code=400, detail="Only published assessments can be archived"
        )

    assessment["status"] = "archived"
    assessment["updated_at"] = __import__("datetime").datetime.utcnow().isoformat()
    return assessment


@router.get("/{assessment_id}/export")
async def export_assessment(assessment_id: str, format: str = Query("markdown")):
    """Export assessment to a specific format."""
    if assessment_id not in ASSESSMENTS:
        raise HTTPException(status_code=404, detail="Assessment not found")

    assessment = ASSESSMENTS[assessment_id]

    if format == "json":
        return assessment
    elif format in ("markdown", "html", "structured"):
        from docs.templates.render_engine import render_document

        # Re-render from template with stored parameters
        content = assessment.get("content", {})
        return {
            "assessment_id": assessment_id,
            "format": format,
            "content": content,
        }
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")
