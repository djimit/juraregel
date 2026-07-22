"""RAG Engine Auditor — apply JLAIF to the JuraRegel RAG engine.

Audits the RAG engine output for all 9 error types:
1. Feitelijke fout — incorrect facts
2. Bronfout — missing or wrong citations
3. Interpretatiefout — wrong legal interpretation
4. Jurisdictiefout — wrong jurisdiction
5. Temporaliteitsfout — outdated legislation/case law
6. Procedurefout — procedural error
7. Omissiefout — missed relevant information
8. Bias — systematic preference
9. Vertrouwelijkheidsincident — PII leak

Each finding is classified by severity (S1-S5) and fed to the
severity scorer for release decisions.
"""

from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .error_taxonomy import (
    LegalError,
    LegalErrorType,
    Severity,
    SeverityDistribution,
)
from .severity_scorer import UseCaseProfile, score_system

logger = logging.getLogger(__name__)

# ─── Known legal patterns for automated checking ────────────────

CITATION_PATTERNS = [
    r"Art\.?\s*\d+",  # Artikel verwijzing
    r"§\s*\d+",  # Paragraaf
    r"EB|EDPB",  # Europees Toezicht
    r"ECLI:",  # European Case Law Identifier
    r"CLI\.[A-Z]+\.\d+",  # CLI identifier
    r"[A-Z][a-z]+\s+voor\s+\d{4}",  # Case name voor jaartal
]

PII_PATTERNS = [
    r"\b\d{9}\b",  # BSN
    r"\b[A-Z]{2}\d{6}\b",  # Paspoort
    r"\b\d{4}\s?[A-Z]{2}\b",  # Postcode
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Z|a-z]{2,}",  # Email
]

JURISDICTION_KEYWORDS = {
    "nederland": ["nederland", "nl", "nederlandse", "amsterdam", "den haag"],
    "eu": ["eu", "europees", "eg", "echt", "edpb"],
    "internationaal": ["internationaal", "verdrag", "echmr", "icao"],
}

OUTDATED_TERMS = [
    "GDPR 2016",  # Moet AVG zijn in NL context
    "AI Act 2023",  # Nog niet in werking
    "Privacyrichtlijn",  # Vervangen door AVG
]


@dataclass
class AuditFinding:
    """A single audit finding."""

    error_type: LegalErrorType
    severity: Severity
    description: str
    evidence: str
    location: str


@dataclass
class AuditReport:
    """Complete audit report for a RAG engine output."""

    audit_id: str
    timestamp: str
    question: str
    answer: str
    findings: list[AuditFinding]
    severity_distribution: SeverityDistribution
    score_result: Any  # ScoringResult
    release_decision: str
    human_review_required: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "timestamp": self.timestamp,
            "question": self.question,
            "answer_length": len(self.answer),
            "findings_count": len(self.findings),
            "findings": [
                {
                    "type": f.error_type.value,
                    "severity": f.severity.value,
                    "description": f.description,
                    "evidence": f.evidence[:100],
                }
                for f in self.findings
            ],
            "severity_distribution": self.severity_distribution.to_dict(),
            "release_decision": self.release_decision,
            "human_review_required": self.human_review_required,
        }


class RAGEngineAuditor:
    """Audits RAG engine output using JLAIF taxonomy."""

    def audit(
        self,
        question: str,
        answer: str,
        expected_jurisdiction: str = "nederland",
        use_case: UseCaseProfile | None = None,
    ) -> AuditReport:
        """Audit a single RAG engine Q&A pair."""
        if use_case is None:
            use_case = UseCaseProfile(
                name="rag_engine_audit",
                autonomy_level=2,
                legal_domain="algemeen",
                user_group="advocaat",
            )

        findings: list[AuditFinding] = []

        # Check each error type
        findings.extend(self._check_factual_errors(question, answer))
        findings.extend(self._check_source_errors(question, answer))
        findings.extend(self._check_jurisdiction_errors(answer, expected_jurisdiction))
        findings.extend(self._check_temporal_errors(answer))
        findings.extend(self._check_omission_errors(question, answer))
        findings.extend(self._check_confidentiality_errors(answer))
        findings.extend(self._check_bias_errors(answer))

        # Build severity distribution
        distribution = SeverityDistribution()
        errors = []
        for finding in findings:
            distribution.add(
                LegalError(
                    error_type=finding.error_type,
                    severity=finding.severity,
                    description=finding.description,
                )
            )
            errors.append(
                LegalError(
                    error_type=finding.error_type,
                    severity=finding.severity,
                    description=finding.description,
                    source_claim=finding.evidence,
                )
            )

        # Score the system
        score_result = score_system(errors, use_case)

        # Release decision
        from .release_gate import evaluate_release

        decision = evaluate_release(errors, use_case)

        return AuditReport(
            audit_id=f"audit-{int(time.time())}",
            timestamp=datetime.now().isoformat(),
            question=question,
            answer=answer,
            findings=findings,
            severity_distribution=distribution,
            score_result=score_result,
            release_decision=decision.verdict,
            human_review_required=decision.verdict != "GO",
        )

    def _check_factual_errors(self, question: str, answer: str) -> list[AuditFinding]:
        """Check for factual inconsistencies between question and answer."""
        findings = []

        # Check if answer addresses the question topic
        question_keywords = set(question.lower().split()) - {
            "de",
            "het",
            "een",
            "van",
            "in",
            "op",
            "is",
            "wat",
            "hoe",
            "waarom",
            "voor",
            "met",
            "zijn",
            "niet",
        }
        answer_lower = answer.lower()
        matched = sum(1 for kw in question_keywords if kw in answer_lower)

        if len(question_keywords) > 3 and matched < len(question_keywords) * 0.3:
            findings.append(
                AuditFinding(
                    error_type=LegalErrorType.FACTUAL,
                    severity=Severity.S2_HERSTELBAAR,
                    description="Antwoord lijkt niet direct op de vraag te antwoorden",
                    evidence=f"Vraag: '{question[:60]}...' — matchende keywords: {matched}/{len(question_keywords)}",
                    location="rag_auditor._check_factual_errors",
                )
            )

        return findings

    def _check_source_errors(self, question: str, answer: str) -> list[AuditFinding]:
        """Check for missing or insufficient citations."""
        findings = []

        citation_count = 0
        for pattern in CITATION_PATTERNS:
            matches = re.findall(pattern, answer, re.IGNORECASE)
            citation_count += len(matches)

        # For legal answers, expect at least 1 citation per 100 words
        word_count = len(answer.split())
        expected_citations = max(1, word_count // 100)

        if citation_count < expected_citations:
            findings.append(
                AuditFinding(
                    error_type=LegalErrorType.SOURCE,
                    severity=Severity.S3_MATERIEEL,
                    description=f"Onvoldoende bronverwijzingen: {citation_count} gevonden, {expected_citations} verwacht",
                    evidence=f"Woorden: {word_count}, citaties: {citation_count}",
                    location="rag_auditor._check_source_errors",
                )
            )

        return findings

    def _check_jurisdiction_errors(
        self, answer: str, expected: str
    ) -> list[AuditFinding]:
        """Check for jurisdiction confusion."""
        findings = []
        answer_lower = answer.lower()

        expected_keywords = JURISDICTION_KEYWORDS.get(expected, [])
        other_jurisdictions = {
            k: v for k, v in JURISDICTION_KEYWORDS.items() if k != expected
        }

        # Check if answer mentions other jurisdictions inappropriately
        for juris, keywords in other_jurisdictions.items():
            for kw in keywords:
                if kw in answer_lower and not any(
                    exp_kw in answer_lower for exp_kw in expected_keywords
                ):
                    findings.append(
                        AuditFinding(
                            error_type=LegalErrorType.JURISDICTION,
                            severity=Severity.S3_MATERIEEL,
                            description=f"Mogelijke jurisdictie-verwisseling: '{juris}' genoemd zonder '{expected}' context",
                            evidence=f"Keyword '{kw}' gevonden in antwoord",
                            location="rag_auditor._check_jurisdiction_errors",
                        )
                    )
                    break

        return findings

    def _check_temporal_errors(self, answer: str) -> list[AuditFinding]:
        """Check for outdated legal references."""
        findings = []

        for term in OUTDATED_TERMS:
            if term.lower() in answer.lower():
                findings.append(
                    AuditFinding(
                        error_type=LegalErrorType.TEMPORAL,
                        severity=Severity.S3_MATERIEEL,
                        description=f"Mogelijk verouderde term: '{term}'",
                        evidence=f"Term '{term}' gevonden in antwoord",
                        location="rag_auditor._check_temporal_errors",
                    )
                )

        return findings

    def _check_omission_errors(self, question: str, answer: str) -> list[AuditFinding]:
        """Check for missed relevant aspects."""
        findings = []

        # Check for common legal aspects that should be addressed
        question_lower = question.lower()

        if "avg" in question_lower or "privacy" in question_lower:
            required_aspects = ["rechtmatigheid", "doel", "bewaartermijn"]
            missing = [a for a in required_aspects if a not in answer.lower()]
            if len(missing) == len(required_aspects):
                findings.append(
                    AuditFinding(
                        error_type=LegalErrorType.OMISSION,
                        severity=Severity.S2_HERSTELBAAR,
                        description="Privacy-vraag beantwoord zonder standaard AVG-aspecten",
                        evidence=f"Ontbrekende aspecten: {missing}",
                        location="rag_auditor._check_omission_errors",
                    )
                )

        if "ai" in question_lower and "risico" in question_lower:
            required_aspects = ["hoog risico", "conformiteit", "transparantie"]
            missing = [a for a in required_aspects if a not in answer.lower()]
            if len(missing) == len(required_aspects):
                findings.append(
                    AuditFinding(
                        error_type=LegalErrorType.OMISSION,
                        severity=Severity.S2_HERSTELBAAR,
                        description="AI-risico vraag beantwoord zonder EU AI Act-aspecten",
                        evidence=f"Ontbrekende aspecten: {missing}",
                        location="rag_auditor._check_omission_errors",
                    )
                )

        return findings

    def _check_confidentiality_errors(self, answer: str) -> list[AuditFinding]:
        """Check for PII leaks in the answer."""
        findings = []

        for pattern in PII_PATTERNS:
            matches = re.findall(pattern, answer)
            if matches:
                findings.append(
                    AuditFinding(
                        error_type=LegalErrorType.CONFIDENTIALITY,
                        severity=Severity.S5_SYSTEEMISCH,
                        description=f"PII-lek gedetecteerd: {len(matches)} matches",
                        evidence=f"Pattern '{pattern}' matched",
                        location="rag_auditor._check_confidentiality_errors",
                    )
                )

        return findings

    def _check_bias_errors(self, answer: str) -> list[AuditFinding]:
        """Check for systematic bias in the answer."""
        findings = []

        # Check for one-sided language without counter-arguments
        answer_lower = answer.lower()
        has_counter = any(
            term in answer_lower
            for term in [
                "tegenargument",
                "daarentegen",
                "echter",
                "aan de andere kant",
                "kritiek",
            ]
        )

        word_count = len(answer.split())
        if word_count > 100 and not has_counter:
            findings.append(
                AuditFinding(
                    error_type=LegalErrorType.BIAS,
                    severity=Severity.S2_HERSTELBAAR,
                    description="Lang antwoord zonder tegenargumenten of nuancering",
                    evidence=f"{word_count} woorden, geen counter-argumentatie",
                    location="rag_auditor._check_bias_errors",
                )
            )

        return findings


# ─── Singleton ─────────────────────────────────────────────────

rag_engine_auditor = RAGEngineAuditor()
