"""Test suite voor Publicatie Rule Service — UC-06."""
import sys, json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("publicatie", JREM_DIR, 8493)
client = TestClient(app)

def make_req(**kw):
    return {"calculationDate": "2026-07-03",
            "zaak": {"rechtsgebied": kw.get("rechtsgebied", "civiel"), "zaakstroom": "handel", "procedureType": "dagvaarding", "vorderingWaarde": 50000, "bijzondereCategorie": "geen"},
            "partij": {"rol": "eiser", "partijType": "natuurlijk_persoon", "onvermogend": False, "verweerStatus": "n.v.t."}}

class TestHealth:
    def test_health(self): assert client.get("/v1/health").status_code == 200
    def test_domain(self): assert client.get("/v1/health").json()["domain"] == "publicatie"

class TestCalculate:
    def test_civiel_publiceerbaar(self):
        r = client.post("/v1/publicatie/calculate", json=make_req())
        assert r.status_code == 200; assert r.json()["result"]["category"] == "publiceerbaar"
    def test_out_of_scope(self):
        r = client.post("/v1/publicatie/calculate", json=make_req(rechtsgebied="strafrecht"))
        assert r.json()["result"]["category"] == "out_of_scope"
    def test_juridische_context(self):
        r = client.post("/v1/publicatie/calculate", json=make_req())
        jc = r.json().get("juridischeContext", {})
        assert jc.get("wetBwbrId") == "BWBR0004701"

class TestExplainability:
    def test_applied_rules(self):
        r = client.post("/v1/publicatie/calculate", json=make_req()); assert len(r.json()["explanation"]["appliedRules"]) > 0
    def test_reasoning_steps(self):
        r = client.post("/v1/publicatie/calculate", json=make_req()); assert len(r.json()["explanation"]["reasoningSteps"]) > 0
    def test_source_refs(self):
        r = client.post("/v1/publicatie/calculate", json=make_req()); assert len(r.json()["explanation"]["sourceRefs"]) > 0

class TestAudit:
    def test_input_hash(self):
        r = client.post("/v1/publicatie/calculate", json=make_req()); assert r.json()["audit"]["inputHash"].startswith("sha256:")
    def test_ruleset_hash(self):
        r = client.post("/v1/publicatie/calculate", json=make_req()); assert r.json()["audit"]["rulesetHash"].startswith("sha256:")

class TestIdempotentie:
    def test_same_id(self):
        r1 = client.post("/v1/publicatie/calculate", json=make_req())
        r2 = client.post("/v1/publicatie/calculate", json=make_req())
        assert r1.json()["calculationId"] == r2.json()["calculationId"]

class TestInputValidatie:
    def test_invalid_zaakstroom(self):
        req = make_req(); req["zaak"]["zaakstroom"] = "invalid"
        assert client.post("/v1/publicatie/calculate", json=req).status_code == 422

class TestJREMValidation:
    def test_schema_valid(self):
        import jsonschema; schema = json.load(open(SHARED / "jrem-schema.json")); jsonschema.Draft202012Validator.check_schema(schema)
    def test_export_validates(self):
        import jsonschema; schema = json.load(open(SHARED / "jrem-schema.json"))
        inst = json.load(open(JREM_DIR / "publicatie-regels-2026.1.json"))
        assert len(list(jsonschema.Draft202012Validator(schema).iter_errors(inst))) == 0
    def test_source_refs(self):
        inst = json.load(open(JREM_DIR / "publicatie-regels-2026.1.json"))
        for r in inst["rules"]: assert len(r["sourceRefs"]) >= 1
