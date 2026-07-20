"""Compliance Scoring Engine — Real-time compliance score calculation.

Formula: CS = Σ(wᵢ × sᵢ) / Σ(wᵢ)

Where:
    CS  = Compliance Score (0-100)
    wᵢ  = Weight per criterion
    sᵢ  = Normalized score per criterion (0-1)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


# ─── Criteria Weights ──────────────────────────────────────────

CRITERIA = {
    "documentation_completeness": {
        "weight": 0.20,
        "description": "Documentatie Compleetheid",
    },
    "evidence_actuality": {"weight": 0.15, "description": "Evidence Actualiteit"},
    "review_timeliness": {"weight": 0.15, "description": "Review-Termijnen"},
    "measures_implementation": {
        "weight": 0.20,
        "description": "Maatregelen-Implementatie",
    },
    "incident_handling": {"weight": 0.10, "description": "Incidenten-Afhandeling"},
    "training_actuality": {"weight": 0.10, "description": "Training Actualiteit"},
    "stakeholder_consultation": {
        "weight": 0.10,
        "description": "Stakeholder-Consultatie",
    },
}


@dataclass
class CriterionScore:
    """Score for a single criterion."""

    name: str
    weight: float
    raw_score: float  # 0-1
    weighted_score: float
    details: str


@dataclass
class ComplianceScore:
    """Full compliance score result."""

    total_score: float  # 0-100
    classification: str  # excellent, good, sufficient, insufficient, critical
    criteria: list[CriterionScore]
    recommendations: list[str]
    calculated_at: str


def calculate_completeness(content: dict) -> float:
    """Calculate documentation completeness (0-1)."""
    if not content:
        return 0.0

    inhoud = content.get("inhoud", {})
    if not inhoud:
        return 0.0

    total_fields = 0
    filled_fields = 0

    for section_key, section in inhoud.items():
        if isinstance(section, dict):
            for key, value in section.items():
                if key == "content":
                    total_fields += 1
                    if value and isinstance(value, str) and "[" not in value:
                        filled_fields += 1
                elif isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        total_fields += 1
                        if (
                            sub_value
                            and isinstance(sub_value, str)
                            and "[" not in sub_value
                        ):
                            filled_fields += 1

    return filled_fields / total_fields if total_fields > 0 else 0.0


def calculate_evidence_actuality(evidence_list: list[dict]) -> float:
    """Calculate evidence actuality (0-1)."""
    if not evidence_list:
        return 0.0

    now = datetime.utcnow()
    valid_count = 0

    for evidence in evidence_list:
        expiry = evidence.get("expiry_date")
        if expiry:
            expiry_date = (
                datetime.fromisoformat(expiry) if isinstance(expiry, str) else expiry
            )
            if expiry_date > now:
                valid_count += 1
        else:
            valid_count += 1

    return valid_count / len(evidence_list)


def calculate_review_timeliness(next_review_date: datetime | None) -> float:
    """Calculate review timeliness (0-1)."""
    if not next_review_date:
        return 0.0

    now = datetime.utcnow().date()
    if isinstance(next_review_date, str):
        next_review_date = datetime.fromisoformat(next_review_date).date()

    if next_review_date > now:
        # Review is in the future — calculate how far
        days_until = (next_review_date - now).days
        if days_until > 180:
            return 1.0
        elif days_until > 90:
            return 0.8
        elif days_until > 30:
            return 0.6
        else:
            return 0.4
    else:
        # Review is overdue
        days_overdue = (now - next_review_date).days
        if days_overdue > 365:
            return 0.0
        elif days_overdue > 180:
            return 0.2
        else:
            return 0.4


def calculate_compliance_score(
    content: dict | None = None,
    evidence_list: list[dict] | None = None,
    next_review_date: datetime | None = None,
    measures_implemented: int = 0,
    measures_total: int = 0,
    incidents_open: int = 0,
    incidents_total: int = 0,
    training_current: bool = False,
    stakeholders_consulted: int = 0,
    stakeholders_total: int = 0,
) -> ComplianceScore:
    """Calculate the full compliance score."""

    criteria_scores = []

    # 1. Documentation Completeness (20%)
    completeness = calculate_completeness(content or {})
    criteria_scores.append(
        CriterionScore(
            name="documentation_completeness",
            weight=CRITERIA["documentation_completeness"]["weight"],
            raw_score=completeness,
            weighted_score=completeness
            * CRITERIA["documentation_completeness"]["weight"],
            details=f"{completeness * 100:.0f}% secties ingevuld",
        )
    )

    # 2. Evidence Actuality (15%)
    evidence = calculate_evidence_actuality(evidence_list or [])
    criteria_scores.append(
        CriterionScore(
            name="evidence_actuality",
            weight=CRITERIA["evidence_actuality"]["weight"],
            raw_score=evidence,
            weighted_score=evidence * CRITERIA["evidence_actuality"]["weight"],
            details=f"{evidence * 100:.0f}% bewijsstukken actueel",
        )
    )

    # 3. Review Timeliness (15%)
    review = calculate_review_timeliness(next_review_date)
    criteria_scores.append(
        CriterionScore(
            name="review_timeliness",
            weight=CRITERIA["review_timeliness"]["weight"],
            raw_score=review,
            weighted_score=review * CRITERIA["review_timeliness"]["weight"],
            details=f"Review-status: {'actueel' if review > 0.6 else 'aandacht nodig'}",
        )
    )

    # 4. Measures Implementation (20%)
    measures = measures_implemented / measures_total if measures_total > 0 else 0.0
    criteria_scores.append(
        CriterionScore(
            name="measures_implementation",
            weight=CRITERIA["measures_implementation"]["weight"],
            raw_score=measures,
            weighted_score=measures * CRITERIA["measures_implementation"]["weight"],
            details=f"{measures_implemented}/{measures_total} maatregelen geïmplementeerd",
        )
    )

    # 5. Incident Handling (10%)
    incidents = 1.0 - (incidents_open / incidents_total if incidents_total > 0 else 0.0)
    criteria_scores.append(
        CriterionScore(
            name="incident_handling",
            weight=CRITERIA["incident_handling"]["weight"],
            raw_score=incidents,
            weighted_score=incidents * CRITERIA["incident_handling"]["weight"],
            details=f"{incidents_open} openstaande incidenten",
        )
    )

    # 6. Training Actuality (10%)
    training = 1.0 if training_current else 0.0
    criteria_scores.append(
        CriterionScore(
            name="training_actuality",
            weight=CRITERIA["training_actuality"]["weight"],
            raw_score=training,
            weighted_score=training * CRITERIA["training_actuality"]["weight"],
            details="Training actueel" if training_current else "Training verlopen",
        )
    )

    # 7. Stakeholder Consultation (10%)
    stakeholders = (
        stakeholders_consulted / stakeholders_total if stakeholders_total > 0 else 0.0
    )
    criteria_scores.append(
        CriterionScore(
            name="stakeholder_consultation",
            weight=CRITERIA["stakeholder_consultation"]["weight"],
            raw_score=stakeholders,
            weighted_score=stakeholders
            * CRITERIA["stakeholder_consultation"]["weight"],
            details=f"{stakeholders_consulted}/{stakeholders_total} stakeholders geraadpleegd",
        )
    )

    # Total
    total_weight = sum(c.weight for c in criteria_scores)
    total_score = (
        sum(c.weighted_score for c in criteria_scores) / total_weight * 100
        if total_weight > 0
        else 0
    )

    # Classification
    if total_score >= 90:
        classification = "excellent"
    elif total_score >= 75:
        classification = "good"
    elif total_score >= 60:
        classification = "sufficient"
    elif total_score >= 40:
        classification = "insufficient"
    else:
        classification = "critical"

    # Recommendations
    recommendations = []
    for c in criteria_scores:
        if c.raw_score < 0.5:
            recommendations.append(
                f"Verbeter {CRITERIA[c.name]['description']}: {c.details}"
            )

    return ComplianceScore(
        total_score=round(total_score, 1),
        classification=classification,
        criteria=criteria_scores,
        recommendations=recommendations,
        calculated_at=datetime.utcnow().isoformat(),
    )


def get_classification_label(classification: str) -> str:
    """Get human-readable classification label."""
    labels = {
        "excellent": "🟢 Excellent",
        "good": "🟢 Goed",
        "sufficient": "🟡 Voldoende",
        "insufficient": "🟠 Onvoldoende",
        "critical": "🔴 Kritiek",
    }
    return labels.get(classification, classification)


def get_classification_color(classification: str) -> str:
    """Get color for classification."""
    colors = {
        "excellent": "#38a169",
        "good": "#38a169",
        "sufficient": "#d69e2e",
        "insufficient": "#dd6b20",
        "critical": "#e53e3e",
    }
    return colors.get(classification, "#718096")
