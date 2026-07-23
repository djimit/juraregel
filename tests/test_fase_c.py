"""Tests for Fase C modules: formal severity, causality, longitudinal, cross-jurisdiction."""

from api.assurance.formal_severity import (
    FormalSeverityModel,
)
from api.assurance.causality_network import causality_network
from api.assurance.longitudinal import longitudinal_eval, AuditSnapshot
from api.assurance.cross_jurisdiction import cross_jurisdiction, JURISDICTION_PROFILES


# ─── Formal Severity Tests ────────────────────────────────────


class TestFormalSeverity:
    def test_utility_function(self):
        model = FormalSeverityModel(risk_aversion=1.0)
        u = model.utility(1.0)
        assert 0 < u < 1

    def test_utility_increases_with_weight(self):
        model = FormalSeverityModel()
        u1 = model.utility(1.0)
        u5 = model.utility(16.0)
        assert u5 > u1

    def test_combined_weight(self):
        model = FormalSeverityModel()
        combined = model.combined_weight(["S1", "S1", "S1"])
        single = model.combined_weight(["S5"])
        # 3x S1 should be less than 1x S5
        assert combined < single

    def test_prospect_adjusted_weight(self):
        model = FormalSeverityModel()
        s1_adj = model.prospect_adjusted_weight("S1")
        s5_adj = model.prospect_adjusted_weight("S5")
        assert s5_adj > s1_adj

    def test_expected_utility_loss(self):
        model = FormalSeverityModel()
        loss = model.expected_utility_loss(["S3", "S4"], [0.5, 0.3])
        assert 0 < loss < 1

    def test_compare_systems(self):
        model = FormalSeverityModel()
        result = model.compare_systems(["S1", "S2"], ["S4"])
        assert result["preferred"] == "A"  # S1+S2 is better than S4

    def test_explain_weighting(self):
        model = FormalSeverityModel()
        explanation = model.explain_weighting("S5")
        assert explanation["level"] == "S5"
        assert "prospect" in explanation["explanation"].lower()


# ─── Causality Network Tests ──────────────────────────────────


class TestCausalityNetwork:
    def test_get_root_causes(self):
        roots = causality_network.get_root_causes("procedurefout")
        assert len(roots) > 0

    def test_get_cascade_effects(self):
        effects = causality_network.get_cascade_effects("bias_ongelijke_behandeling")
        assert len(effects) > 0

    def test_compute_cascade_probability(self):
        prob = causality_network.compute_cascade_probability(
            "bronfout", "feitelijke_fout"
        )
        assert 0 < prob <= 1

    def test_find_critical_path(self):
        paths = causality_network.find_critical_path(
            "bias_ongelijke_behandeling", "procedurefout"
        )
        assert isinstance(paths, list)

    def test_risk_ranking(self):
        ranking = causality_network.get_risk_ranking()
        assert len(ranking) > 0
        # Bias should be high in ranking (no causes, many effects)
        bias_entry = next(
            (r for r in ranking if r["error_type"] == "bias_ongelijke_behandeling"),
            None,
        )
        assert bias_entry is not None


# ─── Longitudinal Evaluation Tests ────────────────────────────


class TestLongitudinalEvaluation:
    def test_add_snapshot(self):
        snapshot = AuditSnapshot(
            timestamp="2026-07-01T00:00:00",
            product_name="test-product",
            total_findings=5,
            severity_distribution={"S2": 3, "S3": 2},
            release_decision="NO-GO",
            score=60.0,
        )
        longitudinal_eval.add_snapshot(snapshot)
        assert len(longitudinal_eval.get_snapshots("test-product")) == 1

    def test_analyze_trend_improving(self):
        # Add improving snapshots
        for i, score in enumerate([50, 55, 60, 65, 70]):
            longitudinal_eval.add_snapshot(
                AuditSnapshot(
                    timestamp=f"2026-0{i + 1}-01T00:00:00",
                    product_name="improving-product",
                    total_findings=10 - i,
                    severity_distribution={"S2": 5},
                    release_decision="NO-GO",
                    score=float(score),
                )
            )
        trend = longitudinal_eval.analyze_trend("improving-product")
        assert trend.trend == "improving"
        assert trend.slope > 0

    def test_detect_regression(self):
        # Add declining snapshots
        for i, score in enumerate([80, 75, 70, 60, 50]):
            longitudinal_eval.add_snapshot(
                AuditSnapshot(
                    timestamp=f"2026-0{i + 1}-01T00:00:00",
                    product_name="declining-product",
                    total_findings=5 + i,
                    severity_distribution={"S3": 3},
                    release_decision="NO-GO",
                    score=float(score),
                )
            )
        regression = longitudinal_eval.detect_regression("declining-product")
        assert regression["detected"]

    def test_generate_report(self):
        longitudinal_eval.add_snapshot(
            AuditSnapshot(
                timestamp="2026-07-01T00:00:00",
                product_name="report-product",
                total_findings=3,
                severity_distribution={"S2": 3},
                release_decision="GO",
                score=85.0,
            )
        )
        report = longitudinal_eval.generate_report("report-product")
        assert "trend" in report
        assert "recommendation" in report


# ─── Cross-Jurisdiction Tests ─────────────────────────────────


class TestCrossJurisdiction:
    def test_get_jurisdiction(self):
        nl = cross_jurisdiction.get_jurisdiction("NL")
        assert nl is not None
        assert nl.name == "Nederland"

    def test_compare_frameworks(self):
        comparisons = cross_jurisdiction.compare_frameworks()
        assert len(comparisons) > 0

    def test_compare_two(self):
        result = cross_jurisdiction.compare_two("NL", "DE")
        assert "shared_frameworks" in result
        # Both have civil law system
        assert result["legal_system_a"] == "civil_law"
        assert result["legal_system_b"] == "civil_law"

    def test_find_gaps(self):
        gaps = cross_jurisdiction.find_gaps()
        assert len(gaps) > 0

    def test_all_jurisdictions_present(self):
        assert "NL" in JURISDICTION_PROFILES
        assert "EU" in JURISDICTION_PROFILES
        assert "INT" in JURISDICTION_PROFILES
        assert "UK" in JURISDICTION_PROFILES
        assert "US" in JURISDICTION_PROFILES
        assert "DE" in JURISDICTION_PROFILES
