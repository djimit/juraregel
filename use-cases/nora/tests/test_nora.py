"""Test suite voor NORA Compliance Rule Service — meta-laag."""
import sys, json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app, load_jrem

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("nora", JREM_DIR, 8497)

@app.get("/v1/nora/principes")
def get_principes(categorie: str = None):
    jrem = load_jrem(JREM_DIR, "2025.1")
    principes = []
    for rule in jrem.get("rules", []):
        cat = rule["outcome"].get("category", "").replace("nora_", "")
        if categorie and categorie.lower() not in cat.lower(): continue
        principes.append({"principeId": rule["ruleId"], "naam": rule["name"], "categorie": cat})
    return {"principes": principes, "totaal": len(principes)}

@app.get("/v1/nora/matrix")
def get_matrix():
    jrem = load_jrem(JREM_DIR, "2025.1")
    return {"matrix": [{"principeId": r["ruleId"], "principe": r["name"]} for r in jrem["rules"]], "totaal": len(jrem["rules"])}

client = TestClient(app)

def make_req(pid="NORA-001"):
    return {"calculationDate": "2025-07-04",
            "zaak": {"rechtsgebied": "civiel", "zaakstroom": "handel", "procedureType": "dagvaarding", "vorderingWaarde": 0, "bijzondereCategorie": pid},
            "partij": {"rol": "eiser", "partijType": "natuurlijk_persoon", "onvermogend": False, "verweerStatus": "n.v.t."}}

class TestHealth:
    def test_health(self): assert client.get("/v1/health").status_code == 200
    def test_domain(self): assert client.get("/v1/health").json()["domain"] == "nora"

class TestCheck:
    def test_principe_001(self):
        r = client.post("/v1/nora/calculate", json=make_req("NORA-001"))
        assert r.status_code == 200
    def test_juridische_context(self):
        r = client.post("/v1/nora/calculate", json=make_req())
        assert r.json()["juridischeContext"]["wet"] == "NORA"
    def test_applied_rules(self):
        r = client.post("/v1/nora/calculate", json=make_req())
        assert len(r.json()["explanation"]["appliedRules"]) > 0

class TestPrincipes:
    def test_all(self):
        r = client.get("/v1/nora/principes")
        assert r.json()["totaal"] >= 15
    def test_filter_beveiliging(self):
        r = client.get("/v1/nora/principes?categorie=beveiliging")
        assert all("beveiliging" in p["categorie"].lower() for p in r.json()["principes"])

class TestMatrix:
    def test_matrix(self):
        r = client.get("/v1/nora/matrix")
        assert r.status_code == 200
        assert r.json()["totaal"] >= 15

class TestAudit:
    def test_input_hash(self):
        r = client.post("/v1/nora/calculate", json=make_req())
        assert r.json()["audit"]["inputHash"].startswith("sha256:")

class TestIdempotentie:
    def test_same_id(self):
        r1 = client.post("/v1/nora/calculate", json=make_req())
        r2 = client.post("/v1/nora/calculate", json=make_req())
        assert r1.json()["calculationId"] == r2.json()["calculationId"]

class TestInputValidatie:
    def test_invalid(self):
        req = make_req(); req["zaak"]["zaakstroom"] = "invalid"
        assert client.post("/v1/nora/calculate", json=req).status_code == 422

class TestJREMValidation:
    def test_schema_valid(self):
        import jsonschema; s = json.load(open(SHARED / "jrem-schema.json")); jsonschema.Draft202012Validator.check_schema(s)
    def test_export_validates(self):
        import jsonschema; s = json.load(open(SHARED / "jrem-schema.json"))
        inst = json.load(open(JREM_DIR / "nora-principes-2025.1.json"))
        assert len(list(jsonschema.Draft202012Validator(s).iter_errors(inst))) == 0
    def test_source_refs(self):
        inst = json.load(open(JREM_DIR / "nora-principes-2025.1.json"))
        for r in inst["rules"]: assert len(r["sourceRefs"]) >= 1
