import json
from pathlib import Path


USE_CASE = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict:
    return json.loads((USE_CASE / relative).read_text())


def keys(value):
    if isinstance(value, dict):
        return set(value) | {key for item in value.values() for key in keys(item)}
    if isinstance(value, list):
        return {key for item in value for key in keys(item)}
    return set()


def test_gpai_profile_is_non_scoring_and_source_complete():
    register = load("sources/source-register.json")
    profile = load("profiles/gpai-implementation-2026.json")
    sources = {item["id"]: item for item in register["sources"]}

    assert sources["EU-AI-ACT"]["class"] == "binding-law"
    assert sources["EU-GPAI-CODE"]["class"] == "voluntary-compliance-method"
    assert len(profile["aspects"]) == 4
    assert not {"score", "weight", "threshold"} & keys(profile)
    for aspect in profile["aspects"]:
        assert aspect["evidenceRequired"]
        assert aspect["prohibitedInference"]
        assert all(ref["sourceId"] in sources and ref["section"] for ref in aspect["sourceRefs"])
