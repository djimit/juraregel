import sys, json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app
JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("dpia-model", JREM_DIR, 8507)
client = TestClient(app)
def make_req(rid="DPIA-001"): return {"calculationDate": "2025-07-04", "zaak": {"rechtsgebied": "civiel", "zaakstroom": "handel", "procedureType": "dagvaarding", "vorderingWaarde": 0, "bijzondereCategorie": rid}, "partij": {"rol": "eiser", "partijType": "natuurlijk_persoon", "onvermogend": False, "verweerStatus": "n.v.t."}}
class TestHealth:
    def test_health(self): assert client.get("/v1/health").status_code == 200
    def test_domain(self): assert client.get("/v1/health").json()["domain"] == "dpia-model"
class TestCheck:
    def test_dpia001(self): assert client.post("/v1/dpia-model/calculate", json=make_req("DPIA-001")).status_code == 200
    def test_juridische_context(self): assert "DPIA" in client.post("/v1/dpia-model/calculate", json=make_req()).json()["juridischeContext"]["wet"]
class TestDpiaBeslisboom:
    def test_grootschalig_bijzonder(self):
        # The beslisboom endpoint is in app.py but not in the test's create_app
        # Test via direct import
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "api"))
        exec(open(Path(__file__).parent.parent / "api" / "app.py").read(), globals())
        client_beslis = TestClient(app)
        r = client_beslis.get("/v1/dpia/vereist?verwerkingType=grootschalig&persoonsgegevensType=bijzonder")
        assert r.status_code == 200
        assert r.json()["dpiaVereist"] == True
    def test_klein_regulier(self):
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "api"))
        exec(open(Path(__file__).parent.parent / "api" / "app.py").read(), globals())
        client_beslis = TestClient(app)
        r = client_beslis.get("/v1/dpia/vereist?verwerkingType=klein&persoonsgegevensType=regulier&monitoring=nee&automatisering=nee")
        assert r.status_code == 200
        assert r.json()["dpiaVereist"] == False
    def test_monitoring(self):
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "api"))
        exec(open(Path(__file__).parent.parent / "api" / "app.py").read(), globals())
        client_beslis = TestClient(app)
        r = client_beslis.get("/v1/dpia/vereist?verwerkingType=klein&monitoring=ja")
        assert r.status_code == 200
        assert r.json()["dpiaVereist"] == True
class TestAudit:
    def test_input_hash(self): assert client.post("/v1/dpia-model/calculate", json=make_req()).json()["audit"]["inputHash"].startswith("sha256:")
class TestIdempotentie:
    def test_same_id(self):
        r1 = client.post("/v1/dpia-model/calculate", json=make_req()); r2 = client.post("/v1/dpia-model/calculate", json=make_req())
        assert r1.json()["calculationId"] == r2.json()["calculationId"]
class TestInputValidatie:
    def test_invalid(self):
        req = make_req(); req["zaak"]["zaakstroom"] = "invalid"
        assert client.post("/v1/dpia-model/calculate", json=req).status_code == 422
class TestJREMValidation:
    def test_schema_valid(self):
        import jsonschema; s = json.load(open(SHARED / "jrem-schema.json")); jsonschema.Draft202012Validator.check_schema(s)
    def test_export_validates(self):
        import jsonschema; s = json.load(open(SHARED / "jrem-schema.json"))
        inst = json.load(open(JREM_DIR / "dpia-model-2025.1.json"))
        assert len(list(jsonschema.Draft202012Validator(s).iter_errors(inst))) == 0
    def test_source_refs(self):
        inst = json.load(open(JREM_DIR / "dpia-model-2025.1.json"))
        for r in inst["rules"]: assert len(r["sourceRefs"]) >= 1
