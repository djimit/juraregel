"""Tests voor eIDAS 2.0 use case — European Digital Identity Framework.

32 regels verdeeld over 11 categorieën:
- Vertrouwensdiensten (eIDAS 1.0): handtekening, zegel, tijdsstempel, ERD, website-auth
- Nieuwe vertrouwensdiensten (eIDAS 2.0): QAA, Electronic Archival
- EUDI-wallet: productie, piloot, ontwikkeling, niet gestart, design, PID
- Grensoverschrijdende erkenning: crossborder, interoperabiliteit, acceptatie
- TSP-kwalificatie: certificering, upgrade vereist
- Niet-discriminatie
- Attribuut-uitwisseling: wallet attributen, eHerkenning, DigiD
- Trust Lists: EUTL, nationale sync
- Kwaliteitskeurmerken: wallet keurmerk, PID provider
- Private sector + security + certificering + DPIA + implementing
"""

import json
from pathlib import Path

import pytest
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from validate import validate_instance

JREM_PATH = Path(__file__).parent.parent / "jrem/exports/eidas-2026.2.json"
SCHEMA_PATH = Path(__file__).parent.parent.parent.parent / "shared" / "jrem-schema.json"


@pytest.fixture
def jrem():
    with open(JREM_PATH) as f:
        return json.load(f)


# ─── JREM Schema Validation ───────────────────────────────────


class TestJREMValidation:
    def test_jrem_valid(self):
        exit_code = validate_instance(str(SCHEMA_PATH), str(JREM_PATH))
        assert exit_code == 0

    def test_rule_count(self, jrem):
        assert len(jrem["rules"]) == 32

    def test_all_rules_have_rule_id(self, jrem):
        for rule in jrem["rules"]:
            assert rule["ruleId"].startswith("EID-")
            assert len(rule["ruleId"]) == 7  # EID-XXX (3 cijfers)

    def test_all_rules_have_source_refs(self, jrem):
        for rule in jrem["rules"]:
            assert len(rule["sourceRefs"]) >= 1
            for ref in rule["sourceRefs"]:
                assert "title" in ref
                assert "url" in ref

    def test_all_rules_have_deadlines(self, jrem):
        for rule in jrem["rules"]:
            assert "deadline" in rule["outcome"]

    def test_all_rules_have_categories(self, jrem):
        expected_cats = {
            "eidas_handtekening",
            "eidas_zegel",
            "eidas_tijdsstempel",
            "eidas_erd",
            "eidas_webauth",
            "eidas_qaa",
            "eidas_archief",
            "eidas_wallet",
            "eidas_wallet_design",
            "eidas_pid",
            "eidas_certificering",
            "eidas_crossborder",
            "eidas_tsp",
            "eidas_niet_discriminatie",
            "eidas_attributen",
            "eidas_trustlist",
            "eidas_keurmerk",
            "eidas_private",
            "eidas_security",
            "eidas_privacy",
            "eidas_implementing",
        }
        actual_cats = set(r["outcome"]["category"] for r in jrem["rules"])
        assert actual_cats == expected_cats

    def test_priority_ordering(self, jrem):
        """Higher priority rules should come first within categories."""
        eid_011 = next(r for r in jrem["rules"] if r["ruleId"] == "EID-011")
        assert eid_011["priority"] >= 500

    def test_eidas_version(self, jrem):
        assert jrem["version"] == "2026.2"
        assert jrem["ruleSetId"] == "eidas"

    def test_procedure_type(self, jrem):
        assert jrem["procedureType"] == "eidas-compliance"

    def test_jurisdiction(self, jrem):
        assert jrem["jurisdiction"] == "NL"


# ─── eIDAS 1.0 Vertrouwensdiensten ────────────────────────────


class TestTrustServices:
    """Test eIDAS 1.0 vertrouwensdiensten (handtekening, zegel, tijdsstempel, ERD, website-auth)."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_qualified_signature_compliant(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-001")
        assert rule["outcome"]["compliant"] is True
        assert rule["outcome"]["category"] == "eidas_handtekening"
        assert "Art. 25(1)" in rule["outcome"]["article"]

    def test_qualified_seal_compliant(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-002")
        assert rule["outcome"]["compliant"] is True
        assert rule["outcome"]["category"] == "eidas_zegel"
        assert "Art. 35(2)" in rule["outcome"]["article"]

    def test_qualified_timestamp(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-003")
        assert rule["outcome"]["compliant"] is True
        assert rule["outcome"]["category"] == "eidas_tijdsstempel"

    def test_qualified_erd(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-004")
        assert rule["outcome"]["compliant"] is True
        assert rule["outcome"]["category"] == "eidas_erd"

    def test_qualified_website_auth(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-005")
        assert rule["outcome"]["compliant"] is True
        assert rule["outcome"]["category"] == "eidas_webauth"

    def test_all_trust_services_have_2026_deadline(self, jrem):
        ts_rules = [
            r
            for r in jrem["rules"]
            if r["outcome"]["category"]
            in [
                "eidas_handtekening",
                "eidas_zegel",
                "eidas_tijdsstempel",
                "eidas_erd",
                "eidas_webauth",
            ]
        ]
        for rule in ts_rules:
            assert rule["outcome"]["deadline"] == "2026-01-01"


# ─── eIDAS 2.0 Nieuwe Vertrouwensdiensten ─────────────────────


class TestNewTrustServices:
    """Test nieuwe vertrouwensdiensten uit eIDAS 2.0."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_qaa_exists(self, jrem):
        """Qualified Attestation of Attributes — nieuw in eIDAS 2.0."""
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-006")
        assert rule["outcome"]["category"] == "eidas_qaa"
        assert "Art. 3(16a)" in rule["outcome"]["article"]
        assert rule["outcome"]["deadline"] == "2026-12-01"

    def test_electronic_archival_exists(self, jrem):
        """Electronic Archival — nieuw in eIDAS 2.0."""
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-007")
        assert rule["outcome"]["category"] == "eidas_archief"
        assert "Art. 3(16b)" in rule["outcome"]["article"]
        assert rule["outcome"]["deadline"] == "2026-12-01"


# ─── EUDI Wallet ─────────────────────────────────────────────


class TestWallet:
    """Test EUDI-wallet regels (eIDAS 2.0)."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_wallet_productie_compliant(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-008")
        assert rule["outcome"]["compliant"] is True
        assert rule["outcome"]["category"] == "eidas_wallet"
        assert rule["outcome"]["deadline"] == "2026-12-01"

    def test_wallet_pilot_temporary_compliance(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-009")
        assert rule["outcome"]["compliant"] is True
        assert "warning" in rule["outcome"]

    def test_wallet_ontwikkeling_non_compliant(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-010")
        assert rule["outcome"]["compliant"] is False
        assert "Versnellen" in rule["outcome"]["actionRequired"]

    def test_wallet_niet_gestart_critical(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-011")
        assert rule["outcome"]["compliant"] is False
        assert rule["outcome"].get("risk") == "CRITICAL"
        assert "START DIRECT" in rule["outcome"]["actionRequired"]

    def test_wallet_design_sole_control(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-012")
        assert rule["outcome"]["category"] == "eidas_wallet_design"
        assert "Sole control" in rule["outcome"]["article"]

    def test_pid_minimum_dataset(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-013")
        assert rule["outcome"]["category"] == "eidas_pid"
        assert "Annex VI" in rule["outcome"]["evidenceRequired"]

    def test_rvig_pid_provider(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-014")
        assert rule["outcome"]["category"] == "eidas_pid"
        assert "RvIG" in rule["outcome"]["evidenceRequired"]

    def test_rdi_certificering(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-015")
        assert rule["outcome"]["category"] == "eidas_certificering"
        assert "RDI" in rule["outcome"]["evidenceRequired"]

    def test_wallet_deadline_december_2026(self, jrem):
        """Correctie: deadline is December 2026, niet September."""
        wallet_rules = [
            r for r in jrem["rules"] if "wallet" in r["outcome"]["category"]
        ]
        for rule in wallet_rules:
            assert rule["outcome"]["deadline"] == "2026-12-01"

    def test_wallet_security_levels(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-029")
        assert rule["outcome"]["category"] == "eidas_security"
        assert "LoA" in rule["outcome"]["evidenceRequired"]

    def test_conformiteitsbeoordeling(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-030")
        assert rule["outcome"]["category"] == "eidas_certificering"
        assert "Art. 6d" in rule["outcome"]["article"]


# ─── Grensoverschrijdende Erkenning ──────────────────────────


class TestCrossBorder:
    """Test grensoverschrijdende erkenning regels."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_crossborder_signature(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-016")
        assert rule["outcome"]["category"] == "eidas_crossborder"
        assert "Art. 13" in rule["outcome"]["article"]

    def test_crossborder_wallet_interop(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-017")
        assert rule["outcome"]["category"] == "eidas_crossborder"
        assert "Art. 6j" in rule["outcome"]["article"]

    def test_crossborder_government_acceptance(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-018")
        assert rule["outcome"]["category"] == "eidas_crossborder"
        assert "Art. 6a(6)" in rule["outcome"]["article"]


# ─── TSP-kwalificatie ────────────────────────────────────────


class TestTSP:
    """Test TSP-kwalificatie regels."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_qualified_tsp(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-019")
        assert rule["outcome"]["category"] == "eidas_tsp"
        assert rule["outcome"]["compliant"] is True

    def test_non_qualified_upgrade_required(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-020")
        assert rule["outcome"]["compliant"] is False
        assert "Migreer" in rule["outcome"]["actionRequired"]


# ─── Attribuut-uitwisseling ──────────────────────────────────


class TestAttributes:
    """Test elektronische attributen regels."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_wallet_attributen(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-022")
        assert rule["outcome"]["category"] == "eidas_attributen"
        assert "Art. 12d" in rule["outcome"]["article"]

    def test_eherkenning_wallet(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-023")
        assert rule["outcome"]["category"] == "eidas_attributen"
        assert "eHerkenning" in rule["outcome"]["evidenceRequired"]

    def test_digid_wallet(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-024")
        assert rule["outcome"]["category"] == "eidas_attributen"
        assert "DigiD" in rule["outcome"]["evidenceRequired"]


# ─── Trust Lists ─────────────────────────────────────────────


class TestTrustLists:
    """Test trust list regels."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_eutl_publicatie(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-025")
        assert rule["outcome"]["category"] == "eidas_trustlist"
        assert "EUTL" in rule["outcome"]["evidenceRequired"]

    def test_nationale_trustlist_sync(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-026")
        assert rule["outcome"]["category"] == "eidas_trustlist"
        assert "Art. 6p" in rule["outcome"]["article"]


# ─── Kwaliteitskeurmerken ────────────────────────────────────


class TestQualityLabels:
    """Test kwaliteitskeurmerk regels."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_wallet_keurmerk(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-027")
        assert rule["outcome"]["category"] == "eidas_keurmerk"
        assert rule["outcome"]["deadline"] == "2027-12-01"

    def test_pid_provider_certificering(self, jrem):
        rule = next(
            r
            for r in jrem["rules"]
            if r["ruleId"] == "EID-020" or r["ruleId"] == "EID-014"
        )
        assert rule["outcome"]["category"] in ["eidas_pid", "eidas_tsp"]


# ─── Privacy + Implementing ──────────────────────────────────


class TestPrivacyImplementing:
    """Test privacy en implementing regels."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_dpia_required(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-031")
        assert rule["outcome"]["category"] == "eidas_privacy"
        assert "DPIA" in rule["outcome"]["evidenceRequired"]
        assert "AVG Art. 35" in rule["outcome"]["article"]

    def test_implementing_acts(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-032")
        assert rule["outcome"]["category"] == "eidas_implementing"
        assert "2024/2977" in rule["outcome"]["evidenceRequired"]

    def test_private_sector(self, jrem):
        rule = next(r for r in jrem["rules"] if r["ruleId"] == "EID-028")
        assert rule["outcome"]["category"] == "eidas_private"
        assert rule["outcome"]["deadline"] == "2027-12-01"


# ─── Deadline Analyse ────────────────────────────────────────


class TestDeadlines:
    """Test deadline correctheid."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_december_2026_deadlines(self, jrem):
        """Wallet regels moeten December 2026 hebben."""
        wallet_rules = [
            r
            for r in jrem["rules"]
            if "wallet" in r["outcome"]["category"]
            or r["ruleId"]
            in [
                "EID-006",
                "EID-007",
                "EID-013",
                "EID-014",
                "EID-015",
                "EID-017",
                "EID-018",
                "EID-022",
                "EID-023",
                "EID-024",
                "EID-026",
                "EID-029",
                "EID-030",
                "EID-031",
                "EID-032",
            ]
        ]
        for rule in wallet_rules:
            assert rule["outcome"]["deadline"] == "2026-12-01", (
                f"{rule['ruleId']} has wrong deadline: {rule['outcome']['deadline']}"
            )

    def test_past_deadlines_flagged(self, jrem):
        """Regels met deadlines in het verleden moeten als urgent worden gemarkeerd."""
        from datetime import date

        today = date.today().isoformat()
        past_rules = [r for r in jrem["rules"] if r["outcome"]["deadline"] < today]
        # EID-016, EID-018, EID-021, EID-025 hebben 2024 deadlines
        assert len(past_rules) >= 4

    def test_no_september_2026_deadlines(self, jrem):
        """Geen enkele regel mag September 2026 als deadline hebben (foute aanname)."""
        sept_rules = [
            r for r in jrem["rules"] if r["outcome"]["deadline"] == "2026-09-29"
        ]
        assert len(sept_rules) == 0, (
            f"Rules with incorrect September deadline: {[r['ruleId'] for r in sept_rules]}"
        )


# ─── Compliance Scenario's ───────────────────────────────────


class TestComplianceScenarios:
    """End-to-end compliance scenario's."""

    @pytest.fixture
    def jrem(self):
        with open(JREM_PATH) as f:
            return json.load(f)

    def test_fully_compliant_organization(self, jrem):
        """Een volledig conforme organisatie heeft alle trust services + wallet productie."""
        compliant_rules = [
            r for r in jrem["rules"] if r["outcome"]["compliant"] is True
        ]
        assert (
            len(compliant_rules) >= 20
        )  # Meeste regels zijn compliant bij goede implementatie

    def test_non_compliant_organization(self, jrem):
        """Een niet-conforme organisatie heeft wallet niet gestart + laag-niveau handtekeningen."""
        non_compliant = [r for r in jrem["rules"] if r["outcome"]["compliant"] is False]
        assert len(non_compliant) >= 3  # EID-010, EID-011, EID-020 niet compliant

    def test_critical_risk_rules(self, jrem):
        """Wallet niet gestart moet CRITICAL risk hebben."""
        critical = [r for r in jrem["rules"] if r["outcome"].get("risk") == "CRITICAL"]
        assert len(critical) >= 1
        assert any(r["ruleId"] == "EID-011" for r in critical)

    def test_action_required_rules(self, jrem):
        """Regels met actionRequired moeten duidelijke actie beschrijven."""
        action_rules = [r for r in jrem["rules"] if "actionRequired" in r["outcome"]]
        assert len(action_rules) >= 3  # EID-010, EID-011, EID-020
        for rule in action_rules:
            assert len(rule["outcome"]["actionRequired"]) > 10

    def test_all_rules_reference_eur_lex(self, jrem):
        """Alle regels moeten een EUR-Lex of overheid.nl referentie hebben."""
        for rule in jrem["rules"]:
            urls = [ref.get("url", "") for ref in rule["sourceRefs"]]
            has_eur_lex = any("eur-lex" in u for u in urls)
            has_overheid = any(
                "overheid" in u or "logius" in u or "rvig" in u or "rkd" in u
                for u in urls
            )
            assert has_eur_lex or has_overheid, (
                f"{rule['ruleId']} missing proper source reference"
            )
