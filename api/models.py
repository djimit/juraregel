"""ORM Models — Multi-tenant compliance data model.

All models include organisation_id for Row Level Security (RLS).
Tenant isolation is enforced at the database level.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


# ─── Organisation ──────────────────────────────────────────────


class Organisation(Base):
    """Multi-tenant organisation."""

    __tablename__ = "organisations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sector: Mapped[str] = mapped_column(String(100), nullable=False)
    size: Mapped[Optional[int]] = mapped_column(Integer)
    kvk_number: Mapped[Optional[str]] = mapped_column(String(20))
    contact_email: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    processing_activities: Mapped[list["ProcessingActivity"]] = relationship(
        back_populates="organisation", cascade="all, delete-orphan"
    )
    assessments: Mapped[list["Assessment"]] = relationship(
        back_populates="organisation", cascade="all, delete-orphan"
    )


# ─── Processing Activity (AVG Art. 30) ────────────────────────


class ProcessingActivity(Base):
    """Verwerkingsactiviteit — AVG Art. 30 Verwerkingsregister."""

    __tablename__ = "processing_activities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    organisation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    purpose: Mapped[str] = mapped_column(Text, nullable=False)
    legal_basis: Mapped[str] = mapped_column(String(50), nullable=False)
    data_categories: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    data_subjects: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    recipients: Mapped[list] = mapped_column(JSON, default=list)
    retention_period: Mapped[Optional[str]] = mapped_column(String(100))
    security_measures: Mapped[list] = mapped_column(JSON, default=list)
    dpia_required: Mapped[bool] = mapped_column(Boolean, default=False)
    dpia_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assessments.id"), nullable=True
    )
    fria_required: Mapped[bool] = mapped_column(Boolean, default=False)
    fria_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assessments.id"), nullable=True
    )
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    organisation: Mapped["Organisation"] = relationship(
        back_populates="processing_activities"
    )
    assessments: Mapped[list["Assessment"]] = relationship(
        back_populates="processing_activity",
        foreign_keys="Assessment.processing_activity_id",
    )

    __table_args__ = (
        Index("idx_pa_org", "organisation_id"),
        Index("idx_pa_status", "status"),
    )


# ─── Assessment ────────────────────────────────────────────────


class Assessment(Base):
    """Compliance assessment — DPIA, FRIA, IAMA, LIA, TIA, etc."""

    __tablename__ = "assessments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    organisation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
    )
    processing_activity_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("processing_activities.id"), nullable=True
    )
    assessment_type: Mapped[str] = mapped_column(String(50), nullable=False)
    template_id: Mapped[str] = mapped_column(String(100), nullable=False)
    template_version: Mapped[str] = mapped_column(
        String(20), nullable=False, default="1.0"
    )
    status: Mapped[str] = mapped_column(String(20), default="draft")
    content: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    compliance_score: Mapped[Optional[float]] = mapped_column(Numeric(5, 2))
    next_review_date: Mapped[Optional[datetime]] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    organisation: Mapped["Organisation"] = relationship(back_populates="assessments")
    processing_activity: Mapped[Optional["ProcessingActivity"]] = relationship(
        back_populates="assessments",
        foreign_keys=[processing_activity_id],
    )
    evidence: Mapped[list["Evidence"]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan"
    )
    approvals: Mapped[list["Approval"]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan"
    )
    ai_claims: Mapped[list["AIClaim"]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_assessments_org", "organisation_id"),
        Index("idx_assessments_status", "status"),
        Index("idx_assessments_type", "assessment_type"),
    )


# ─── Evidence ──────────────────────────────────────────────────


class Evidence(Base):
    """Evidence linked to assessment sections."""

    __tablename__ = "evidence"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assessments.id", ondelete="CASCADE"),
        nullable=False,
    )
    section_id: Mapped[str] = mapped_column(String(100), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    reference: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    verified_by: Mapped[Optional[str]] = mapped_column(String(255))
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    expiry_date: Mapped[Optional[datetime]] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="active")
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    assessment: Mapped["Assessment"] = relationship(back_populates="evidence")

    __table_args__ = (Index("idx_evidence_assessment", "assessment_id"),)


# ─── Approval ──────────────────────────────────────────────────


class Approval(Base):
    """Assessment approval record."""

    __tablename__ = "approvals"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assessments.id", ondelete="CASCADE"),
        nullable=False,
    )
    approver: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    comments: Mapped[Optional[str]] = mapped_column(Text)
    signature_hash: Mapped[Optional[str]] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    assessment: Mapped["Assessment"] = relationship(back_populates="approvals")


# ─── Regulatory Change ─────────────────────────────────────────


class RegulatoryChange(Base):
    """Detected regulatory change with impact analysis."""

    __tablename__ = "regulatory_changes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    effective_date: Mapped[Optional[datetime]] = mapped_column(Date)
    impact_score: Mapped[Optional[float]] = mapped_column(Numeric(3, 2))
    affected_frameworks: Mapped[list] = mapped_column(JSON, default=list)
    affected_processing_activities: Mapped[list] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(20), default="detected")
    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        Index("idx_rc_status", "status"),
        Index("idx_rc_source", "source"),
    )


# ─── AI Claims Log ─────────────────────────────────────────────


class AIClaim(Base):
    """Log of AI-generated claims for hallucination tracking."""

    __tablename__ = "ai_claims"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assessments.id", ondelete="CASCADE"),
        nullable=False,
    )
    claim: Mapped[str] = mapped_column(Text, nullable=False)
    citations: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    confidence: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    hallucination_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    model_version: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    assessment: Mapped["Assessment"] = relationship(back_populates="ai_claims")

    __table_args__ = (Index("idx_ai_claims_assessment", "assessment_id"),)


# ─── Audit Trail (Immutable) ──────────────────────────────────


class AuditTrail(Base):
    """Immutable audit trail — append-only."""

    __tablename__ = "audit_trail"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    actor: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[Optional[dict]] = mapped_column(JSON)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (Index("idx_audit_entity", "entity_type", "entity_id"),)
