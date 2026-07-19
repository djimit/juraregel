"""Tests voor ISO 22301 use case."""

import json
from pathlib import Path

import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from validate import validate_instance

JREM_PATH = Path(__file__).parent.parent / "jrem/exports/iso22301-2026.1.json"
SCHEMA_PATH = Path(__file__).parent.parent.parent.parent / "shared" / "jrem-schema.json"


@pytest.fixture
def jrem():
    with open(JREM_PATH) as f:
        return json.load(f)


class TestJREMValidation:
    def test_jrem_valid(self):
        assert validate_instance(str(SCHEMA_PATH), str(JREM_PATH)) == 0

    def test_domain(self, jrem):
        assert jrem["domain"] == "iso22301"

    def test_rule_count(self, jrem):
        assert len(jrem["rules"]) == 24


class TestBCMSPhases:
    """Test dat alle BCMS-fasen aanwezig zijn."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    @pytest.fixture
    def categories(self, jrem):
        return set(r["outcome"].get("category", "") for r in jrem["rules"])

    def test_context(self, categories):
        assert "bcms_context" in categories

    def test_leadership(self, categories):
        assert "bcms_leadership" in categories

    def test_analysis(self, categories):
        assert "bcms_analysis" in categories

    def test_implementation(self, categories):
        assert "bcms_implementation" in categories

    def test_testing(self, categories):
        assert "bcms_testing" in categories

    def test_evaluation(self, categories):
        assert "bcms_evaluation" in categories

    def test_improvement(self, categories):
        assert "bcms_improvement" in categories


class TestRecoveryTargets:
    """Test RTO/RPO regels."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_rto_rules(self, jrem):
        rto = [r for r in jrem["rules"] if r["ruleId"].startswith("RTO-")]
        assert len(rto) == 2

    def test_rpo_rules(self, jrem):
        rpo = [r for r in jrem["rules"] if r["ruleId"].startswith("RPO-")]
        assert len(rpo) == 1

    def test_critical_rto(self, jrem):
        critical = next(r for r in jrem["rules"] if r["ruleId"] == "RTO-001")
        assert critical["outcome"]["rto_max"] == 4


class TestBIALinks:
    """Test BIA-koppelingen."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_bia_linked(self, jrem):
        bia_linked = [r for r in jrem["rules"] if r["outcome"].get("linked_bia")]
        assert len(bia_linked) >= 2

    def test_bia_bcp_link(self, jrem):
        bia_bcp = next((r for r in jrem["rules"] if r["ruleId"] == "BCMS-8.2"), None)
        assert bia_bcp is not None
        assert "bia-biv-dpia" in bia_bcp["outcome"].get("linked_use_cases", [])
