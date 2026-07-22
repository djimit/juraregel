"""Tests for Fase 1-3 JLAIF modules."""

from api.assurance.pii_redaction import pii_redaction
from api.assurance.jurisdiction import jurisdiction_classifier
from api.assurance.citation_verification import citation_verifier
from api.assurance.temporal_validity import temporal_checker
from api.assurance.bias_score import bias_calculator
from api.assurance.approval_gate import ApprovalGate


# ─── PII Redaction Tests ──────────────────────────────────────


class TestPIIRedaction:
    def test_detect_bsn(self):
        result = pii_redaction.audit_only("De patiënt heeft BSN 123456789.")
        assert result.has_pii
        assert any(d.pii_type == "BSN" for d in result.detections)

    def test_detect_email(self):
        result = pii_redaction.audit_only("Neem contact op via jan@email.com")
        assert result.has_pii
        assert any(d.pii_type == "EMAIL" for d in result.detections)

    def test_redact_bsn(self):
        result = pii_redaction.redact("BSN: 987654321")
        assert "[BSN]" in result.redacted_text
        assert "987654321" not in result.redacted_text

    def test_no_pii(self):
        result = pii_redaction.audit_only("De AVG is van toepassing op verwerkingen.")
        assert not result.has_pii

    def test_high_density_blocks(self):
        text = "BSN 111111111, BSN 222222222, BSN 333333333, BSN 444444444"
        result = pii_redaction.redact(text)
        assert result.blocked

    def test_pii_density_zero(self):
        result = pii_redaction.audit_only("Geen persoonsgegevens aanwezig.")
        assert result.pii_density == 0.0


# ─── Jurisdiction Classifier Tests ────────────────────────────


class TestJurisdictionClassifier:
    def test_nl_jurisdiction(self):
        result = jurisdiction_classifier.classify(
            "De Autoriteit Persoonsgegevens hanteert boetes conform de AVG."
        )
        assert result.primary == "NL"

    def test_eu_jurisdiction(self):
        result = jurisdiction_classifier.classify(
            "Conform Art. 9 van de EU AI Act is risicobeheer verplicht."
        )
        assert result.primary == "EU"

    def test_int_jurisdiction(self):
        result = jurisdiction_classifier.classify(
            "De OECD AI Principles zijn soft law voor internationale organisaties."
        )
        assert result.primary == "INT"

    def test_unknown_jurisdiction(self):
        result = jurisdiction_classifier.classify("Het weer is vandaag zonnig.")
        assert result.primary == "unknown"

    def test_conflict_detection(self):
        result = jurisdiction_classifier.classify(
            "De AVG is van toepassing in Nederland, maar de EU AI Act heeft voorrang."
        )
        assert len(result.conflicts) > 0

    def test_validate_consistency_ok(self):
        ok, msg = jurisdiction_classifier.validate_consistency(
            "EU", "De EU AI Act vereist risicobeheer."
        )
        assert ok

    def test_validate_consistency_fail(self):
        ok, msg = jurisdiction_classifier.validate_consistency(
            "NL", "De EU AI Act vereist risicobeheer."
        )
        assert not ok


# ─── Citation Verification Tests ──────────────────────────────


class TestCitationVerifier:
    def test_valid_citation(self):
        result = citation_verifier.verify(
            "Conform Art. 5 AVG is rechtmatigheid vereist."
        )
        assert result.total_claims > 0

    def test_missing_citation(self):
        result = citation_verifier.verify(
            "Persoonsgegevens moeten worden beschermd volgens de wet."
        )
        assert result.uncited_claims > 0

    def test_citation_rate(self):
        result = citation_verifier.verify(
            "Art. 5 AVG bepaalt dat gegevens rechtmatig worden verwerkt."
        )
        assert result.citation_rate >= 0.0


# ─── Temporal Validity Tests ──────────────────────────────────


class TestTemporalValidity:
    def test_outdated_reference(self):
        result = temporal_checker.check(
            "De Privacyrichtlijn uit 1995 is hier van toepassing."
        )
        assert result.outdated_count > 0

    def test_current_reference(self):
        result = temporal_checker.check(
            "De AVG (Verordening 2016/679) is sinds 2018 van kracht."
        )
        assert result.outdated_count == 0

    def test_expired_deadline(self):
        result = temporal_checker.check("De deadline was per 2020-01-01.")
        assert len(result.findings) > 0


# ─── Bias Score Calculator Tests ──────────────────────────────


class TestBiasScoreCalculator:
    def test_calculate_from_audits(self):
        audit_data = {
            "rag_engine": [
                {"type": "jurisdictiefout", "severity": "S3"},
                {"type": "bronfout", "severity": "S3"},
            ],
            "orchestrator": [
                {"type": "bias_ongelijke_behandeling", "severity": "S2"},
            ],
        }
        result = bias_calculator.calculate_from_audits(audit_data)
        assert result.overall_bias_rate > 0
        assert result.highest_risk_product == "orchestrator"


# ─── Approval Gate Tests ──────────────────────────────────────


class TestApprovalGate:
    def test_l4_requires_2_approvers(self):
        gate = ApprovalGate()
        req = gate.submit(4, "test", "output", 3, "S3")
        assert req.required_approvers == 2

    def test_l5_requires_3_approvers(self):
        gate = ApprovalGate()
        req = gate.submit(5, "test", "output", 3, "S3")
        assert req.required_approvers == 3

    def test_s5_auto_blocks(self):
        gate = ApprovalGate()
        req = gate.submit(4, "test", "output", 1, "S5")
        assert req.status == "rejected"

    def test_s4_auto_escalates(self):
        gate = ApprovalGate()
        req = gate.submit(3, "test", "output", 1, "S4")
        assert req.status == "escalated"

    def test_approve_flow(self):
        gate = ApprovalGate()
        req = gate.submit(4, "test", "output", 1, "S2")
        assert req.status == "pending"

        gate.approve(req.request_id, "approver_1")
        assert req.status == "pending"

        gate.approve(req.request_id, "approver_2")
        assert req.status == "approved"

    def test_reject_flow(self):
        gate = ApprovalGate()
        req = gate.submit(4, "test", "output", 1, "S2")
        gate.reject(req.request_id, "approver_1", "Te veel fouten")
        assert req.status == "rejected"
