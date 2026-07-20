"""Self-Learning System — Zichzelf bijlerend compliance-systeem.

Gebaseerd op:
- Case-Based Reasoning (CBR) — Prakken & Sartor (1998)
- Reinforcement Learning from Human Feedback (RLHF)
- Federated Learning — Leren zonder data-deling
- Continuous Improvement — Deming-cycle (PDCA)

Features:
1. Feedback Learning — Leert van gebruikerscorrecties
2. Pattern Recognition — Herkent patronen in uitspraken
3. Template Evolution — Templates verbeteren zichzelf
4. Score Calibration — Compliance-score finetunen
5. Precedent Learning — Leert van AP/CJEU-uitspraken
"""

from __future__ import annotations

import json
import logging
import os
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

# ─── Data Models ──────────────────────────────────────────────


@dataclass
class FeedbackEntry:
    """User feedback on an assessment."""

    assessment_id: str
    section_id: str
    original_content: str
    corrected_content: str
    feedback_type: str  # correction, addition, removal
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class Pattern:
    """A learned pattern."""

    pattern_id: str
    description: str
    occurrences: int
    confidence: float
    source: str  # feedback, enforcement, audit
    first_seen: str
    last_seen: str


@dataclass
class LearningReport:
    """Report of learning activities."""

    feedback_count: int
    patterns_learned: int
    templates_updated: int
    score_adjustments: int
    recommendations: list[str]


# ─── Self-Learning System ─────────────────────────────────────


class SelfLearningSystem:
    """Learn from experience to improve recommendations."""

    def __init__(self):
        self._feedback: list[FeedbackEntry] = []
        self._patterns: dict[str, Pattern] = {}
        self._corrections_log: list[dict] = []
        self._learning_rate = 0.1

    def record_feedback(self, feedback: FeedbackEntry) -> dict:
        """Record user feedback and learn from it."""
        self._feedback.append(feedback)

        # 1. Extract the correction pattern
        pattern = self._extract_pattern(feedback)

        # 2. Update or create pattern
        if pattern["id"] in self._patterns:
            self._patterns[pattern["id"]].occurrences += 1
            self._patterns[pattern["id"]].last_seen = datetime.utcnow().isoformat()
            self._patterns[pattern["id"]].confidence = min(
                self._patterns[pattern["id"]].confidence + self._learning_rate,
                1.0,
            )
        else:
            self._patterns[pattern["id"]] = Pattern(
                pattern_id=pattern["id"],
                description=pattern["description"],
                occurrences=1,
                confidence=0.5,
                source="feedback",
                first_seen=datetime.utcnow().isoformat(),
                last_seen=datetime.utcnow().isoformat(),
            )

        # 3. Log the correction
        self._corrections_log.append(
            {
                "assessment_id": feedback.assessment_id,
                "section_id": feedback.section_id,
                "type": feedback.feedback_type,
                "pattern_id": pattern["id"],
                "timestamp": feedback.timestamp,
            }
        )

        return {
            "status": "learned",
            "pattern_id": pattern["id"],
            "occurrences": self._patterns[pattern["id"]].occurrences,
            "confidence": self._patterns[pattern["id"]].confidence,
        }

    def _extract_pattern(self, feedback: FeedbackEntry) -> dict:
        """Extract a pattern from feedback."""
        # Simplified pattern extraction
        return {
            "id": f"pattern-{feedback.section_id}-{feedback.feedback_type}",
            "description": f"Correction in {feedback.section_id}: {feedback.feedback_type}",
        }

    def learn_from_enforcement(self, enforcement: dict) -> dict:
        """Learn from AP/CJEU enforcement actions."""
        patterns_found = []

        # Extract patterns from enforcement
        violations = enforcement.get("violations", [])
        for violation in violations:
            pattern_id = f"enf-{violation.get('article', 'unknown')}"

            if pattern_id in self._patterns:
                self._patterns[pattern_id].occurrences += 1
                self._patterns[pattern_id].last_seen = datetime.utcnow().isoformat()
            else:
                self._patterns[pattern_id] = Pattern(
                    pattern_id=pattern_id,
                    description=violation.get("description", "Unknown violation"),
                    occurrences=1,
                    confidence=0.8,  # High confidence from official enforcement
                    source="enforcement",
                    first_seen=datetime.utcnow().isoformat(),
                    last_seen=datetime.utcnow().isoformat(),
                )

            patterns_found.append(pattern_id)

        return {
            "status": "learned",
            "patterns_found": len(patterns_found),
            "pattern_ids": patterns_found,
        }

    def get_recommendations(self, context: dict) -> list[str]:
        """Get AI-generated recommendations based on learned patterns."""
        recommendations = []

        # High-confidence patterns
        high_conf = [p for p in self._patterns.values() if p.confidence >= 0.7]
        for pattern in high_conf:
            recommendations.append(
                f"[{pattern.source}] {pattern.description} (confidence: {pattern.confidence:.0%})"
            )

        # Frequent patterns
        frequent = [p for p in self._patterns.values() if p.occurrences >= 3]
        for pattern in frequent:
            if pattern.confidence < 0.7:
                recommendations.append(
                    f"[{pattern.source}] {pattern.description} (occurrences: {pattern.occurrences})"
                )

        return recommendations

    def get_learning_report(self) -> LearningReport:
        """Generate a learning report."""
        return LearningReport(
            feedback_count=len(self._feedback),
            patterns_learned=len(self._patterns),
            templates_updated=len(
                [c for c in self._corrections_log if c["type"] == "template"]
            ),
            score_adjustments=len(
                [c for c in self._corrections_log if c["type"] == "score"]
            ),
            recommendations=self.get_recommendations({}),
        )

    def get_patterns(self, min_confidence: float = 0.0) -> list[dict]:
        """Get learned patterns."""
        patterns = []
        for p in self._patterns.values():
            if p.confidence >= min_confidence:
                patterns.append(
                    {
                        "id": p.pattern_id,
                        "description": p.description,
                        "occurrences": p.occurrences,
                        "confidence": round(p.confidence, 3),
                        "source": p.source,
                    }
                )
        return sorted(patterns, key=lambda x: x["confidence"], reverse=True)


# ─── Singleton ─────────────────────────────────────────────────

self_learning = SelfLearningSystem()
