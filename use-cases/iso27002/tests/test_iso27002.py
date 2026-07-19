"""Tests voor ISO 27002 use case."""

import json
from pathlib import Path

import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from validate import validate_instance

JREM_PATH = Path(__file__).parent.parent / "jrem/exports/iso27002-2026.1.json"
SCHEMA_PATH = Path(__file__).parent.parent.parent.parent / "shared" / "jrem-schema.json"


@pytest.fixture
def jrem():
    with open(JREM_PATH) as f:
        return json.load(f)


class TestJREMValidation:
    def test_jrem_valid(self):
        assert validate_instance(str(SCHEMA_PATH), str(JREM_PATH)) == 0

    def test_domain(self, jrem):
        assert jrem["domain"] == "iso27002"

    def test_rule_count(self, jrem):
        assert len(jrem["rules"]) == 34


class TestCategories:
    """Test dat alle 4 ISO 27002 categorieën aanwezig zijn."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    @pytest.fixture
    def categories(self, jrem):
        return set(r["outcome"].get("category", "") for r in jrem["rules"])

    def test_organizational(self, categories):
        assert "organizational" in categories

    def test_people(self, categories):
        assert "people" in categories

    def test_physical(self, categories):
        assert "physical" in categories

    def test_technological(self, categories):
        assert "technological" in categories


class TestBIO2Mapping:
    """Test BIO2 → ISO 27002 mapping."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_bio2_links_present(self, jrem):
        linked = [r for r in jrem["rules"] if r["outcome"].get("linked_bio2")]
        assert len(linked) >= 20

    def test_all_have_source_refs(self, jrem):
        for rule in jrem["rules"]:
            assert len(rule["sourceRefs"]) >= 1

    def test_high_priority_security_controls(self, jrem):
        """Security controls should be high priority."""
        high_prio = [r for r in jrem["rules"] if r["priority"] >= 400]
        assert len(high_prio) >= 10

    def test_dpia_link(self, jrem):
        """PII control should link to DPIA."""
        pii = next((r for r in jrem["rules"] if r["ruleId"] == "27002-A.5.34"), None)
        assert pii is not None
        assert pii["outcome"].get("linked_dpia") is True
