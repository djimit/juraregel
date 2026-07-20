"""Processing Activity API — AVG Art. 30 Verwerkingsregister."""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Any

router = APIRouter()


# ─── Request/Response Models ──────────────────────────────────


class ProcessingActivityInput(BaseModel):
    """Processing activity registration."""

    name: str = Field(..., min_length=1, description="Naam van de verwerking")
    purpose: str = Field(..., min_length=1, description="Doel van de verwerking")
    legal_basis: str = Field(..., description="AVG Art. 6(1)(a-f)")
    data_categories: list[str] = Field(default_factory=list)
    data_subjects: list[str] = Field(default_factory=list)
    recipients: list[str] = Field(default_factory=list)
    retention_period: str = Field(default="")
    security_measures: list[str] = Field(default_factory=list)


class ProcessingActivity(ProcessingActivityInput):
    """Full processing activity record."""

    id: str
    organisation_id: str
    dpia_required: bool = False
    fria_required: bool = False
    status: str = "active"
    created_at: str
    updated_at: str


# ─── In-memory store (placeholder for PostgreSQL) ─────────────

PROCESSING_ACTIVITIES: dict[str, dict] = {}


# ─── Endpoints ────────────────────────────────────────────────


@router.get("/")
async def list_processing_activities(
    organisation_id: str | None = Query(None),
    status: str | None = Query(None),
    dpia_required: bool | None = Query(None),
):
    """List processing activities with optional filters."""
    results = []
    for pid, pa in PROCESSING_ACTIVITIES.items():
        if organisation_id and pa["organisation_id"] != organisation_id:
            continue
        if status and pa["status"] != status:
            continue
        if dpia_required is not None and pa["dpia_required"] != dpia_required:
            continue
        results.append(pa)
    return results


@router.post("/", status_code=201)
async def create_processing_activity(
    organisation_id: str,
    request: ProcessingActivityInput,
):
    """Register a new processing activity."""
    import uuid
    from datetime import datetime

    pa_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    # Auto-determine if DPIA is required based on 9 EDPB criteria
    dpia_required = _check_dpia_required(request.dict())

    activity = {
        "id": pa_id,
        "organisation_id": organisation_id,
        **request.dict(),
        "dpia_required": dpia_required,
        "fria_required": False,  # Would need AI classification
        "status": "active",
        "created_at": now,
        "updated_at": now,
    }

    PROCESSING_ACTIVITIES[pa_id] = activity
    return activity


@router.get("/{activity_id}")
async def get_processing_activity(activity_id: str):
    """Get processing activity by ID."""
    if activity_id not in PROCESSING_ACTIVITIES:
        raise HTTPException(status_code=404, detail="Processing activity not found")
    return PROCESSING_ACTIVITIES[activity_id]


@router.put("/{activity_id}")
async def update_processing_activity(
    activity_id: str, request: ProcessingActivityInput
):
    """Update processing activity."""
    if activity_id not in PROCESSING_ACTIVITIES:
        raise HTTPException(status_code=404, detail="Processing activity not found")

    activity = PROCESSING_ACTIVITIES[activity_id]
    for key, value in request.dict().items():
        activity[key] = value

    activity["dpia_required"] = _check_dpia_required(request.dict())
    activity["updated_at"] = __import__("datetime").datetime.utcnow().isoformat()
    return activity


@router.get("/{activity_id}/compliance")
async def get_compliance_status(activity_id: str):
    """Get compliance status for a processing activity."""
    if activity_id not in PROCESSING_ACTIVITIES:
        raise HTTPException(status_code=404, detail="Processing activity not found")

    activity = PROCESSING_ACTIVITIES[activity_id]

    return {
        "activity_id": activity_id,
        "dpia_required": activity["dpia_required"],
        "dpia_completed": False,  # Would check assessments store
        "fria_required": activity["fria_required"],
        "fria_completed": False,
        "compliance_score": None,
        "next_review_date": None,
    }


def _check_dpia_required(data: dict) -> bool:
    """Auto-determine if DPIA is required based on EDPB criteria."""
    score = 0

    # Criterion 4: Sensitive data
    sensitive = {
        "biometrische gegevens",
        "gezondheidsgegevens",
        "strafrechtelijke gegevens",
        "etniciteit",
        "religie",
        "seksuele geaardheid",
    }
    if any(cat.lower() in sensitive for cat in data.get("data_categories", [])):
        score += 1

    # Criterion 5: Large scale
    if len(data.get("data_subjects", [])) > 3:  # Proxy for large scale
        score += 1

    # Criterion 7: Vulnerable subjects
    vulnerable = {"kinderen", "medewerkers", "patiënten", "kwetsbare groepen"}
    if any(sub.lower() in vulnerable for sub in data.get("data_subjects", [])):
        score += 1

    return score >= 2
