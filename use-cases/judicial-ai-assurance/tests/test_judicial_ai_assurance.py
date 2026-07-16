import copy
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
DEMO_DIR = USE_CASE / "demo"
DEMO_OUTPUT_PATH = ROOT / "playground" / "judicial-ai-demo.json"

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


def load_demo_module():
    module_path = DEMO_DIR / "admission_gate.py"
    spec = importlib.util.spec_from_file_location("judicial_ai_admission_gate", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_adapter_module():
    module_path = DEMO_DIR / "evidence_adapter.py"
    spec = importlib.util.spec_from_file_location("judicial_ai_evidence_adapter", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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


def test_admission_demo_is_deterministic_non_scoring_and_schema_valid():
    module = load_demo_module()
    generated = module.build_demo(JREM_PATH, DEMO_DIR / "scenarios.json")
    committed = json.loads(DEMO_OUTPUT_PATH.read_text())
    schema = json.loads((DEMO_DIR / "evidence-bundle.schema.json").read_text())

    assert generated == committed
    jsonschema.Draft202012Validator(schema).validate(generated)
    assert [item["status"] for item in generated["scenarios"]] == [
        "review-required", "blocked", "blocked"
    ]
    assert generated["profile"]["hardStopCount"] == 9
    assert "score" not in json.dumps(generated).lower()


def test_admission_demo_requires_matching_human_final_decision():
    module = load_demo_module()
    profile = load_jrem()
    scenarios = json.loads((DEMO_DIR / "scenarios.json").read_text())
    scenario = copy.deepcopy(scenarios["scenarios"][0])

    scenario["humanDecision"] = {
        "decision": "approved",
        "profileVersion": "2025.1",
        "actor": "independent-reviewer",
        "role": "jurist",
        "reason": "synthetic test only"
    }
    wrong_version = module.evaluate_scenario(profile, scenarios["commonEvidence"], scenario)
    assert wrong_version["status"] == "review-required"

    scenario["humanDecision"]["profileVersion"] = profile["version"]
    approved = module.evaluate_scenario(profile, scenarios["commonEvidence"], scenario)
    assert approved["status"] == "conditionally-admissible"

    scenario["humanDecision"]["actor"] = ""
    incomplete_approval = module.evaluate_scenario(profile, scenarios["commonEvidence"], scenario)
    assert incomplete_approval["status"] == "review-required"


def test_admission_demo_fails_closed_without_hard_stop_evidence():
    module = load_demo_module()
    profile = load_jrem()
    scenarios = json.loads((DEMO_DIR / "scenarios.json").read_text())
    common = [
        item for item in scenarios["commonEvidence"]
        if "source-hash" not in item["artifactTypes"]
    ]
    result = module.evaluate_scenario(profile, common, scenarios["scenarios"][0])

    assert result["status"] == "blocked"
    jai_006 = next(item for item in result["controls"] if item["controlId"] == "JAI-006")
    assert jai_006["status"] == "blocked"
    assert "source-hash" in jai_006["missingEvidence"]


def test_required_evidence_failure_cannot_auto_approve_but_is_not_a_hard_stop():
    module = load_demo_module()
    profile = load_jrem()
    scenarios = json.loads((DEMO_DIR / "scenarios.json").read_text())
    scenario = copy.deepcopy(scenarios["scenarios"][0])
    scenario["evidence"] = [{
        "sourceSystem": "openmythos",
        "status": "failed",
        "artifactRef": "demo://security/failure",
        "summary": "Synthetic security test failure.",
        "artifactTypes": ["indirect-prompt-injection-tests"]
    }]

    result = module.evaluate_scenario(profile, scenarios["commonEvidence"], scenario)
    jai_010 = next(item for item in result["controls"] if item["controlId"] == "JAI-010")
    assert jai_010["status"] == "review-required"
    assert jai_010["failedEvidence"] == ["indirect-prompt-injection-tests"]
    assert result["status"] == "review-required"


def test_static_demo_uses_generated_pack_without_simulating_human_approval():
    html = (ROOT / "playground" / "judicial-ai.html").read_text()
    index = (ROOT / "playground" / "index.html").read_text()

    assert 'fetch("judicial-ai-demo.json")' in html
    assert "humanDecision" not in html
    assert ".innerHTML" not in html
    assert 'href="judicial-ai.html"' in index


def test_openmythos_adapter_preserves_negative_oracle_evidence():
    adapter = load_adapter_module()
    fixtures = DEMO_DIR / "fixtures"
    record = adapter.adapt_openmythos(
        fixtures / "openmythos-run.jsonl",
        fixtures / "openmythos-oracle.jsonl",
        "fixture-openmythos-run",
    )

    assert record["sourceSystem"] == "openmythos"
    assert record["status"] == "failed"
    assert record["runId"] == "fixture-openmythos-run"
    assert record["artifactTypes"] == [
        "independent-evaluation", "indirect-prompt-injection-tests"
    ]
    assert record["artifactHash"].startswith("sha256:")
    assert "1 oracle failures" in record["summary"]


def test_openmythos_adapter_rejects_an_oracle_for_an_unknown_case(tmp_path):
    adapter = load_adapter_module()
    fixtures = DEMO_DIR / "fixtures"
    unknown_oracle = tmp_path / "oracle.jsonl"
    unknown_oracle.write_text(
        '{"case_id":"unknown-001","oracle_applicable":true,"oracle_pass":true}\n'
    )

    try:
        adapter.adapt_openmythos(fixtures / "openmythos-run.jsonl", unknown_oracle)
    except ValueError as error:
        assert "unknown run cases" in str(error)
    else:
        raise AssertionError("Unknown oracle case was accepted")


def test_djimitflo_adapter_does_not_turn_a_score_into_admission():
    adapter = load_adapter_module()
    record = adapter.adapt_djimitflo(DEMO_DIR / "fixtures" / "djimitflo-run.json")

    assert record["sourceSystem"] == "djimitflo"
    assert record["status"] == "observed"
    assert record["runId"] == "6a6f2ca0-370f-460e-94b4-cfa660cfa1b1"
    assert "overall_score" not in record
    assert "score" not in record["summary"].lower()
    assert "deepseek-v4-pro:cloud" in record["summary"]

    normalized = load_demo_module().normalise_evidence([record])[0]
    bundle_schema = json.loads((DEMO_DIR / "evidence-bundle.schema.json").read_text())
    evidence_schema = {
        "$schema": bundle_schema["$schema"],
        "$defs": bundle_schema["$defs"],
        **bundle_schema["properties"]["scenarios"]["items"]["properties"]["evidence"]["items"],
    }
    jsonschema.Draft202012Validator(evidence_schema).validate(normalized)
