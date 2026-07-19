"""Tests voor ISO 25010 use case."""

import json
from pathlib import Path

import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from validate import validate_instance

JREM_PATH = Path(__file__).parent.parent / "jrem/exports/iso25010-2026.1.json"
SCHEMA_PATH = Path(__file__).parent.parent.parent.parent / "shared" / "jrem-schema.json"


@pytest.fixture
def jrem():
    with open(JREM_PATH) as f:
        return json.load(f)


class TestJREMValidation:
    def test_jrem_valid(self):
        assert validate_instance(str(SCHEMA_PATH), str(JREM_PATH)) == 0

    def test_domain(self, jrem):
        assert jrem["domain"] == "iso25010"

    def test_rule_count(self, jrem):
        assert len(jrem["rules"]) == 35


class TestQualityCharacteristics:
    """Test dat alle 9 ISO 25010 kenmerken gedekt zijn."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    @pytest.fixture
    def categories(self, jrem):
        return set(r["outcome"].get("category", "") for r in jrem["rules"])

    def test_functional_suitability(self, categories):
        assert "functional_suitability" in categories

    def test_performance_efficiency(self, categories):
        assert "performance_efficiency" in categories

    def test_compatibility(self, categories):
        assert "compatibility" in categories

    def test_interaction_capability(self, categories):
        assert "interaction_capability" in categories

    def test_reliability(self, categories):
        assert "reliability" in categories

    def test_security(self, categories):
        assert "security" in categories

    def test_maintainability(self, categories):
        assert "maintainability" in categories

    def test_flexibility(self, categories):
        assert "flexibility" in categories

    def test_safety(self, categories):
        assert "safety" in categories

    def test_nine_characteristics(self, categories):
        assert len(categories) == 9


class TestSubCharacteristics:
    """Test dat sub-kenmerken correct gemapt zijn."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    @pytest.fixture
    def sub_chars(self, jrem):
        return {r["outcome"].get("sub_characteristic", "") for r in jrem["rules"]}

    def test_functional_subs(self, sub_chars):
        assert "functional_completeness" in sub_chars
        assert "functional_correctness" in sub_chars
        assert "functional_appropriateness" in sub_chars

    def test_security_subs(self, sub_chars):
        assert "confidentiality" in sub_chars
        assert "integrity" in sub_chars
        assert "authenticity" in sub_chars

    def test_interaction_subs(self, sub_chars):
        assert "learnability" in sub_chars
        assert "operability" in sub_chars
        assert "inclusivity" in sub_chars


class TestCrossLinks:
    """Test dat gekoppelde use cases correct zijn."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_wdo_link(self, jrem):
        inclusivity = next(r for r in jrem["rules"] if r["ruleId"] == "QA-4.6")
        assert "wdo" in inclusivity["outcome"].get("linked_use_cases", [])

    def test_iso27001_link(self, jrem):
        conf = next(r for r in jrem["rules"] if r["ruleId"] == "QA-6.1")
        assert "iso27001" in conf["outcome"].get("linked_use_cases", [])

    def test_bia_link(self, jrem):
        recover = next(r for r in jrem["rules"] if r["ruleId"] == "QA-5.4")
        assert "bia-biv-dpia" in recover["outcome"].get("linked_use_cases", [])
