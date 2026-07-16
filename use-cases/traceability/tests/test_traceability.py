import importlib.util
import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).parents[3]
path = Path(__file__).parents[1] / "api" / "app.py"
spec = importlib.util.spec_from_file_location("traceability_app", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
client = TestClient(module.app)


def test_matrix_has_stable_evidence_envelopes():
    first = client.get("/v1/traceability/matrix").json()
    second = client.get("/v1/traceability/matrix").json()
    assert first["totalRules"] == 702
    assert first["matrix"][0]["evidenceEnvelope"]["envelopeId"] == second["matrix"][0]["evidenceEnvelope"]["envelopeId"]


def test_explicit_rule_test_mapping(tmp_path):
    sys.path.insert(0, str(Path(__file__).parents[1] / "lib"))
    from traceability_engine import _test_refs_for_rule

    test_file = tmp_path / "use-cases" / "sample" / "tests" / "test_sample.py"
    test_file.parent.mkdir(parents=True)
    test_file.write_text('def test_rule_is_applied():\n    assert "RULE-001"\n')
    assert _test_refs_for_rule(tmp_path, "sample", "RULE-001") == [
        "use-cases/sample/tests/test_sample.py::test_rule_is_applied"
    ]


def test_impact_analysis_returns_affected_rules():
    result = client.get("/v1/impact/analyze?source=EU AI Act").json()
    assert result["affectedRules"] > 0
