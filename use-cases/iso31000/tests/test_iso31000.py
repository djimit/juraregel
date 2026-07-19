"""Tests voor ISO 31000 use case."""

import json
from pathlib import Path

import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from validate import validate_instance

JREM_PATH = Path(__file__).parent.parent / "jrem/exports/iso31000-2026.1.json"
SCHEMA_PATH = Path(__file__).parent.parent.parent.parent / "shared" / "jrem-schema.json"


@pytest.fixture
def jrem():
    with open(JREM_PATH) as f:
        return json.load(f)


class TestJREMValidation:
    def test_jrem_valid(self):
        assert validate_instance(str(SCHEMA_PATH), str(JREM_PATH)) == 0

    def test_domain(self, jrem):
        assert jrem["domain"] == "iso31000"

    def test_rule_count(self, jrem):
        assert len(jrem["rules"]) == 21


class TestRMCategories:
    """Test ISO 31000 categorieën."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    @pytest.fixture
    def categories(self, jrem):
        return set(r["outcome"].get("category", "") for r in jrem["rules"])

    def test_framework(self, categories):
        assert "rm_framework" in categories

    def test_process(self, categories):
        assert "rm_process" in categories

    def test_treatment(self, categories):
        assert "rm_treatment" in categories

    def test_improvement(self, categories):
        assert "rm_improvement" in categories

    def test_tools(self, categories):
        assert "rm_tools" in categories


class TestRiskMatrix:
    """Test risico-matrix regels."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_risk_matrix_rule(self, jrem):
        rule = next(
            (r for r in jrem["rules"] if r["ruleId"] == "RISK-MATRIX-001"), None
        )
        assert rule is not None
        assert rule["outcome"]["matrix_size"] == "5x5"

    def test_risk_appetite(self, jrem):
        rule = next(
            (r for r in jrem["rules"] if r["ruleId"] == "RISK-MATRIX-002"), None
        )
        assert rule is not None


class TestFrameworkLinks:
    """Test koppelingen naar andere frameworks."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_bia_link(self, jrem):
        linked = [
            r
            for r in jrem["rules"]
            if "bia-biv-dpia" in r["outcome"].get("linked_use_cases", [])
        ]
        assert len(linked) >= 1

    def test_iso27001_link(self, jrem):
        linked = [
            r
            for r in jrem["rules"]
            if "iso27001" in r["outcome"].get("linked_use_cases", [])
        ]
        assert len(linked) >= 1

    def test_iso22301_link(self, jrem):
        linked = [
            r
            for r in jrem["rules"]
            if "iso22301" in r["outcome"].get("linked_use_cases", [])
        ]
        assert len(linked) >= 1
