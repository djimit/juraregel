"""Test suite voor BIO2 Compliance Rule Service."""
import sys, json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app, load_jrem

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("bio2", JREM_DIR, 8494)

# Custom endpoints
@app.get("/v1/bio2/maatregelen")
def get_maatregelen(categorie: str = None):
    jrem = load_jrem(JREM_DIR, "2025.1")
    maatregelen = []
    for rule in jrem.get("rules", []):
        rid = rule["ruleId"].replace("BIO2-", "")
        cat = rule["outcome"].get("category", "").replace("bio2_", "")
        iso_ref = ""
        for ref in rule.get("sourceRefs", []):
            if "ISO 27002" in ref.get("title", ""):
                iso_ref = ref.get("section", "")
                break
        if categorie and categorie.lower() not in cat.lower():
            continue
        maatregelen.append({"maatregelId": rid, "categorie": cat, "isoRef": iso_ref, "beschrijving": rule["name"][:100]})
    return {"maatregelen": maatregelen, "totaal": len(maatregelen)}

@app.get("/v1/bio2/rapport/{org_id}")
def get_rapport(org_id: str):
    jrem = load_jrem(JREM_DIR, "2025.1")
    from collections import defaultdict
    per_cat = defaultdict(lambda: {"totaal": 0, "onbekend": 0})
    for rule in jrem.get("rules", []):
        cat = rule["outcome"].get("category", "onbekend").replace("bio2_", "")
        per_cat[cat]["totaal"] += 1
        per_cat[cat]["onbekend"] += 1
    totaal = sum(v["totaal"] for v in per_cat.values())
    return {"organisatieId": org_id, "bioVersie": jrem["version"], "totaalMaatregelen": totaal, "score": 0.0, "perCategorie": dict(per_cat)}

client = TestClient(app)

def make_req(maatregel="5.01.01"):
    return {"calculationDate": "2026-07-04",
            "zaak": {"rechtsgebied": "civiel", "zaakstroom": "handel", "procedureType": "dagvaarding", "vorderingWaarde": 0, "bijzondereCategorie": maatregel},
            "partij": {"rol": "eiser", "partijType": "natuurlijk_persoon", "onvermogend": False, "verweerStatus": "n.v.t."}}

class TestHealth:
    def test_health(self): assert client.get("/v1/health").status_code == 200
    def test_domain(self): assert client.get("/v1/health").json()["domain"] == "bio2"

class TestCheckMaatregel:
    def test_5_01_01(self):
        r = client.post("/v1/bio2/calculate", json=make_req("5.01.01"))
        assert r.status_code == 200
        assert "bio2_" in r.json()["result"]["category"]
    def test_8_01_01(self):
        r = client.post("/v1/bio2/calculate", json=make_req("8.01.01"))
        assert r.status_code == 200
    def test_juridische_context(self):
        r = client.post("/v1/bio2/calculate", json=make_req())
        assert r.json()["juridischeContext"]["wet"] == "BIO2"
        assert r.json()["juridischeContext"]["wetBwbrId"] == "BWBR0044701"
    def test_applied_rules(self):
        r = client.post("/v1/bio2/calculate", json=make_req())
        assert len(r.json()["explanation"]["appliedRules"]) > 0
    def test_source_refs(self):
        r = client.post("/v1/bio2/calculate", json=make_req())
        assert len(r.json()["explanation"]["sourceRefs"]) >= 1

class TestMaatregelenListing:
    def test_all(self):
        r = client.get("/v1/bio2/maatregelen")
        assert r.status_code == 200
        assert r.json()["totaal"] >= 160
    def test_filter_organisatorisch(self):
        r = client.get("/v1/bio2/maatregelen?categorie=organisatorisch")
        assert r.status_code == 200
        assert all("organisatorisch" in m["categorie"].lower() for m in r.json()["maatregelen"])

class TestRapport:
    def test_rapport(self):
        r = client.get("/v1/bio2/rapport/test-org")
        assert r.status_code == 200
        assert r.json()["totaalMaatregelen"] >= 160
        assert "perCategorie" in r.json()

class TestAudit:
    def test_input_hash(self):
        r = client.post("/v1/bio2/calculate", json=make_req())
        assert r.json()["audit"]["inputHash"].startswith("sha256:")
    def test_ruleset_hash(self):
        r = client.post("/v1/bio2/calculate", json=make_req())
        assert r.json()["audit"]["rulesetHash"].startswith("sha256:")

class TestIdempotentie:
    def test_same_id(self):
        r1 = client.post("/v1/bio2/calculate", json=make_req())
        r2 = client.post("/v1/bio2/calculate", json=make_req())
        assert r1.json()["calculationId"] == r2.json()["calculationId"]

class TestInputValidatie:
    def test_invalid_zaakstroom(self):
        req = make_req(); req["zaak"]["zaakstroom"] = "invalid"
        assert client.post("/v1/bio2/calculate", json=req).status_code == 422

class TestJREMValidation:
    def test_schema_valid(self):
        import jsonschema; s = json.load(open(SHARED / "jrem-schema.json")); jsonschema.Draft202012Validator.check_schema(s)
    def test_export_validates(self):
        import jsonschema; s = json.load(open(SHARED / "jrem-schema.json"))
        inst = json.load(open(JREM_DIR / "bio2-maatregelen-2025.1.json"))
        assert len(list(jsonschema.Draft202012Validator(s).iter_errors(inst))) == 0
    def test_all_rules_have_source_refs(self):
        inst = json.load(open(JREM_DIR / "bio2-maatregelen-2025.1.json"))
        for r in inst["rules"]: assert len(r["sourceRefs"]) >= 1
    def test_all_rules_have_iso_ref(self):
        inst = json.load(open(JREM_DIR / "bio2-maatregelen-2025.1.json"))
        for r in inst["rules"]:
            has_iso = any("ISO" in ref.get("title","") for ref in r["sourceRefs"])
            assert has_iso, f"Rule {r['ruleId']} has no ISO 27002 sourceRef"
