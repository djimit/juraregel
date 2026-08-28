import json
from pathlib import Path


USE_CASE = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict:
    return json.loads((USE_CASE / relative).read_text())


def test_foreign_and_interchange_sources_remain_pilot_only():
    sources = {item["id"]: item for item in load("sources/source-register.json")["sources"]}
    profile = load("profiles/comparative-methods-2026.json")

    assert profile["interpretationStatus"] == "pilot-only"
    assert all(source_id in sources for pilot in profile["pilots"] for source_id in pilot["sourceIds"])
    assert all(pilot["promotionEvidence"] and pilot["prohibitedUse"] for pilot in profile["pilots"])
    assert not any(item["class"] == "binding-law" for item in sources.values())
