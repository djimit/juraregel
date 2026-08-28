import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
USE_CASE = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "evidence_assess",
    ROOT / "use-cases" / "acict-assurance" / "assess.py",
)
assess = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assess)


def load(relative: str) -> dict:
    return json.loads((USE_CASE / relative).read_text())


def keys(value):
    if isinstance(value, dict):
        return set(value) | {key for item in value.values() for key in keys(item)}
    if isinstance(value, list):
        return {key for item in value for key in keys(item)}
    return set()


def test_sources_are_versioned_and_current_policy_replaces_historical_baseline():
    register = load("sources/source-register.json")
    sources = {item["sourceId"]: item for item in register["sources"]}

    assert len(sources) == 5
    assert sources["rijk-mjp-2024-2025"]["status"] == "superseded"
    assert sources["rijk-mjp-2026-2030"]["status"] == "current"
    assert all(len(item["sha256"]) == 64 for item in sources.values())
    assert all(item["url"].startswith("https://") for item in sources.values())


def test_profile_is_anchored_non_scoring_and_fails_closed_without_evidence():
    register = load("sources/source-register.json")
    profile = load("profiles/rijk-ihh-2026.json")
    source_ids = {item["sourceId"] for item in register["sources"]}

    assert len(profile["aspects"]) == 10
    assert "score" not in keys(profile)
    for aspect in profile["aspects"]:
        assert aspect["sourceRefs"]
        assert all(ref["sourceId"] in source_ids for ref in aspect["sourceRefs"])
        assert all(ref["section"] and ref["pages"] for ref in aspect["sourceRefs"])
        assert aspect["evidenceRequired"]
        assert aspect["falsifiedBy"]
        assert aspect["prohibitedInference"]

    result = assess.evaluate(
        profile,
        {
            "profileId": profile["profileId"],
            "profileVersion": profile["version"],
            "assessmentId": "empty-proof",
            "findings": [],
        },
    )
    assert result["status"] == "evidence-incomplete"
    assert result["incompleteAspects"] == [item["aspectId"] for item in profile["aspects"]]
