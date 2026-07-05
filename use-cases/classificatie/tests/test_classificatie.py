"""Test suite voor Classificatie Rule Service — infrastructuur tests."""
import sys, json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("classificatie", JREM_DIR, 8492)
client = TestClient(app)

def make_req(vw=50000):
    return {"calculationDate": "2026-07-03",
            "zaak": {"rechtsgebied": "civiel", "zaakstroom": "handel", "procedureType": "dagvaarding", "vorderingWaarde": vw, "bijzondereCategorie": "geen"},
            "partij": {"rol": "eiser", "partijType": "natuurlijk_persoon", "onvermogend": False, "verweerStatus": "n.v.t."}}

class TestHealth:
    def test_health(self): assert client.get("/v1/health").status_code == 200
    def test_domain(self): assert client.get("/v1/health").json()["domain"] == "classificatie"

class TestCalculate:
    def test_kanton(self):
        r = client.post("/v1/classificatie/calculate", json=make_req(5000))
        assert "kanton" in r.json()["result"]["category"].lower() or r.json()["result"]["category"].startswith("uc_")
    def test_handel(self):
        r = client.post("/v1/classificatie/calculate", json=make_req(50000))
        assert "handel" in r.json()["result"]["category"].lower() or r.json()["result"]["category"].startswith("uc_")
    def test_onbepaald_manual(self):
        req = make_req("onbepaald"); r = client.post("/v1/classificatie/calculate", json=req)
        assert r.json()["result"]["manualReviewRequired"] is True or r.json()["result"]["category"].startswith("uc_")
    def test_juridische_context(self):
        r = client.post("/v1/classificatie/calculate", json=make_req())
        assert r.json()["juridischeContext"]["wetBwbrId"] == "BWBR0002534"

class TestExplainability:
    def test_applied_rules(self):
        r = client.post("/v1/classificatie/calculate", json=make_req()); assert len(r.json()["explanation"]["appliedRules"]) > 0
    def test_reasoning_steps(self):
        r = client.post("/v1/classificatie/calculate", json=make_req()); assert len(r.json()["explanation"]["reasoningSteps"]) > 0
    def test_source_refs(self):
        r = client.post("/v1/classificatie/calculate", json=make_req()); assert len(r.json()["explanation"]["sourceRefs"]) > 0

class TestAudit:
    def test_input_hash(self):
        r = client.post("/v1/classificatie/calculate", json=make_req()); assert r.json()["audit"]["inputHash"].startswith("sha256:")
    def test_ruleset_hash(self):
        r = client.post("/v1/classificatie/calculate", json=make_req()); assert r.json()["audit"]["rulesetHash"].startswith("sha256:")

class TestIdempotentie:
    def test_same_id(self):
        r1 = client.post("/v1/classificatie/calculate", json=make_req())
        r2 = client.post("/v1/classificatie/calculate", json=make_req())
        assert r1.json()["calculationId"] == r2.json()["calculationId"]

class TestInputValidatie:
    def test_invalid_zaakstroom(self):
        req = make_req(); req["zaak"]["zaakstroom"] = "invalid"
        assert client.post("/v1/classificatie/calculate", json=req).status_code == 422

class TestJREMValidation:
    def test_schema_valid(self):
        import jsonschema; schema = json.load(open(SHARED / "jrem-schema.json")); jsonschema.Draft202012Validator.check_schema(schema)
    def test_export_validates(self):
        import jsonschema; schema = json.load(open(SHARED / "jrem-schema.json"))
        inst = json.load(open(JREM_DIR / "classificatie-zaak-intake-2026.1.json"))
        assert len(list(jsonschema.Draft202012Validator(schema).iter_errors(inst))) == 0
    def test_source_refs(self):
        inst = json.load(open(JREM_DIR / "classificatie-zaak-intake-2026.1.json"))
        for r in inst["rules"]: assert len(r["sourceRefs"]) >= 1
