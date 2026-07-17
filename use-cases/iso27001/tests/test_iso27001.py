"""Tests voor ISO 27001 ISMS use case."""

import json
from pathlib import Path

import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from validate import validate_instance

JREM_PATH = Path(__file__).parent.parent / "jrem/exports/iso27001-2026.1.json"
SCHEMA_PATH = Path(__file__).parent.parent.parent.parent / "shared" / "jrem-schema.json"


@pytest.fixture
def jrem():
    with open(JREM_PATH) as f:
        return json.load(f)


class TestJREMValidation:
    def test_jrem_valid(self):
        assert validate_instance(str(SCHEMA_PATH), str(JREM_PATH)) == 0

    def test_domain(self, jrem):
        assert jrem["domain"] == "iso27001"

    def test_rule_count(self, jrem):
        assert len(jrem["rules"]) == 28


class TestISMSClausules:
    """Test dat ISMS clausules 4-10 aanwezig zijn."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_clausule_4_3(self, jrem):
        assert any(r["ruleId"] == "ISMS-4.3" for r in jrem["rules"])

    def test_clausule_5_2(self, jrem):
        assert any(r["ruleId"] == "ISMS-5.2" for r in jrem["rules"])

    def test_clausule_6_1_2(self, jrem):
        assert any(r["ruleId"] == "ISMS-6.1.2" for r in jrem["rules"])

    def test_clausule_6_1_3(self, jrem):
        assert any(r["ruleId"] == "ISMS-6.1.3" for r in jrem["rules"])

    def test_clausule_6_1_3d(self, jrem):
        assert any(r["ruleId"] == "ISMS-6.1.3d" for r in jrem["rules"])

    def test_clausule_6_2(self, jrem):
        assert any(r["ruleId"] == "ISMS-6.2" for r in jrem["rules"])

    def test_clausule_8_2(self, jrem):
        assert any(r["ruleId"] == "ISMS-8.2" for r in jrem["rules"])


class TestSOA:
    """Test Statement of Applicability controls."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_soa_controls_exist(self, jrem):
        soa = [r for r in jrem["rules"] if r["ruleId"].startswith("SOA-")]
        assert len(soa) >= 15

    def test_soa_controls_have_control_id(self, jrem):
        soa = [r for r in jrem["rules"] if r["ruleId"].startswith("SOA-")]
        for rule in soa:
            assert "control" in rule["outcome"]

    def test_soa_controls_reference_annex_a(self, jrem):
        soa = [r for r in jrem["rules"] if r["ruleId"].startswith("SOA-")]
        for rule in soa:
            assert rule["outcome"]["control"].startswith("A.")


class TestAssetRegister:
    """Test asset register regels."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_asset_register_rule(self, jrem):
        assert any(r["ruleId"] == "ASSET-001" for r in jrem["rules"])

    def test_asset_eigenaar_rule(self, jrem):
        assert any(r["ruleId"] == "ASSET-002" for r in jrem["rules"])


class TestRisicobehandeling:
    """Test risicobehandelingsregels."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_4_strategies(self, jrem):
        strategies = [r for r in jrem["rules"] if r["ruleId"].startswith("RISK-TREAT-")]
        assert len(strategies) == 4

    def test_accepteer_strategy(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "RISK-TREAT-001")
        assert rule["outcome"]["strategie"] == "accepteeren"

    def test_verminderen_strategy(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "RISK-TREAT-002")
        assert rule["outcome"]["strategie"] == "verminderen"

    def test_vermijden_strategy(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "RISK-TREAT-003")
        assert rule["outcome"]["strategie"] == "vermijden"

    def test_overdragen_strategy(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "RISK-TREAT-004")
        assert rule["outcome"]["strategie"] == "overdragen"
