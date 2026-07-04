"""Test suite voor Overheidsstandaarden Compliance Rule Service."""
import sys, json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app, load_jrem

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("overheidsstandaarden", JREM_DIR, 8496)

@app.get("/v1/os/standaarden")
def get_standaarden(categorie: str = None, bron: str = None):
    jrem = load_jrem(JREM_DIR, "2025.1")
    standaarden = []
    for rule in jrem.get("rules", []):
        cat = rule["outcome"].get("category", "").replace("os_", "")
        if categorie and categorie.lower() not in cat.lower(): continue
        standaarden.append({"standaardId": rule["ruleId"], "naam": rule["name"], "categorie": cat})
    return {"standaarden": standaarden, "totaal": len(standaarden)}

@app.get("/v1/os/rapport/{org_id}")
def get_rapport(org_id: str):
    jrem = load_jrem(JREM_DIR, "2025.1")
    return {"organisatieId": org_id, "totaalStandaarden": len(jrem["rules"])}

client = TestClient(app)

def make_req(sid="OS-API-001"):
    return {"calculationDate": "2025-07-04",
            "zaak": {"rechtsgebied": "civiel", "zaakstroom": "handel", "procedureType": "dagvaarding", "vorderingWaarde": 0, "bijzondereCategorie": sid},
            "partij": {"rol": "eiser", "partijType": "natuurlijk_persoon", "onvermogend": False, "verweerStatus": "n.v.t."}}

class TestHealth:
    def test_health(self): assert client.get("/v1/health").status_code == 200
    def test_domain(self): assert client.get("/v1/health").json()["domain"] == "overheidsstandaarden"

class TestCheck:
    def test_api_design(self):
        r = client.post("/v1/overheidsstandaarden/calculate", json=make_req("OS-API-001"))
        assert r.status_code == 200
    def test_auth(self):
        r = client.post("/v1/overheidsstandaarden/calculate", json=make_req("OS-AUTH-001"))
        assert r.status_code == 200
    def test_events(self):
        r = client.post("/v1/overheidsstandaarden/calculate", json=make_req("OS-EVT-001"))
        assert r.status_code == 200
    def test_juridische_context(self):
        r = client.post("/v1/overheidsstandaarden/calculate", json=make_req())
        assert r.json()["juridischeContext"]["wet"] == "Logius Standaarden"
    def test_applied_rules(self):
        r = client.post("/v1/overheidsstandaarden/calculate", json=make_req())
        assert len(r.json()["explanation"]["appliedRules"]) > 0

class TestListing:
    def test_all(self):
        r = client.get("/v1/os/standaarden")
        assert r.json()["totaal"] >= 20
    def test_filter_api(self):
        r = client.get("/v1/os/standaarden?categorie=api-design")
        assert all("api" in s["categorie"].lower() for s in r.json()["standaarden"])

class TestRapport:
    def test_rapport(self):
        r = client.get("/v1/os/rapport/test-org")
        assert r.status_code == 200
        assert r.json()["totaalStandaarden"] >= 20

class TestAudit:
    def test_input_hash(self):
        r = client.post("/v1/overheidsstandaarden/calculate", json=make_req())
        assert r.json()["audit"]["inputHash"].startswith("sha256:")

class TestIdempotentie:
    def test_same_id(self):
        r1 = client.post("/v1/overheidsstandaarden/calculate", json=make_req())
        r2 = client.post("/v1/overheidsstandaarden/calculate", json=make_req())
        assert r1.json()["calculationId"] == r2.json()["calculationId"]

class TestInputValidatie:
    def test_invalid(self):
        req = make_req(); req["zaak"]["zaakstroom"] = "invalid"
        assert client.post("/v1/overheidsstandaarden/calculate", json=req).status_code == 422

class TestJREMValidation:
    def test_schema_valid(self):
        import jsonschema; s = json.load(open(SHARED / "jrem-schema.json")); jsonschema.Draft202012Validator.check_schema(s)
    def test_export_validates(self):
        import jsonschema; s = json.load(open(SHARED / "jrem-schema.json"))
        inst = json.load(open(JREM_DIR / "overheidsstandaarden-2025.1.json"))
        assert len(list(jsonschema.Draft202012Validator(s).iter_errors(inst))) == 0
    def test_source_refs(self):
        inst = json.load(open(JREM_DIR / "overheidsstandaarden-2025.1.json"))
        for r in inst["rules"]: assert len(r["sourceRefs"]) >= 1
