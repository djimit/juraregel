"""Test suite voor Procesreglement Rule Service — infrastructuur tests."""
import sys, json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("procesreglement", JREM_DIR, 8491)
client = TestClient(app)

def make_req(**kw):
    return {"calculationDate": "2026-07-03",
            "zaak": {"rechtsgebied": "civiel", "zaakstroom": kw.get("zaakstroom", "handel"), "procedureType": "dagvaarding", "vorderingWaarde": kw.get("vordering", 50000), "bijzondereCategorie": "geen"},
            "partij": {"rol": "eiser", "partijType": "natuurlijk_persoon", "onvermogend": False, "verweerStatus": "n.v.t."}}

class TestHealth:
    def test_health_ok(self):
        r = client.get("/v1/health"); assert r.status_code == 200; assert r.json()["status"] == "ok"
    def test_domain(self):
        r = client.get("/v1/health"); assert r.json()["domain"] == "procesreglement"

class TestCalculate:
    def test_handel_digitaal(self):
        r = client.post("/v1/procesreglement/calculate", json=make_req(zaakstroom="handel"))
        assert r.status_code == 200; assert r.json()["result"]["category"] == "digitaal_verplicht_handel"
    def test_kanton_digitaal(self):
        r = client.post("/v1/procesreglement/calculate", json=make_req(zaakstroom="kanton"))
        assert r.status_code == 200; assert r.json()["result"]["category"] == "digitaal_verplicht_kanton"
    def test_out_of_scope(self):
        req = make_req(); req["zaak"]["rechtsgebied"] = "strafrecht"
        r = client.post("/v1/procesreglement/calculate", json=req)
        assert r.json()["result"]["category"] == "out_of_scope"
    def test_juridische_context(self):
        r = client.post("/v1/procesreglement/calculate", json=make_req())
        assert r.json()["juridischeContext"] is not None
        assert r.json()["juridischeContext"]["wetBwbrId"] == "BWBR0002534"

class TestExplainability:
    def test_has_applied_rules(self):
        r = client.post("/v1/procesreglement/calculate", json=make_req())
        assert len(r.json()["explanation"]["appliedRules"]) > 0
    def test_has_reasoning_steps(self):
        r = client.post("/v1/procesreglement/calculate", json=make_req())
        assert len(r.json()["explanation"]["reasoningSteps"]) > 0
    def test_has_source_refs(self):
        r = client.post("/v1/procesreglement/calculate", json=make_req())
        assert len(r.json()["explanation"]["sourceRefs"]) > 0

class TestAudit:
    def test_has_input_hash(self):
        r = client.post("/v1/procesreglement/calculate", json=make_req())
        assert r.json()["audit"]["inputHash"].startswith("sha256:")
    def test_has_ruleset_hash(self):
        r = client.post("/v1/procesreglement/calculate", json=make_req())
        assert r.json()["audit"]["rulesetHash"].startswith("sha256:")

class TestIdempotentie:
    def test_same_input_same_id(self):
        r1 = client.post("/v1/procesreglement/calculate", json=make_req())
        r2 = client.post("/v1/procesreglement/calculate", json=make_req())
        assert r1.json()["calculationId"] == r2.json()["calculationId"]

class TestInputValidatie:
    def test_invalid_zaakstroom(self):
        req = make_req(); req["zaak"]["zaakstroom"] = "invalid"
        r = client.post("/v1/procesreglement/calculate", json=req)
        assert r.status_code == 422

class TestJREMValidation:
    def test_schema_valid(self):
        import jsonschema; schema = json.load(open(SHARED / "jrem-schema.json"))
        jsonschema.Draft202012Validator.check_schema(schema)
    def test_export_validates(self):
        import jsonschema; schema = json.load(open(SHARED / "jrem-schema.json"))
        inst = json.load(open(JREM_DIR / "procesreglement-civiel-2026.1.json"))
        errs = list(jsonschema.Draft202012Validator(schema).iter_errors(inst))
        assert len(errs) == 0
    def test_all_rules_have_source_refs(self):
        inst = json.load(open(JREM_DIR / "procesreglement-civiel-2026.1.json"))
        for r in inst["rules"]: assert len(r["sourceRefs"]) >= 1
