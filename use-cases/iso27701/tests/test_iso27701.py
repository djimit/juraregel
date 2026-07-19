"""Tests voor ISO 27701 use case."""

import json
from pathlib import Path

import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from validate import validate_instance

JREM_PATH = Path(__file__).parent.parent / "jrem/exports/iso27701-2026.1.json"
SCHEMA_PATH = Path(__file__).parent.parent.parent.parent / "shared" / "jrem-schema.json"


@pytest.fixture
def jrem():
    with open(JREM_PATH) as f:
        return json.load(f)


class TestJREMValidation:
    def test_jrem_valid(self):
        assert validate_instance(str(SCHEMA_PATH), str(JREM_PATH)) == 0

    def test_domain(self, jrem):
        assert jrem["domain"] == "iso27701"

    def test_rule_count(self, jrem):
        assert len(jrem["rules"]) == 24


class TestCategories:
    """Test PIMS categorieën."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    @pytest.fixture
    def categories(self, jrem):
        return set(r["outcome"].get("category", "") for r in jrem["rules"])

    def test_privacy_governance(self, categories):
        assert "privacy_governance" in categories

    def test_privacy_operations(self, categories):
        assert "privacy_operations" in categories

    def test_controller_obligations(self, categories):
        assert "controller_obligations" in categories

    def test_processor_obligations(self, categories):
        assert "processor_obligations" in categories

    def test_pims_improvement(self, categories):
        assert "pims_improvement" in categories


class TestAVGLinks:
    """Test AVG-koppelingen."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_dpia_links(self, jrem):
        dpia_rules = [r for r in jrem["rules"] if r["outcome"].get("linked_dpia")]
        assert len(dpia_rules) >= 2

    def test_avg_links(self, jrem):
        avg_rules = [r for r in jrem["rules"] if r["outcome"].get("linked_avg")]
        assert len(avg_rules) >= 10

    def test_iso27001_links(self, jrem):
        linked = [r for r in jrem["rules"] if r["outcome"].get("linked_iso27001")]
        assert len(linked) >= 5


class TestPIORoles:
    """Test PII controller/processor specifieke regels."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_controller_rol(self, jrem):
        controller = [
            r for r in jrem["rules"] if r["outcome"].get("rol") == "controller"
        ]
        assert len(controller) >= 1

    def test_processor_rol(self, jrem):
        processor = [r for r in jrem["rules"] if r["outcome"].get("rol") == "processor"]
        assert len(processor) >= 3
