import importlib.util
import json
import sys
from pathlib import Path

import jsonschema
from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[3]
USE_CASE = Path(__file__).resolve().parents[1]
JREM_PATH = USE_CASE / "jrem" / "exports" / "judicial-ai-assurance-2026.1.json"
SOURCE_REGISTER_PATH = USE_CASE / "sources" / "source-register.json"

sys.path.insert(0, str(ROOT / "shared"))

from registry import can_calculate, list_domains


def load_jrem() -> dict:
    return json.loads(JREM_PATH.read_text())


def load_source_register() -> dict:
    return json.loads(SOURCE_REGISTER_PATH.read_text())


def load_client() -> TestClient:
    app_path = USE_CASE / "api" / "app.py"
    spec = importlib.util.spec_from_file_location("judicial_ai_assurance_api", app_path)
    assert spec is not None, f"Spec kon niet worden geladen voor {app_path}"
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None, "Spec loader is None"
    spec.loader.exec_module(module)
    return TestClient(module.app)


def test_jrem_validates_against_shared_schema():
    schema = json.loads((ROOT / "shared" / "jrem-schema.json").read_text())
    errors = list(jsonschema.Draft202012Validator(schema).iter_errors(load_jrem()))
    assert errors == []


def test_profile_is_catalog_only_and_auto_discovered():
    assert can_calculate("judicial-ai-assurance") is False
    domains = {item["domain"] for item in list_domains(ROOT / "use-cases")}
    assert "judicial-ai-assurance" in domains

    client = load_client()
    health = client.get("/v1/health").json()
    assert health["status"] == "ok"
    assert health["capabilities"] == {"catalog": True, "calculate": False}

    response = client.post("/v1/judicial-ai-assurance/calculate", json={})
    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "catalog_only"


def test_profile_has_twelve_reviewable_controls_without_aggregate_score():
    rules = load_jrem()["rules"]
    assert len(rules) == 12
    assert [rule["ruleId"] for rule in rules] == [f"JAI-{index:03d}" for index in range(1, 13)]

    for rule in rules:
        assert "score" not in rule
        assert "threshold" not in rule
        assert "score" not in rule["outcome"]
        assert "threshold" not in rule["outcome"]
        if "assurance" in rule["outcome"]:
            assert "score" not in rule["outcome"]["assurance"]
            assert "threshold" not in rule["outcome"]["assurance"]
    for rule in rules:
        assert rule["conditions"] == {}
        assert rule["outcome"]["manualReviewRequired"] is True
        assert rule["outcome"]["assurance"]["evidenceRequired"]


def test_hard_stops_are_non_compensable_and_fail_closed():
    hard_stops = [
        rule for rule in load_jrem()["rules"]
        if rule["outcome"]["assurance"]["controlClass"] == "hard-stop"
    ]
    assert {rule["ruleId"] for rule in hard_stops} == {
        "JAI-001", "JAI-002", "JAI-003", "JAI-004", "JAI-005",
        "JAI-006", "JAI-008", "JAI-009", "JAI-011",
    }
    for rule in hard_stops:
        assert rule["outcome"]["assurance"]["decision"] == "block-until-evidence"
        assert rule["outcome"]["manualReviewRequired"] is True


def test_every_control_source_is_ranked_and_context_only_sources_are_excluded():
    register = load_source_register()
    assert [item["rank"] for item in register["hierarchy"]] == [1, 2, 3, 4, 5]
    source_by_url = {item["url"]: item for item in register["sources"]}
    assert len(source_by_url) == len(register["sources"])
    assert all(item.get("date") or item.get("retrievedOn") for item in register["sources"])

    used_urls = set()
    for rule in load_jrem()["rules"]:
        authorities = set(rule["outcome"]["assurance"]["sourceAuthority"])
        for source_ref in rule["sourceRefs"]:
            assert source_ref["url"] in source_by_url, f"Bron-URL {source_ref['url']} ontbreekt in source-register.json"
            source = source_by_url[source_ref["url"]]
            assert source["class"] != "context-only"
            assert source["class"] in authorities
            assert source_ref["section"]
            assert source_ref.get("bronVersie") or source_ref.get("bronDatum")
            used_urls.add(source_ref["url"])

    case_studies = {
        item["url"] for item in register["sources"]
        if item["usage"] == "case-study-only"
    }
    assert len(case_studies) == 4
    assert used_urls.isdisjoint(case_studies)


def test_composed_domains_exist_and_are_not_duplicated_as_runtime_dependencies():
    available = {item["domain"] for item in list_domains(ROOT / "use-cases")}
    reused = {
        domain
        for rule in load_jrem()["rules"]
        if "assurance" in rule["outcome"]
        for domain in rule["outcome"]["assurance"].get("reusesDomains", [])
    }
    assert reused <= available
    assert {"eu-ai-act", "avg-gdpr", "dpia-model", "traceability"} <= reused
    assert not (USE_CASE / "lib").exists()
