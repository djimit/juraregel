"""CRUD operations — Database-backed operations with RLS.

All operations automatically enforce tenant isolation via RLS.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models


# ─── Organisation ──────────────────────────────────────────────


async def create_organisation(
    session: AsyncSession,
    name: str,
    sector: str,
    size: int | None = None,
    contact_email: str | None = None,
) -> models.Organisation:
    org = models.Organisation(
        name=name, sector=sector, size=size, contact_email=contact_email
    )
    session.add(org)
    await session.flush()
    return org


async def get_organisation(
    session: AsyncSession, org_id: uuid.UUID
) -> models.Organisation | None:
    result = await session.execute(
        select(models.Organisation).where(models.Organisation.id == org_id)
    )
    return result.scalar_one_or_none()


# ─── Processing Activity ───────────────────────────────────────


async def create_processing_activity(
    session: AsyncSession,
    organisation_id: uuid.UUID,
    name: str,
    purpose: str,
    legal_basis: str,
    data_categories: list[str] | None = None,
    data_subjects: list[str] | None = None,
    recipients: list[str] | None = None,
    retention_period: str | None = None,
    security_measures: list[str] | None = None,
) -> models.ProcessingActivity:
    pa = models.ProcessingActivity(
        organisation_id=organisation_id,
        name=name,
        purpose=purpose,
        legal_basis=legal_basis,
        data_categories=data_categories or [],
        data_subjects=data_subjects or [],
        recipients=recipients or [],
        retention_period=retention_period,
        security_measures=security_measures or [],
        dpia_required=_check_dpia_required(data_categories, data_subjects),
    )
    session.add(pa)
    await session.flush()
    return pa


async def list_processing_activities(
    session: AsyncSession,
    organisation_id: uuid.UUID,
) -> list[models.ProcessingActivity]:
    result = await session.execute(
        select(models.ProcessingActivity)
        .where(models.ProcessingActivity.organisation_id == organisation_id)
        .order_by(models.ProcessingActivity.created_at.desc())
    )
    return list(result.scalars().all())


# ─── Assessment ────────────────────────────────────────────────


async def create_assessment(
    session: AsyncSession,
    organisation_id: uuid.UUID,
    assessment_type: str,
    template_id: str,
    content: dict,
    processing_activity_id: uuid.UUID | None = None,
) -> models.Assessment:
    assessment = models.Assessment(
        organisation_id=organisation_id,
        processing_activity_id=processing_activity_id,
        assessment_type=assessment_type,
        template_id=template_id,
        template_version="1.0",
        content=content,
        status="draft",
    )
    session.add(assessment)
    await session.flush()
    return assessment


async def get_assessment(
    session: AsyncSession,
    assessment_id: uuid.UUID,
) -> models.Assessment | None:
    result = await session.execute(
        select(models.Assessment).where(models.Assessment.id == assessment_id)
    )
    return result.scalar_one_or_none()


async def update_assessment_status(
    session: AsyncSession,
    assessment_id: uuid.UUID,
    status: str,
) -> models.Assessment | None:
    assessment = await get_assessment(session, assessment_id)
    if assessment:
        assessment.status = status
        if status == "published":
            assessment.next_review_date = datetime(2027, 7, 20).date()
        await session.flush()
    return assessment


async def list_assessments(
    session: AsyncSession,
    organisation_id: uuid.UUID,
    assessment_type: str | None = None,
    status: str | None = None,
) -> list[models.Assessment]:
    query = select(models.Assessment).where(
        models.Assessment.organisation_id == organisation_id
    )
    if assessment_type:
        query = query.where(models.Assessment.assessment_type == assessment_type)
    if status:
        query = query.where(models.Assessment.status == status)
    result = await session.execute(query.order_by(models.Assessment.created_at.desc()))
    return list(result.scalars().all())


# ─── Evidence ──────────────────────────────────────────────────


async def add_evidence(
    session: AsyncSession,
    assessment_id: uuid.UUID,
    section_id: str,
    evidence_type: str,
    title: str,
    reference: str,
    description: str = "",
    verified_by: str = "",
) -> models.Evidence:
    import hashlib

    content_hash = hashlib.sha256(
        f"{section_id}:{evidence_type}:{title}:{reference}".encode()
    ).hexdigest()

    evidence = models.Evidence(
        assessment_id=assessment_id,
        section_id=section_id,
        evidence_type=evidence_type,
        title=title,
        reference=reference,
        description=description,
        verified_by=verified_by,
        verified_at=datetime.utcnow(),
        content_hash=content_hash,
    )
    session.add(evidence)
    await session.flush()
    return evidence


async def list_evidence(
    session: AsyncSession,
    assessment_id: uuid.UUID,
) -> list[models.Evidence]:
    result = await session.execute(
        select(models.Evidence)
        .where(models.Evidence.assessment_id == assessment_id)
        .where(models.Evidence.status == "active")
    )
    return list(result.scalars().all())


# ─── Audit Trail ───────────────────────────────────────────────


async def log_audit(
    session: AsyncSession,
    entity_type: str,
    entity_id: uuid.UUID,
    action: str,
    actor: str,
    details: dict | None = None,
) -> models.AuditTrail:
    entry = models.AuditTrail(
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        actor=actor,
        details=details,
    )
    session.add(entry)
    await session.flush()
    return entry


# ─── Helpers ───────────────────────────────────────────────────


def _check_dpia_required(
    data_categories: list[str] | None = None,
    data_subjects: list[str] | None = None,
) -> bool:
    """Auto-determine if DPIA is required based on EDPB criteria."""
    score = 0
    sensitive = {
        "biometrische gegevens",
        "gezondheidsgegevens",
        "strafrechtelijke gegevens",
        "etniciteit",
        "religie",
        "seksuele geaardheid",
    }
    vulnerable = {"kinderen", "medewerkers", "patiënten", "kwetsbare groepen"}

    if data_categories and any(cat.lower() in sensitive for cat in data_categories):
        score += 1
    if data_subjects and any(sub.lower() in vulnerable for sub in data_subjects):
        score += 1
    if data_subjects and len(data_subjects) > 3:
        score += 1

    return score >= 2
