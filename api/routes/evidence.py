"""Evidence Linking API — Link evidence to assessment sections."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any

router = APIRouter()


# ─── Request/Response Models ──────────────────────────────────


class EvidenceInput(BaseModel):
    """Evidence attachment request."""

    section_id: str = Field(..., description="ID van de assessment-sectie")
    evidence_type: str = Field(..., description="wetgeving, beleid, audit, certificaat")
    title: str = Field(..., min_length=1)
    reference: str = Field(..., min_length=1, description="URL of document-ID")
    description: str = Field(default="")
    verified_by: str = Field(default="")


class EvidenceResponse(BaseModel):
    """Evidence record."""

    id: str
    assessment_id: str
    section_id: str
    evidence_type: str
    title: str
    reference: str
    status: str
    verified_by: str
    verified_at: str


# ─── In-memory store ──────────────────────────────────────────

EVIDENCE: dict[str, list[dict]] = {}


# ─── Endpoints ────────────────────────────────────────────────


@router.get("/{assessment_id}")
async def list_evidence(assessment_id: str):
    """List all evidence for an assessment."""
    return EVIDENCE.get(assessment_id, [])


@router.post("/{assessment_id}", status_code=201)
async def add_evidence(assessment_id: str, request: EvidenceInput):
    """Add evidence to an assessment section."""
    import uuid
    from datetime import datetime

    evidence_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    record = {
        "id": evidence_id,
        "assessment_id": assessment_id,
        "section_id": request.section_id,
        "evidence_type": request.evidence_type,
        "title": request.title,
        "reference": request.reference,
        "description": request.description,
        "verified_by": request.verified_by,
        "verified_at": now,
        "status": "active",
    }

    if assessment_id not in EVIDENCE:
        EVIDENCE[assessment_id] = []
    EVIDENCE[assessment_id].append(record)

    return record


@router.delete("/{assessment_id}/{evidence_id}")
async def remove_evidence(assessment_id: str, evidence_id: str):
    """Remove evidence (soft delete)."""
    if assessment_id not in EVIDENCE:
        raise HTTPException(status_code=404, detail="Assessment not found")

    for item in EVIDENCE[assessment_id]:
        if item["id"] == evidence_id:
            item["status"] = "removed"
            return {"status": "removed", "id": evidence_id}

    raise HTTPException(status_code=404, detail="Evidence not found")


@router.get("/{assessment_id}/coverage")
async def get_evidence_coverage(assessment_id: str):
    """Get evidence coverage report for an assessment."""
    evidence_list = EVIDENCE.get(assessment_id, [])
    active = [e for e in evidence_list if e["status"] == "active"]
    sections = set(e["section_id"] for e in active)

    return {
        "assessment_id": assessment_id,
        "total_evidence": len(active),
        "sections_covered": len(sections),
        "by_type": _group_by_type(active),
    }


def _group_by_type(evidence_list: list[dict]) -> dict:
    result: dict[str, int] = {}
    for e in evidence_list:
        etype = e["evidence_type"]
        result[etype] = result.get(etype, 0) + 1
    return result
