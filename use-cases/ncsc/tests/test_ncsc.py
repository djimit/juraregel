"""Test suite voor NCSC Cybersecurity Rule Service."""
import sys, json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app, load_jrem
JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("ncsc", JREM_DIR, 8500)

@app.get("/v1/ncsc/richtlijnen")
def get_richtlijnen(categorie: str = None):
    jrem = load_jrem(JREM_DIR, "2025.1")
    r = [{"regelId": rule["ruleId"], "naam": rule["name"], "categorie": rule["outcome"].get("category","").replace("ncsc_","")} for rule in jrem["rules"]]
    if categorie: r = [x for x in r if categorie.lower() in x["categorie"].lower()]
    return {"richtlijnen": r, "totaal": len(r)}

@app.get("/v1/ncsc/rapport/{org_id}")
def get_rapport(org_id: str):
    jrem = load_jrem(JREM_DIR, "2025.1")
    return {"organisatieId": org_id, "totaalRichtlijnen": len(jrem["rules"])}

client = TestClient(app)
def make_req(rid="NCSC-TLS-001"): return {"calculationDate": "2025-07-04", "zaak": {"rechtsgebied": "civiel", "zaakstroom": "handel", "procedureType": "dagvaarding", "vorderingWaarde": 0, "bijzondereCategorie": rid}, "partij": {"rol": "eiser", "partijType": "natuurlijk_persoon", "onvermogend": False, "verweerStatus": "n.v.t."}}

class TestHealth:
    def test_health(self): assert client.get("/v1/health").status_code == 200
    def test_domain(self): assert client.get("/v1/health").json()["domain"] == "ncsc"
class TestCheck:
    def test_tls001(self): assert client.post("/v1/ncsc/calculate", json=make_req("NCSC-TLS-001")).status_code == 200
    def test_web001(self): assert client.post("/v1/ncsc/calculate", json=make_req("NCSC-WEB-001")).status_code == 200
    def test_bas001(self): assert client.post("/v1/ncsc/calculate", json=make_req("NCSC-BAS-001")).status_code == 200
    def test_cyb001(self): assert client.post("/v1/ncsc/calculate", json=make_req("NCSC-CYB-001")).status_code == 200
    def test_juridische_context(self): assert client.post("/v1/ncsc/calculate", json=make_req()).json()["juridischeContext"]["wet"] == "NCSC"
    def test_applied_rules(self): assert len(client.post("/v1/ncsc/calculate", json=make_req()).json()["explanation"]["appliedRules"]) > 0
class TestListing:
    def test_all(self):
        r = client.get("/v1/ncsc/richtlijnen"); assert r.json()["totaal"] >= 30
    def test_filter_tls(self):
        r = client.get("/v1/ncsc/richtlijnen?categorie=tls"); assert all("tls" in x["categorie"].lower() for x in r.json()["richtlijnen"])
class TestRapport:
    def test_rapport(self): assert client.get("/v1/ncsc/rapport/test").json()["totaalRichtlijnen"] >= 30
class TestAudit:
    def test_input_hash(self): assert client.post("/v1/ncsc/calculate", json=make_req()).json()["audit"]["inputHash"].startswith("sha256:")
class TestIdempotentie:
    def test_same_id(self):
        r1 = client.post("/v1/ncsc/calculate", json=make_req()); r2 = client.post("/v1/ncsc/calculate", json=make_req())
        assert r1.json()["calculationId"] == r2.json()["calculationId"]
class TestInputValidatie:
    def test_invalid(self):
        req = make_req(); req["zaak"]["zaakstroom"] = "invalid"
        assert client.post("/v1/ncsc/calculate", json=req).status_code == 422
class TestJREMValidation:
    def test_schema_valid(self):
        import jsonschema; s = json.load(open(SHARED / "jrem-schema.json")); jsonschema.Draft202012Validator.check_schema(s)
    def test_export_validates(self):
        import jsonschema; s = json.load(open(SHARED / "jrem-schema.json"))
        inst = json.load(open(JREM_DIR / "ncsc-richtlijnen-2025.1.json"))
        assert len(list(jsonschema.Draft202012Validator(s).iter_errors(inst))) == 0
    def test_source_refs(self):
        inst = json.load(open(JREM_DIR / "ncsc-richtlijnen-2025.1.json"))
        for r in inst["rules"]: assert len(r["sourceRefs"]) >= 1
