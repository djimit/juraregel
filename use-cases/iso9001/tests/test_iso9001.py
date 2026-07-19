"""Tests voor ISO 9001 use case."""

import json
from pathlib import Path

import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from validate import validate_instance

JREM_PATH = Path(__file__).parent.parent / "jrem/exports/iso9001-2026.1.json"
SCHEMA_PATH = Path(__file__).parent.parent.parent.parent / "shared" / "jrem-schema.json"


@pytest.fixture
def jrem():
    with open(JREM_PATH) as f:
        return json.load(f)


class TestJREMValidation:
    def test_jrem_valid(self):
        assert validate_instance(str(SCHEMA_PATH), str(JREM_PATH)) == 0

    def test_domain(self, jrem):
        assert jrem["domain"] == "iso9001"

    def test_rule_count(self, jrem):
        assert len(jrem["rules"]) == 27


class TestQMSPhases:
    """Test QMS PDCA fasen."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    @pytest.fixture
    def categories(self, jrem):
        return set(r["outcome"].get("category", "") for r in jrem["rules"])

    def test_context(self, categories):
        assert "qms_context" in categories

    def test_leadership(self, categories):
        assert "qms_leadership" in categories

    def test_planning(self, categories):
        assert "qms_planning" in categories

    def test_support(self, categories):
        assert "qms_support" in categories

    def test_operation(self, categories):
        assert "qms_operation" in categories

    def test_evaluation(self, categories):
        assert "qms_evaluation" in categories

    def test_improvement(self, categories):
        assert "qms_improvement" in categories


class TestISO31000Link:
    """Test koppeling naar ISO 31000."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_risk_link(self, jrem):
        risk = next((r for r in jrem["rules"] if r["ruleId"] == "QMS-6.1"), None)
        assert risk is not None
        assert risk["outcome"].get("linked_iso31000") == "RM-5.4"
