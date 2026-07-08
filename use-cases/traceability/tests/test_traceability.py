import sys, json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app
JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("traceability", JREM_DIR, 8511)
client = TestClient(app)
def make_req(rid="TRACE-001"): return {"calculationDate":"2025-07-04","zaak":{"rechtsgebied":"civiel","zaakstroom":"handel","procedureType":"dagvaarding","vorderingWaarde":0,"bijzondereCategorie":rid},"partij":{"rol":"eiser","partijType":"natuurlijk_persoon","onvermogend":False,"verweerStatus":"n.v.t."}}
class TestHealth:
    def test_health(self): assert client.get("/v1/health").status_code == 200
    def test_domain(self): assert client.get("/v1/health").json()["domain"] == "traceability"
class TestCheck:
    def test_first(self): assert client.post("/v1/traceability/calculate", json=make_req()).status_code == 200
    def test_applied_rules(self): assert len(client.post("/v1/traceability/calculate", json=make_req()).json()["explanation"]["appliedRules"]) > 0
class TestAudit:
    def test_input_hash(self): assert client.post("/v1/traceability/calculate", json=make_req()).json()["audit"]["inputHash"].startswith("sha256:")
class TestIdempotentie:
    def test_same_id(self):
        r1 = client.post("/v1/traceability/calculate", json=make_req()); r2 = client.post("/v1/traceability/calculate", json=make_req())
        assert r1.json()["calculationId"] == r2.json()["calculationId"]
class TestInputValidatie:
    def test_invalid(self):
        req = make_req(); req["zaak"]["zaakstroom"] = "invalid"
        assert client.post("/v1/traceability/calculate", json=req).status_code == 422
class TestJREMValidation:
    def test_export_validates(self):
        import jsonschema; s = json.load(open(SHARED / "jrem-schema.json"))
        inst = json.load(open(JREM_DIR / "traceability-2025.1.json"))
        assert len(list(jsonschema.Draft202012Validator(s).iter_errors(inst))) == 0
    def test_source_refs(self):
        inst = json.load(open(JREM_DIR / "traceability-2025.1.json"))
        for r in inst["rules"]: assert len(r["sourceRefs"]) >= 1

class TestEvidenceEnvelope:
    def test_matrix_entry_has_evidence_envelope(self):
        sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
        from traceability_engine import build_traceability_matrix
        matrix = build_traceability_matrix(Path(__file__).parent.parent.parent.parent)
        entry = next(e for e in matrix["matrix"] if e["domain"] == "traceability")
        envelope = entry["evidenceEnvelope"]
        assert envelope["envelopeId"].startswith("sha256:")
        assert envelope["ruleId"] == entry["ruleId"]
        assert envelope["api"]["endpoint"] == entry["apiEndpoint"]
        assert envelope["acceptance"]["acceptatieType"] in {"draft", "full", "update"}

    def test_evidence_envelope_id_is_stable(self):
        sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
        from traceability_engine import build_traceability_matrix
        base = Path(__file__).parent.parent.parent.parent
        first = build_traceability_matrix(base)["matrix"][0]["evidenceEnvelope"]["envelopeId"]
        second = build_traceability_matrix(base)["matrix"][0]["evidenceEnvelope"]["envelopeId"]
        assert first == second

    def test_explicit_rule_test_mapping(self, tmp_path):
        sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
        from traceability_engine import _test_refs_for_rule
        test_file = tmp_path / "use-cases" / "sample" / "tests" / "test_sample.py"
        test_file.parent.mkdir(parents=True)
        test_file.write_text("""
def test_rule_is_applied():
    assert "RULE-001"

def test_other_rule():
    assert "RULE-002"
""")
        refs = _test_refs_for_rule(tmp_path, "sample", "RULE-001")
        assert refs == ["test_rule_is_applied"]
