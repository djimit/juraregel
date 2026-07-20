"""ORM Models — Multi-tenant compliance data model.
Requires SQLAlchemy. If not available, models are not defined.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

try:
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

    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False


if HAS_SQLALCHEMY:
    from .database import Base

    class Organisation(Base):
        __tablename__ = "organisations"
        id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
        )
        name: Mapped[str] = mapped_column(String(255), nullable=False)
        sector: Mapped[str] = mapped_column(String(100), nullable=False)
        size: Mapped[Optional[int]] = mapped_column(Integer)
        contact_email: Mapped[Optional[str]] = mapped_column(String(255))
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), server_default=func.now()
        )
        updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        )
        processing_activities: Mapped[list["ProcessingActivity"]] = relationship(
            back_populates="organisation", cascade="all, delete-orphan"
        )
        assessments: Mapped[list["Assessment"]] = relationship(
            back_populates="organisation", cascade="all, delete-orphan"
        )

    class ProcessingActivity(Base):
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
        data_categories: Mapped[list] = mapped_column(
            JSON, nullable=False, default=list
        )
        data_subjects: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
        dpia_required: Mapped[bool] = mapped_column(Boolean, default=False)
        status: Mapped[str] = mapped_column(String(20), default="active")
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), server_default=func.now()
        )
        updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
        )
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

    class Assessment(Base):
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
        organisation: Mapped["Organisation"] = relationship(
            back_populates="assessments"
        )
        processing_activity: Mapped[Optional["ProcessingActivity"]] = relationship(
            back_populates="assessments", foreign_keys=[processing_activity_id]
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
        )

    class Evidence(Base):
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
        content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
        status: Mapped[str] = mapped_column(String(20), default="active")
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), server_default=func.now()
        )
        assessment: Mapped["Assessment"] = relationship(back_populates="evidence")

    class Approval(Base):
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
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), server_default=func.now()
        )
        assessment: Mapped["Assessment"] = relationship(back_populates="approvals")

    class RegulatoryChange(Base):
        __tablename__ = "regulatory_changes"
        id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
        )
        source: Mapped[str] = mapped_column(String(100), nullable=False)
        title: Mapped[str] = mapped_column(String(500), nullable=False)
        summary: Mapped[str] = mapped_column(Text, nullable=False)
        impact_score: Mapped[Optional[float]] = mapped_column(Numeric(3, 2))
        status: Mapped[str] = mapped_column(String(20), default="detected")
        detected_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), server_default=func.now()
        )

    class AIClaim(Base):
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
        confidence: Mapped[float] = mapped_column(Numeric(3, 2), nullable=False)
        hallucination_flag: Mapped[bool] = mapped_column(Boolean, default=False)
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), server_default=func.now()
        )
        assessment: Mapped["Assessment"] = relationship(back_populates="ai_claims")

    class AuditTrail(Base):
        __tablename__ = "audit_trail"
        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
        entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
        action: Mapped[str] = mapped_column(String(50), nullable=False)
        actor: Mapped[str] = mapped_column(String(255), nullable=False)
        details: Mapped[Optional[dict]] = mapped_column(JSON)
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), server_default=func.now()
        )

else:
    # Fallback: empty classes for type hints
    Organisation = ProcessingActivity = Assessment = None
    Evidence = Approval = RegulatoryChange = None
    AIClaim = AuditTrail = None
