"""Tests voor DPIA Generator use case."""

import json
from pathlib import Path

import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from validate import validate_instance

JREM_PATH = Path(__file__).parent.parent / "jrem/exports/dpia-generator-2026.1.json"
SCHEMA_PATH = Path(__file__).parent.parent.parent.parent / "shared" / "jrem-schema.json"


@pytest.fixture
def jrem():
    with open(JREM_PATH) as f:
        return json.load(f)


class TestJREMValidation:
    def test_jrem_valid(self):
        assert validate_instance(str(SCHEMA_PATH), str(JREM_PATH)) == 0

    def test_rule_count(self, jrem):
        assert len(jrem["rules"]) == 51

    def test_domain(self, jrem):
        assert jrem["domain"] == "dpia-generator"

    def test_all_have_source_refs(self, jrem):
        for rule in jrem["rules"]:
            assert len(rule["sourceRefs"]) >= 1


class TestEDPBSecties:
    """Test dat alle 7 EDPB-secties gedekt zijn."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    @pytest.fixture
    def secties(self, jrem):
        return set(r["outcome"].get("sectie", "") for r in jrem["rules"])

    def test_sectie_0(self, secties):
        assert "0_technical_sheet" in secties

    def test_sectie_1(self, secties):
        assert "1_context" in secties

    def test_sectie_2(self, secties):
        assert "2_essentieel" in secties

    def test_sectie_3(self, secties):
        assert "3_noodzaak" in secties

    def test_sectie_4(self, secties):
        assert "4_risico" in secties

    def test_sectie_5(self, secties):
        assert "5_maatregelen" in secties

    def test_sectie_6(self, secties):
        assert "6_conclusie" in secties


class TestAPCategories:
    """Test dat alle 12 AP-categorieen gedekt zijn."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_ap_categories_exist(self, jrem):
        ap_rules = [
            r
            for r in jrem["rules"]
            if r["ruleId"].startswith("DPG-07") or r["ruleId"].startswith("DPG-08")
        ]
        assert len(ap_rules) == 12

    def test_ap_categories_have_dpia_verplicht(self, jrem):
        ap_rules = [r for r in jrem["rules"] if r["ruleId"].startswith("DPG-07")]
        for rule in ap_rules:
            assert rule["outcome"].get("dpiaVerplicht") is True


class TestKCBRParts:
    """Test dat KCBR 4-delen structuur gedekt is."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_kcbr_deel_a(self, jrem):
        """Deel A: Beschrijving feitelijke situatie → sectie 1_context."""
        context_rules = [
            r for r in jrem["rules"] if r["outcome"].get("sectie") == "1_context"
        ]
        assert len(context_rules) >= 8

    def test_kcbr_deel_b(self, jrem):
        """Deel B: Noodzaak/proportionaliteit → sectie 3_noodzaak."""
        noodzaak_rules = [
            r for r in jrem["rules"] if r["outcome"].get("sectie") == "3_noodzaak"
        ]
        assert len(noodzaak_rules) >= 4

    def test_kcbr_deel_c(self, jrem):
        """Deel C: Risico-analyse → sectie 4_risico."""
        risico_rules = [
            r for r in jrem["rules"] if r["outcome"].get("sectie") == "4_risico"
        ]
        assert len(risico_rules) >= 5

    def test_kcbr_deel_d(self, jrem):
        """Deel D: Maatregelen → sectie 5_maatregelen."""
        maatregelen_rules = [
            r for r in jrem["rules"] if r["outcome"].get("sectie") == "5_maatregelen"
        ]
        assert len(maatregelen_rules) >= 6


class TestVerplichteRegels:
    """Test dat AVG Art. 35 lid 7a-f elementen aanwezig zijn."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_art_35_7a(self, jrem):
        """Beschrijving van de verwerking."""
        assert any("7a" in r["outcome"].get("artikel", "") for r in jrem["rules"])

    def test_art_35_7b(self, jrem):
        """Beoordeling van de noodzaak en proportionaliteit."""
        assert any("3" in r["outcome"].get("sectie", "") for r in jrem["rules"])

    def test_art_35_7d(self, jrem):
        """Beoordeling van de risico's."""
        assert any("7d" in r["outcome"].get("artikel", "") for r in jrem["rules"])

    def test_art_35_7e(self, jrem):
        """Voorgenomen maatregelen."""
        assert any("7e" in r["outcome"].get("artikel", "") for r in jrem["rules"])
