"""
Test suite voor Griffierecht Rule Service PoC.

Dekt:
- Unit tests (positief + negatief per tariefcategorie)
- Boundary tests (exacte grenswaarden €100.000, €100.000,01, €1.000.000, €1.000.000,01)
- Regression tests (2025 vs 2026 tariefsets)
- Explainability tests (response bevat appliedRules + sourceRefs + reasoningSteps)
- Audit tests (inputHash + rulesetHash + timestamp)
- Scenario tests (ingebde scenarios uit JREM)
"""

import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add shared to path
SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app, load_jrem as _load_jrem, list_versions as _list_versions

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("griffierecht", JREM_DIR, 8490)

def load_jrem(version):
    return _load_jrem(JREM_DIR, version)

def list_versions():
    return _list_versions(JREM_DIR)

client = TestClient(app)


# ─── Helpers ───

def make_request(zaakstroom="handel", rol="eiser", partij_type="natuurlijk_persoon",
                 vordering_waarde=50000, verweer_status="n.v.t.", onvermogend=False,
                 calculation_date="2026-07-03", bijzondere_categorie="geen", tariefjaar=None):
    """Build a standard calculate request."""
    return {
        "calculationDate": calculation_date,
        "zaak": {
            "rechtsgebied": "civiel",
            "zaakstroom": zaakstroom,
            "procedureType": "dagvaarding",
            "vorderingWaarde": vordering_waarde,
            "bijzondereCategorie": bijzondere_categorie,
        },
        "partij": {
            "rol": rol,
            "partijType": partij_type,
            "onvermogend": onvermogend,
            "verweerStatus": verweer_status,
        },
        "tariefjaar": tariefjaar,
    }


def calculate(req):
    """Call the calculate endpoint and return the response."""
    r = client.post("/v1/griffierecht/calculate", json=req)
    assert r.status_code == 200, f"Calculate failed: {r.status_code} {r.text}"
    return r.json()


# ═══════════════════════════════════════════
# UNIT TESTS — Happy Path per tariefcategorie
# ═══════════════════════════════════════════

class TestHappyPath:
    """Positieve tests voor elke tariefcategorie."""

    def test_handel_onbepaald_natuurlijk(self):
        """Onbepaalde waarde, handel, natuurlijk persoon → €364 (2026)."""
        r = calculate(make_request(vordering_waarde="onbepaald"))
        assert r["result"]["griffierecht"]["amount"] == 364
        assert r["result"]["category"] == "onbepaald_natuurlijk"

    def test_handel_onbepaald_niet_natuurlijk(self):
        """Onbepaalde waarde, handel, niet-natuurlijk persoon → €727 (2026)."""
        r = calculate(make_request(partij_type="niet_natuurlijk_persoon", vordering_waarde="onbepaald"))
        assert r["result"]["griffierecht"]["amount"] == 727

    def test_handel_lte_100k_natuurlijk(self):
        """Vordering ≤ €100.000, handel, natuurlijk persoon → €364 (2026)."""
        r = calculate(make_request(vordering_waarde=50000))
        assert r["result"]["griffierecht"]["amount"] == 364
        assert r["result"]["category"] == "vordering_lte_100000_natuurlijk"

    def test_handel_lte_100k_niet_natuurlijk(self):
        """Vordering ≤ €100.000, handel, niet-natuurlijk persoon → €727 (2026)."""
        r = calculate(make_request(partij_type="niet_natuurlijk_persoon", vordering_waarde=75000))
        assert r["result"]["griffierecht"]["amount"] == 727

    def test_handel_gt_100k_lte_1m_natuurlijk(self):
        """Vordering > €100.000 en ≤ €1.000.000, handel, natuurlijk persoon → €2.803 (2026)."""
        r = calculate(make_request(vordering_waarde=125000))
        assert r["result"]["griffierecht"]["amount"] == 2803
        assert r["result"]["category"] == "vordering_gt_100000_lte_1000000_natuurlijk"

    def test_handel_gt_100k_lte_1m_niet_natuurlijk(self):
        """Vordering > €100.000 en ≤ €1.000.000, handel, niet-natuurlijk persoon → €3.616 (2026)."""
        r = calculate(make_request(partij_type="niet_natuurlijk_persoon", vordering_waarde=500000))
        assert r["result"]["griffierecht"]["amount"] == 3616

    def test_handel_gt_1m_natuurlijk(self):
        """Vordering > €1.000.000, handel, natuurlijk persoon → €3.616 (2026)."""
        r = calculate(make_request(vordering_waarde=2000000))
        assert r["result"]["griffierecht"]["amount"] == 3616

    def test_handel_gt_1m_niet_natuurlijk(self):
        """Vordering > €1.000.000, handel, niet-natuurlijk persoon → €5.644 (2026)."""
        r = calculate(make_request(partij_type="niet_natuurlijk_persoon", vordering_waarde=2500000))
        assert r["result"]["griffierecht"]["amount"] == 5644

    def test_kanton_natuurlijk(self):
        """Kantonzaken, eiser, natuurlijk persoon → €91 (2026)."""
        r = calculate(make_request(zaakstroom="kanton", vordering_waarde=5000))
        assert r["result"]["griffierecht"]["amount"] == 91

    def test_kanon_nnp_onder_25k(self):
        """Kantonzaken, eiser, niet-natuurlijk persoon, ≤ €25.000 → €91 (2026)."""
        r = calculate(make_request(zaakstroom="kanton", partij_type="niet_natuurlijk_persoon", vordering_waarde=10000))
        assert r["result"]["griffierecht"]["amount"] == 91

    def test_kanon_nnp_boven_25k(self):
        """Kantonzaken, eiser, niet-natuurlijk persoon, > €25.000 → €727 (2026)."""
        r = calculate(make_request(zaakstroom="kanton", partij_type="niet_natuurlijk_persoon", vordering_waarde=50000))
        assert r["result"]["griffierecht"]["amount"] == 727

    def test_onvermogend_handel_lte_100k(self):
        """Onvermogend, handel, ≤ €100.000 → zelfde tarief als natuurlijk persoon."""
        r = calculate(make_request(onvermogend=True, vordering_waarde=50000))
        assert r["result"]["griffierecht"]["amount"] == 364


# ═══════════════════════════════════════════
# NEGATIVE TESTS — Geen griffierecht
# ═══════════════════════════════════════════

class TestNegativeCases:
    """Negatieve tests — geen griffierecht verschuldigd."""

    def test_kanton_gedaagde_niet_verschuldigd(self):
        """Kantonzaken — gedaagde betaalt geen griffierecht."""
        r = calculate(make_request(zaakstroom="kanton", rol="gedaagde", verweer_status="ingediend"))
        assert r["result"]["griffierecht"]["amount"] is None
        assert r["result"]["category"] == "kanton_gedaagde_niet_verschuldigd"

    def test_handel_gedaagde_zonder_verweer(self):
        """Handel — gedaagde zonder verweer betaalt geen griffierecht."""
        r = calculate(make_request(rol="gedaagde", verweer_status="niet_ingediend"))
        assert r["result"]["griffierecht"]["amount"] is None
        assert r["result"]["category"] == "gedaagde_geen_verweer"

    def test_strafrecht_out_of_scope(self):
        """Strafrecht is out-of-scope voor PoC."""
        req = make_request()
        req["zaak"]["rechtsgebied"] = "strafrecht"
        r = calculate(req)
        assert r["result"]["category"] == "out_of_scope"
        assert r["result"]["manualReviewRequired"] is True
        assert len(r["warnings"]) > 0

    def test_bestuursrecht_out_of_scope(self):
        """Bestuursrecht is out-of-scope voor PoC."""
        req = make_request()
        req["zaak"]["rechtsgebied"] = "bestuursrecht"
        r = calculate(req)
        assert r["result"]["category"] == "out_of_scope"


# ═══════════════════════════════════════════
# BOUNDARY TESTS — Exacte grenswaarden
# ═══════════════════════════════════════════

class TestBoundaryCases:
    """Boundary tests — exacte grenswaarden voor tariefcategorieën."""

    def test_exact_100000_natuurlijk(self):
        """Exact €100.000 valt in ≤€100.000 categorie (lte operator)."""
        r = calculate(make_request(vordering_waarde=100000))
        assert r["result"]["griffierecht"]["amount"] == 364
        assert "lte_100000" in r["result"]["category"]

    def test_100000_01_natuurlijk(self):
        """€100.000,01 valt in >€100.000-≤€1.000.000 categorie (gt operator)."""
        r = calculate(make_request(vordering_waarde=100000.01))
        assert r["result"]["griffierecht"]["amount"] == 2803
        assert "gt_100000" in r["result"]["category"]

    def test_exact_100000_niet_natuurlijk(self):
        """Exact €100.000 voor niet-natuurlijk persoon → €727."""
        r = calculate(make_request(partij_type="niet_natuurlijk_persoon", vordering_waarde=100000))
        assert r["result"]["griffierecht"]["amount"] == 727

    def test_100000_01_niet_natuurlijk(self):
        """€100.000,01 voor niet-natuurlijk persoon → €3.616."""
        r = calculate(make_request(partij_type="niet_natuurlijk_persoon", vordering_waarde=100000.01))
        assert r["result"]["griffierecht"]["amount"] == 3616

    def test_exact_1000000_natuurlijk(self):
        """Exact €1.000.000 valt in >€100.000-≤€1.000.000 categorie (lte operator)."""
        r = calculate(make_request(vordering_waarde=1000000))
        assert r["result"]["griffierecht"]["amount"] == 2803

    def test_1000000_01_natuurlijk(self):
        """€1.000.000,01 valt in >€1.000.000 categorie (gt operator)."""
        r = calculate(make_request(vordering_waarde=1000000.01))
        assert r["result"]["griffierecht"]["amount"] == 3616

    def test_exact_1000000_niet_natuurlijk(self):
        """Exact €1.000.000 voor niet-natuurlijk persoon → €3.616."""
        r = calculate(make_request(partij_type="niet_natuurlijk_persoon", vordering_waarde=1000000))
        assert r["result"]["griffierecht"]["amount"] == 3616

    def test_1000000_01_niet_natuurlijk(self):
        """€1.000.000,01 voor niet-natuurlijk persoon → €5.644."""
        r = calculate(make_request(partij_type="niet_natuurlijk_persoon", vordering_waarde=1000000.01))
        assert r["result"]["griffierecht"]["amount"] == 5644

    def test_kanton_25000_nnp(self):
        """Exact €25.000 voor NNP in kanton → €91 (lte operator)."""
        r = calculate(make_request(zaakstroom="kanton", partij_type="niet_natuurlijk_persoon", vordering_waarde=25000))
        assert r["result"]["griffierecht"]["amount"] == 91

    def test_kanton_25000_01_nnp(self):
        """€25.000,01 voor NNP in kanton → €727 (gt operator)."""
        r = calculate(make_request(zaakstroom="kanton", partij_type="niet_natuurlijk_persoon", vordering_waarde=25000.01))
        assert r["result"]["griffierecht"]["amount"] == 727

    def test_vordering_nul(self):
        """Vordering van €0 moet werken (gte: 0 in conditions)."""
        r = calculate(make_request(vordering_waarde=0))
        assert r["result"]["griffierecht"]["amount"] is not None

    def test_vordering_negatief(self):
        """Negatieve vordering wordt afgewezen door input-validatie (422)."""
        req = make_request(vordering_waarde=-100)
        r = client.post("/v1/griffierecht/calculate", json=req)
        assert r.status_code == 422


# ═══════════════════════════════════════════
# REGRESSION TESTS — 2025 vs 2026
# ═══════════════════════════════════════════

class TestRegression:
    """Regression tests — 2025 en 2026 tariefsets naast elkaar."""

    def test_2026_amount_differs_from_2025(self):
        """2026 tarief moet hoger zijn dan 2025 (indexatie)."""
        r2026 = calculate(make_request(vordering_waarde=125000, tariefjaar=2026))
        r2025 = calculate(make_request(vordering_waarde=125000, tariefjaar=2025))
        assert r2026["result"]["griffierecht"]["amount"] > r2025["result"]["griffierecht"]["amount"]

    def test_2025_groter_dan_100k_natuurlijk(self):
        """2025: >€100K-≤€1M, NP → €2.749."""
        r = calculate(make_request(vordering_waarde=125000, tariefjaar=2025))
        assert r["result"]["griffierecht"]["amount"] == 2749
        assert r["ruleSetVersion"] == "2025.1"

    def test_2026_groter_dan_100k_natuurlijk(self):
        """2026: >€100K-≤€1M, NP → €2.803."""
        r = calculate(make_request(vordering_waarde=125000, tariefjaar=2026))
        assert r["result"]["griffierecht"]["amount"] == 2803
        assert r["ruleSetVersion"] == "2026.1"

    def test_2025_kanton_natuurlijk(self):
        """2025: kanton, NP → €89."""
        r = calculate(make_request(zaakstroom="kanton", vordering_waarde=5000, tariefjaar=2025))
        assert r["result"]["griffierecht"]["amount"] == 89

    def test_2026_kanton_natuurlijk(self):
        """2026: kanton, NP → €91."""
        r = calculate(make_request(zaakstroom="kanton", vordering_waarde=5000, tariefjaar=2026))
        assert r["result"]["griffierecht"]["amount"] == 91

    def test_2025_gt_1m_nnp(self):
        """2025: >€1M, NNP → €5.535."""
        r = calculate(make_request(partij_type="niet_natuurlijk_persoon", vordering_waarde=2500000, tariefjaar=2025))
        assert r["result"]["griffierecht"]["amount"] == 5535

    def test_2026_gt_1m_nnp(self):
        """2026: >€1M, NNP → €5.644."""
        r = calculate(make_request(partij_type="niet_natuurlijk_persoon", vordering_waarde=2500000, tariefjaar=2026))
        assert r["result"]["griffierecht"]["amount"] == 5644

    def test_both_versions_available(self):
        """Both 2025 and 2026 versions are available."""
        versions = list_versions()
        version_ids = [v["version"] for v in versions]
        assert "2025.1" in version_ids
        assert "2026.1" in version_ids


# ═══════════════════════════════════════════
# EXPLAINABILITY TESTS
# ═══════════════════════════════════════════

class TestExplainability:
    """Every calculate response must contain explanation with appliedRules, sourceRefs, and reasoningSteps."""

    def test_has_applied_rules(self):
        """Response must contain at least one appliedRule."""
        r = calculate(make_request(vordering_waarde=125000))
        assert len(r["explanation"]["appliedRules"]) > 0

    def test_has_source_refs(self):
        """Response must contain at least one sourceRef."""
        r = calculate(make_request(vordering_waarde=125000))
        assert len(r["explanation"]["sourceRefs"]) > 0
        for ref in r["explanation"]["sourceRefs"]:
            assert "title" in ref
            assert "type" in ref

    def test_has_reasoning_steps(self):
        """Response must contain reasoningSteps array."""
        r = calculate(make_request(vordering_waarde=125000))
        assert len(r["explanation"]["reasoningSteps"]) > 0
        for step in r["explanation"]["reasoningSteps"]:
            assert isinstance(step, str)
            assert len(step) > 5

    def test_has_summary(self):
        """Response must contain a summary string."""
        r = calculate(make_request(vordering_waarde=50000))
        assert isinstance(r["explanation"]["summary"], str)
        assert len(r["explanation"]["summary"]) > 20

    def test_applied_rule_has_source_ref_in_jrem(self):
        """The applied rule must have sourceRefs in the JREM model."""
        r = calculate(make_request(vordering_waarde=125000))
        rule_id = r["explanation"]["appliedRules"][0]
        jrem = load_jrem("2026.1")
        rule = next(r for r in jrem["rules"] if r["ruleId"] == rule_id)
        assert len(rule["sourceRefs"]) >= 1

    def test_gedaagde_onbekend_has_manual_review(self):
        """Gedaagde with unknown verweerStatus must have manualReviewRequired and warning."""
        r = calculate(make_request(rol="gedaagde", verweer_status="onbekend"))
        assert r["result"]["manualReviewRequired"] is True
        assert len(r["warnings"]) > 0
        assert "onbekend" in r["warnings"][0].lower()


# ═══════════════════════════════════════════
# AUDIT TESTS
# ═══════════════════════════════════════════

class TestAudit:
    """Audit trail tests."""

    def test_has_input_hash(self):
        """Response must contain inputHash."""
        r = calculate(make_request(vordering_waarde=50000))
        assert "inputHash" in r["audit"]
        assert r["audit"]["inputHash"].startswith("sha256:")

    def test_has_ruleset_hash(self):
        """Response must contain rulesetHash."""
        r = calculate(make_request(vordering_waarde=50000))
        assert "rulesetHash" in r["audit"]
        assert r["audit"]["rulesetHash"].startswith("sha256:")

    def test_has_timestamp(self):
        """Response must contain timestamp."""
        r = calculate(make_request(vordering_waarde=50000))
        assert "timestamp" in r["audit"]
        assert "T" in r["audit"]["timestamp"]

    def test_audit_endpoint_returns_record(self):
        """GET /v1/audit/{calculationId} returns the stored audit record."""
        r = calculate(make_request(vordering_waarde=50000))
        calc_id = r["calculationId"]
        audit_r = client.get(f"/v1/audit/{calc_id}")
        assert audit_r.status_code == 200
        audit_data = audit_r.json()
        assert audit_data["calculationId"] == calc_id
        assert "inputHash" in audit_data
        assert "rulesetHash" in audit_data

    def test_audit_404_for_unknown_id(self):
        """GET /v1/audit/unknown returns 404."""
        r = client.get("/v1/audit/nonexistent-id")
        assert r.status_code == 404


# ═══════════════════════════════════════════
# IDEMPOTENTIE TESTS
# ═══════════════════════════════════════════

class TestIdempotentie:
    """Idempotentie tests — same input + same version = same calculationId."""

    def test_same_input_same_calculation_id(self):
        """Two identical requests must produce the same calculationId."""
        req = make_request(vordering_waarde=125000)
        r1 = calculate(req)
        r2 = calculate(req)
        assert r1["calculationId"] == r2["calculationId"]

    def test_different_input_different_calculation_id(self):
        """Different input must produce different calculationId."""
        r1 = calculate(make_request(vordering_waarde=125000))
        r2 = calculate(make_request(vordering_waarde=200000))
        assert r1["calculationId"] != r2["calculationId"]

    def test_different_version_different_calculation_id(self):
        """Same input but different tariefjaar must produce different calculationId."""
        r1 = calculate(make_request(vordering_waarde=125000, tariefjaar=2025))
        r2 = calculate(make_request(vordering_waarde=125000, tariefjaar=2026))
        assert r1["calculationId"] != r2["calculationId"]


# ═══════════════════════════════════════════
# SCENARIO TESTS — Ingebedde scenarios uit JREM
# ═══════════════════════════════════════════

class TestJREMScenarios:
    """Run the scenarios embedded in the JREM exports."""

    @pytest.mark.parametrize("version", ["2025.1", "2026.1"])
    def test_all_scenarios(self, version):
        """All embedded scenarios must produce the expected result."""
        jrem = load_jrem(version)
        scenarios = jrem.get("scenarios", [])
        assert len(scenarios) > 0, f"No scenarios in JREM {version}"
        
        for sc in scenarios:
            inp = sc["input"]
            expected = sc["expected"]
            
            req = {
                "calculationDate": f"{version.split('.')[0]}-07-03",
                "zaak": {
                    "rechtsgebied": inp.get("rechtsgebied", "civiel"),
                    "zaakstroom": inp.get("zaakstroom", "handel"),
                    "procedureType": inp.get("procedureType", "dagvaarding"),
                    "vorderingWaarde": inp.get("vorderingWaarde", 50000),
                    "bijzondereCategorie": inp.get("bijzondereCategorie", "geen"),
                },
                "partij": {
                    "rol": inp.get("rol", "eiser"),
                    "partijType": inp.get("partijType", "natuurlijk_persoon"),
                    "onvermogend": inp.get("onvermogend", False),
                    "verweerStatus": inp.get("verweerStatus", "n.v.t."),
                },
                "tariefjaar": int(version.split(".")[0]),
            }
            
            r = calculate(req)
            
            # Check expected amount
            expected_amount = expected["griffierecht"]
            actual_amount = r["result"]["griffierecht"]["amount"]
            if expected_amount == 0:
                assert actual_amount is None or actual_amount == 0, \
                    f"Scenario {sc['id']}: expected 0/None, got {actual_amount}"
            else:
                assert actual_amount == expected_amount, \
                    f"Scenario {sc['id']}: expected {expected_amount}, got {actual_amount}"
            
            # Check applied rules
            expected_rules = expected.get("appliedRules", [])
            # Rule IDs in 2025 have 2025 instead of 2026
            actual_rules = r["explanation"]["appliedRules"]
            if version == "2025.1":
                expected_rules = [r.replace("2026", "2025") for r in expected_rules]
            assert set(actual_rules) == set(expected_rules), \
                f"Scenario {sc['id']}: expected rules {expected_rules}, got {actual_rules}"


# ═══════════════════════════════════════════
# JREM SCHEMA VALIDATION TESTS
# ═══════════════════════════════════════════

class TestJREMValidation:
    """JREM schema validation tests."""

    def test_schema_is_valid_2020_12(self):
        """Schema must be valid JSON Schema draft 2020-12."""
        import jsonschema
        schema = json.load(open(Path(__file__).parent.parent.parent.parent / "shared" / "jrem-core.json"))
        jsonschema.Draft202012Validator.check_schema(schema)

    def test_2026_export_validates(self):
        """2026 JREM export must validate against schema."""
        import jsonschema
        schema = json.load(open(Path(__file__).parent.parent.parent.parent / "shared" / "jrem-core.json"))
        instance = json.load(open(JREM_DIR / "griffierecht-civiel-2026.1.json"))
        validator = jsonschema.Draft202012Validator(schema)
        errors = list(validator.iter_errors(instance))
        assert len(errors) == 0, f"Validation errors: {errors}"

    def test_2025_export_validates(self):
        """2025 JREM export must validate against schema."""
        import jsonschema
        schema = json.load(open(Path(__file__).parent.parent.parent.parent / "shared" / "jrem-core.json"))
        instance = json.load(open(JREM_DIR / "griffierecht-civiel-2025.1.json"))
        validator = jsonschema.Draft202012Validator(schema)
        errors = list(validator.iter_errors(instance))
        assert len(errors) == 0, f"Validation errors: {errors}"

    def test_all_rules_have_source_refs(self):
        """Every rule must have at least 1 sourceRef (brontraceability)."""
        for version in ["2025.1", "2026.1"]:
            jrem = load_jrem(version)
            for rule in jrem["rules"]:
                assert len(rule["sourceRefs"]) >= 1, \
                    f"Rule {rule['ruleId']} in {version} has no sourceRefs"

    def test_all_rules_have_validity(self):
        """Every ruleset must have validFrom and validUntil."""
        for version in ["2025.1", "2026.1"]:
            jrem = load_jrem(version)
            assert "validFrom" in jrem
            assert "validUntil" in jrem
