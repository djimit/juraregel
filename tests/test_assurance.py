"""Unit tests for JuraRegel Legal AI Assurance Framework."""

import pytest

from api.assurance.error_taxonomy import (
    LegalError,
    LegalErrorType,
    Severity,
    SeverityDistribution,
)
from api.assurance.release_gate import ReleaseDecision, evaluate_release
from api.assurance.severity_scorer import (
    ScoringResult,
    UseCaseProfile,
    score_system,
)
from shared.gate.lineage import (
    EvidenceLineage,
    HumanEdit,
    RetrievalRecord,
    SourceRef,
)


def test_nine_error_types():
    assert len(LegalErrorType) == 9


def test_error_type_values():
    names = {e.value for e in LegalErrorType}
    assert "fout" in names
    assert "bronfout" in names
    assert "interpretatiefout" in names
    assert "jurisdictiefout" in names
    assert "temporaliteitsfout" in names
    assert "procedurefout" in names
    assert "omissiefout" in names
    assert "bias_ongelijke_behandeling" in names
    assert "vertrouwelijkheidsincident" in names


def test_five_severities():
    assert len(Severity) == 5


def test_severity_weights():
    assert Severity.S1_COSMETISCH.weight == 1.0
    assert Severity.S2_HERSTELBAAR.weight == 2.0
    assert Severity.S3_MATERIEEL.weight == 4.0
    assert Severity.S4_RECHTSVERLIES.weight == 8.0
    assert Severity.S5_SYSTEEMISCH.weight == 16.0


def test_s5_is_16x_s1():
    assert Severity.S5_SYSTEEMISCH.weight == 16 * Severity.S1_COSMETISCH.weight


def test_blocks_release():
    assert Severity.S4_RECHTSVERLIES.blocks_release is True
    assert Severity.S5_SYSTEEMISCH.blocks_release is True
    assert Severity.S1_COSMETISCH.blocks_release is False
    assert Severity.S2_HERSTELBAAR.blocks_release is False
    assert Severity.S3_MATERIEEL.blocks_release is False


def test_risk_score_detectable():
    err = LegalError(
        error_type=LegalErrorType.BIAS,
        severity=Severity.S5_SYSTEEMISCH,
        description="t",
        detectable=True,
    )
    assert err.risk_score == 0.0


def test_risk_score_undetectable():
    err = LegalError(
        error_type=LegalErrorType.BIAS,
        severity=Severity.S5_SYSTEEMISCH,
        description="t",
        detectable=False,
    )
    assert err.risk_score == pytest.approx(12.8)


def test_risk_score_s1_undetectable():
    err = LegalError(
        error_type=LegalErrorType.FACTUAL,
        severity=Severity.S1_COSMETISCH,
        description="c",
        detectable=False,
    )
    assert err.risk_score == pytest.approx(0.8)


def test_distribution_add():
    dist = SeverityDistribution()
    dist.add(LegalError(LegalErrorType.FACTUAL, Severity.S3_MATERIEEL, "t"))
    assert dist.counts[Severity.S3_MATERIEEL] == 1


def test_distribution_weighted_score():
    dist = SeverityDistribution()
    dist.add(LegalError(LegalErrorType.FACTUAL, Severity.S1_COSMETISCH, ""))
    dist.add(LegalError(LegalErrorType.FACTUAL, Severity.S5_SYSTEEMISCH, ""))
    assert dist.weighted_score == pytest.approx(17.0)


def test_has_blocking_errors_true():
    dist = SeverityDistribution()
    dist.add(LegalError(LegalErrorType.BIAS, Severity.S5_SYSTEEMISCH, ""))
    assert dist.has_blocking_errors is True


def test_has_blocking_errors_false():
    dist = SeverityDistribution()
    dist.add(LegalError(LegalErrorType.FACTUAL, Severity.S1_COSMETISCH, ""))
    assert dist.has_blocking_errors is False


def test_non_blocking_ratio_no_errors():
    dist = SeverityDistribution()
    assert dist.non_blocking_ratio == 1.0


def test_non_blocking_ratio_all_blocking():
    dist = SeverityDistribution()
    dist.add(LegalError(LegalErrorType.BIAS, Severity.S5_SYSTEEMISCH, ""))
    assert dist.non_blocking_ratio == pytest.approx(0.0)


def test_non_blocking_ratio_mixed():
    dist = SeverityDistribution()
    dist.add(LegalError(LegalErrorType.FACTUAL, Severity.S1_COSMETISCH, ""))
    dist.add(LegalError(LegalErrorType.BIAS, Severity.S5_SYSTEEMISCH, ""))
    assert dist.non_blocking_ratio == pytest.approx(1.0 / 17.0)


def test_score_system_no_errors():
    uc = UseCaseProfile("test", 1, "criminal", "rechter")
    result = score_system([], uc)
    assert isinstance(result, ScoringResult)
    assert result.distribution.total_errors == 0


def test_score_system_fields():
    uc = UseCaseProfile("test", 3, "civil", "advocaat", affected_parties=10)
    errors = [LegalError(LegalErrorType.FACTUAL, Severity.S2_HERSTELBAAR, "t")]
    result = score_system(errors, uc)
    assert result.use_case == uc
    assert result.benefit_score > 0
    assert result.risk_score > 0


def test_high_autonomy_stricter():
    uc_low = UseCaseProfile("low", 1, "civil", "burger")
    uc_high = UseCaseProfile("high", 5, "civil", "burger")
    errors = [LegalError(LegalErrorType.FACTUAL, Severity.S2_HERSTELBAAR, "t")]
    r_low = score_system(errors, uc_low)
    r_high = score_system(errors, uc_high)
    assert r_low.ratio == r_high.ratio
    assert r_low.acceptable or not r_high.acceptable


def test_blocking_errors_unacceptable():
    uc = UseCaseProfile("test", 1, "civil", "burger")
    errors = [LegalError(LegalErrorType.BIAS, Severity.S5_SYSTEEMISCH, "bias")]
    result = score_system(errors, uc)
    assert result.acceptable is False
    assert "S5" in result.blocking_severities


def test_scoring_result_to_dict():
    uc = UseCaseProfile("test", 2, "admin", "ambtenaar")
    result = score_system([], uc)
    d = result.to_dict()
    assert "use_case" in d
    assert "ratio" in d


def test_release_go_no_errors():
    uc = UseCaseProfile("test", 1, "civil", "burger")
    decision = evaluate_release([], uc)
    assert isinstance(decision, ReleaseDecision)
    assert decision.verdict == "GO"
    assert decision.approved is True


def test_release_go_with_s1_errors():
    uc = UseCaseProfile("test", 1, "civil", "burger", expected_value=1.0)
    errors = [LegalError(LegalErrorType.FACTUAL, Severity.S1_COSMETISCH, "c")]
    decision = evaluate_release(
        errors, uc, min_detectability=0.8, min_recoverability=0.8
    )
    assert decision.verdict == "GO"


def test_release_nogo_s5():
    uc = UseCaseProfile("test", 1, "civil", "burger")
    errors = [LegalError(LegalErrorType.BIAS, Severity.S5_SYSTEEMISCH, "bias")]
    decision = evaluate_release(errors, uc)
    assert decision.verdict == "NO-GO"
    assert decision.approved is False


def test_release_nogo_s4():
    uc = UseCaseProfile("test", 1, "civil", "burger")
    errors = [LegalError(LegalErrorType.JURISDICTION, Severity.S4_RECHTSVERLIES, "j")]
    decision = evaluate_release(errors, uc)
    assert decision.verdict == "NO-GO"


def test_release_nogo_s3_formula():
    """S3 at L1 is NO-GO because ratio = d*r/4 max 0.25 < 0.5 threshold."""
    uc = UseCaseProfile("test", 1, "civil", "burger", expected_value=1.0)
    errors = [LegalError(LegalErrorType.FACTUAL, Severity.S3_MATERIEEL, "m")]
    decision = evaluate_release(
        errors, uc, min_detectability=1.0, min_recoverability=1.0
    )
    assert decision.verdict == "NO-GO"


def test_release_conditional_unreachable_at_l1():
    """CONDITIONAL requires acceptable=True AND S3 present — unreachable at L1 with this formula."""
    uc = UseCaseProfile("test", 1, "civil", "burger", expected_value=1.0)
    errors = [LegalError(LegalErrorType.FACTUAL, Severity.S3_MATERIEEL, "m")]
    decision = evaluate_release(
        errors, uc, min_detectability=0.99, min_recoverability=0.99
    )
    # Even with d=0.99 r=0.99, ratio = 0.9801/4 = 0.245 < 0.5 → NO-GO
    assert decision.verdict == "NO-GO"


def test_source_ref():
    ref = SourceRef(document_id="doc1", source_hash="abc", authority_rank=1)
    assert ref.document_id == "doc1"
    assert ref.authority_rank == 1


def test_retrieval_record():
    rec = RetrievalRecord(query="q", retrieval_model="m")
    assert rec.query == "q"
    assert rec.results == []


def test_human_edit():
    edit = HumanEdit(actor="j", role="r", action="approved")
    assert edit.actor == "j"
    assert edit.action == "approved"


def test_lineage_compute_hash():
    lin = EvidenceLineage(
        model_version="v1",
        prompt_template_id="t1",
        sources=[SourceRef(document_id="d1", source_hash="h1")],
        generated_answer="a",
    )
    h = lin.compute_hash()
    assert len(h) == 64
    assert lin.lineage_hash == h


def test_lineage_hash_deterministic():
    lin = EvidenceLineage(
        model_version="v1",
        generated_answer="a",
        sources=[SourceRef(document_id="d1", source_hash="h1")],
    )
    assert lin.compute_hash() == lin.compute_hash()


def test_lineage_is_complete_true():
    lin = EvidenceLineage(
        model_version="v1",
        generated_answer="a",
        sources=[SourceRef(document_id="d1")],
        human_review_completed=True,
        final_answer="f",
    )
    lin.compute_hash()
    assert lin.is_complete is True


def test_lineage_is_complete_no_hash():
    lin = EvidenceLineage(
        model_version="v1",
        generated_answer="a",
        sources=[SourceRef(document_id="d1")],
        human_review_completed=True,
        final_answer="f",
    )
    assert lin.is_complete is False


def test_lineage_is_complete_no_sources():
    lin = EvidenceLineage(
        model_version="v1",
        generated_answer="a",
        human_review_completed=True,
        final_answer="f",
    )
    lin.compute_hash()
    assert lin.is_complete is False


def test_lineage_is_traceable_true():
    lin = EvidenceLineage(
        sources=[
            SourceRef(document_id="d1", source_hash="h1"),
            SourceRef(document_id="d2", source_hash="h2"),
        ]
    )
    assert lin.is_traceable is True


def test_lineage_is_traceable_false():
    lin = EvidenceLineage(sources=[SourceRef(document_id="d1", source_hash="")])
    assert lin.is_traceable is False


def test_lineage_to_dict():
    lin = EvidenceLineage(
        model_version="v1",
        prompt_template_id="t1",
        generated_answer="a",
        sources=[SourceRef(document_id="d1", source_hash="h1")],
        human_edits=[HumanEdit(actor="a", role="r", action="approved")],
    )
    d = lin.to_dict()
    assert d["model_version"] == "v1"
    assert isinstance(d["sources"], list)
    assert isinstance(d["human_edits"], list)
    assert "is_complete" in d
    assert "is_traceable" in d
