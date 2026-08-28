import json
from pathlib import Path


USE_CASE = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict:
    return json.loads((USE_CASE / relative).read_text())


def test_case_law_profile_routes_only_to_primary_databases():
    sources = {item["id"]: item for item in load("sources/source-register.json")["sources"]}
    profile = load("profiles/european-case-law-evidence-2026.json")

    assert all(item["class"] == "primary-case-law-database" for item in sources.values())
    assert all(route["sourceId"] in sources for route in profile["sourceRouting"])
    assert {"decisionStatus", "paragraphOrSection", "translationStatus"} <= set(profile["requiredRecord"])
