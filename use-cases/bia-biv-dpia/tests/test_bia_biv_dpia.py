"""Tests voor BIA-BIV-DPIA use case."""

import json
from pathlib import Path

import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from validate import validate_instance

JREM_PATH = Path(__file__).parent.parent / "jrem/exports/bia-biv-dpia-2026.1.json"
SCHEMA_PATH = Path(__file__).parent.parent.parent.parent / "shared" / "jrem-schema.json"


@pytest.fixture
def jrem():
    with open(JREM_PATH) as f:
        return json.load(f)


class TestJREMValidation:
    def test_jrem_valid(self):
        assert validate_instance(str(SCHEMA_PATH), str(JREM_PATH)) == 0

    def test_rule_count(self, jrem):
        assert len(jrem["rules"]) == 32

    def test_all_have_source_refs(self, jrem):
        for rule in jrem["rules"]:
            assert len(rule["sourceRefs"]) >= 1

    def test_domain(self, jrem):
        assert jrem["domain"] == "bia-biv-dpia"


class TestBIA:
    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_bia_rules_exist(self, jrem):
        bia = [r for r in jrem["rules"] if r["ruleId"].startswith("BIA-")]
        assert len(bia) == 5

    def test_hersteltijd_catastrofaal(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "BIA-003")
        assert rule["priority"] == 400


class TestBIV:
    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_biv_rules_exist(self, jrem):
        biv = [r for r in jrem["rules"] if r["ruleId"].startswith("BIV-")]
        assert len(biv) == 6

    def test_biv_mismatch(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "BIV-005")
        assert rule["outcome"]["compliant"] is False


class TestRisico:
    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_risico_rules_exist(self, jrem):
        risico = [r for r in jrem["rules"] if r["ruleId"].startswith("RIS-")]
        assert len(risico) == 6

    def test_kritiek_risico(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "RIS-002")
        assert rule["outcome"]["compliant"] is False
        assert rule["outcome"]["prioriteit"] == "P0"


class TestDPIA:
    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_dpia_rules_exist(self, jrem):
        dpia = [r for r in jrem["rules"] if r["ruleId"].startswith("DPI-")]
        assert len(dpia) == 12

    def test_dpia_verplicht_boete(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "DPI-001")
        assert "boete" in rule["outcome"]

    def test_dpia_ai_fria(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "DPI-012")
        assert "FRIA" in rule["outcome"]["actionRequired"]

    def test_dpia_bijzondere_categorie(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "DPI-003")
        assert rule["outcome"]["dpiaVerplicht"] is True


class TestCombinatie:
    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_combi_rules_exist(self, jrem):
        combi = [r for r in jrem["rules"] if r["ruleId"].startswith("COM-")]
        assert len(combi) == 3
