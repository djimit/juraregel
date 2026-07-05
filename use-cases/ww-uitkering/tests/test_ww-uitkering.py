import sys, json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app
JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("ww-uitkering", JREM_DIR, 8503)
client = TestClient(app)
def make_req(rid="WW-001"): return {"calculationDate": "2025-07-04", "zaak": {"rechtsgebied": "civiel", "zaakstroom": "handel", "procedureType": "dagvaarding", "vorderingWaarde": 0, "bijzondereCategorie": rid}, "partij": {"rol": "eiser", "partijType": "natuurlijk_persoon", "onvermogend": False, "verweerStatus": "n.v.t."}}
class TestHealth:
    def test_health(self): assert client.get("/v1/health").status_code == 200
    def test_domain(self): assert client.get("/v1/health").json()["domain"] == "ww-uitkering"
class TestCheck:
    def test_first_regel(self): assert client.post("/v1/ww-uitkering/calculate", json=make_req()).status_code == 200
    def test_juridische_context(self): assert client.post("/v1/ww-uitkering/calculate", json=make_req()).json()["juridischeContext"]["wet"] == "Werkloosheidswet"
    def test_applied_rules(self): assert len(client.post("/v1/ww-uitkering/calculate", json=make_req()).json()["explanation"]["appliedRules"]) > 0
class TestAudit:
    def test_input_hash(self): assert client.post("/v1/ww-uitkering/calculate", json=make_req()).json()["audit"]["inputHash"].startswith("sha256:")
class TestIdempotentie:
    def test_same_id(self):
        r1 = client.post("/v1/ww-uitkering/calculate", json=make_req()); r2 = client.post("/v1/ww-uitkering/calculate", json=make_req())
        assert r1.json()["calculationId"] == r2.json()["calculationId"]
class TestInputValidatie:
    def test_invalid(self):
        req = make_req(); req["zaak"]["zaakstroom"] = "invalid"
        assert client.post("/v1/ww-uitkering/calculate", json=req).status_code == 422
class TestJREMValidation:
    def test_schema_valid(self):
        import jsonschema; s = json.load(open(SHARED / "jrem-schema.json")); jsonschema.Draft202012Validator.check_schema(s)
    def test_export_validates(self):
        import jsonschema; s = json.load(open(SHARED / "jrem-schema.json"))
        inst = json.load(open(JREM_DIR / "ww-uitkering-2025.1.json"))
        assert len(list(jsonschema.Draft202012Validator(s).iter_errors(inst))) == 0
    def test_source_refs(self):
        inst = json.load(open(JREM_DIR / "ww-uitkering-2025.1.json"))
        for r in inst["rules"]: assert len(r["sourceRefs"]) >= 1
