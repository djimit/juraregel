import importlib.util
import json
import sys
from pathlib import Path

import jsonschema
from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[3]
USE_CASE = Path(__file__).resolve().parents[1]
SOURCE = USE_CASE / "sources" / "adr-itgc-kader-v1-1.zip"
JREM = USE_CASE / "jrem" / "exports" / "itgc-kader-2026.1.json"
sys.path.insert(0, str(USE_CASE / "lib"))

from itgc_parser import SOURCE_XLSX_SHA256, SOURCE_ZIP_SHA256, build_jrem


def keys(value):
    if isinstance(value, dict):
        return set(value) | {key for item in value.values() for key in keys(item)}
    if isinstance(value, list):
        return {key for item in value for key in keys(item)}
    return set()


def load_client() -> TestClient:
    path = USE_CASE / "api" / "app.py"
    spec = importlib.util.spec_from_file_location("itgc_kader_api", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return TestClient(module.app)


def test_official_source_snapshot_and_generated_catalog_are_reproducible():
    committed = json.loads(JREM.read_text())
    assert build_jrem(SOURCE) == committed
    assert SOURCE_ZIP_SHA256 == "9b50fc02cb03c6a505a0c9d939853afbcd3d71eaa330c62349e9152d61d0af17"
    assert SOURCE_XLSX_SHA256 == "bff440bd16fd8f6a03892b0a96d0e5e4c9b4eb6ae86da177b1d9d1f006188a7e"


def test_catalog_has_exact_source_counts_and_validates_against_both_schemas():
    data = json.loads(JREM.read_text())
    criteria = [
        criterion
        for rule in data["rules"]
        for criterion in rule["outcome"]["itgc"]["testCriteria"]
    ]
    assert len(data["rules"]) == 48
    assert len(criteria) == 147
    assert len({criterion["id"] for criterion in criteria}) == 147
    assert {rule["ruleId"].split("-")[1].split(".")[0] for rule in data["rules"]} == {
        "R1", "R2", "A1", "G1", "W1", "I1", "C1", "S1"
    }
    for schema_name in ("jrem-core.json", "jrem-schema.json"):
        schema = json.loads((ROOT / "shared" / schema_name).read_text())
        jsonschema.Draft202012Validator(schema).validate(data)


def test_api_is_catalog_only_and_never_claims_compliance_without_evidence():
    client = load_client()
    health = client.get("/v1/health").json()
    assert health["capabilities"] == {"catalog": True, "calculate": False}

    response = client.post("/v1/itgc-kader/calculate", json={})
    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "catalog_only"

    catalog = client.get("/v1/itgc-kader/maatregelen").json()
    assert catalog["assessmentStatus"] == "insufficient_evidence"
    assert catalog["totaalMaatregelen"] == 48
    assert catalog["totaalToetsingscriteria"] == 147
    assert "score" not in keys(catalog)


def test_objective_filter_preserves_exact_subtotals():
    client = load_client()
    expected = {"R1": 5, "R2": 5, "A1": 7, "G1": 5, "W1": 5, "I1": 5, "C1": 7, "S1": 9}
    for objective, count in expected.items():
        result = client.get("/v1/itgc-kader/maatregelen", params={"doelstelling": objective}).json()
        assert result["totaalMaatregelen"] == count
