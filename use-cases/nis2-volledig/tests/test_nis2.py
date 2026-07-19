"""Tests voor NIS2 volledig."""

import json, sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from validate import validate_instance

JREM_PATH = Path(__file__).parent.parent / "jrem/exports/nis2-volledig-2026.1.json"
SCHEMA_PATH = Path(__file__).parent.parent.parent.parent / "shared/jrem-schema.json"


@pytest.fixture
def jrem():
    with open(JREM_PATH) as f:
        return json.load(f)


class TestJREM:
    def test_valid(self):
        assert validate_instance(str(SCHEMA_PATH), str(JREM_PATH)) == 0

    def test_domain(self, jrem):
        assert jrem["domain"] == "nis2-volledig"

    def test_rules(self, jrem):
        assert len(jrem["rules"]) == 24
