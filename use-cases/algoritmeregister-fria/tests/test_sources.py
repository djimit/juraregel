import json
from pathlib import Path


USE_CASE = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict:
    return json.loads((USE_CASE / relative).read_text())


def test_primary_law_is_separated_from_guidance_and_methods():
    sources = {item["id"]: item for item in load("sources/source-register.json")["sources"]}

    assert sources["EU-AI-ACT"]["class"] == "binding-law"
    assert sources["ALGORITMEKADER-2.5"]["class"] == "authoritative-implementation-guidance"
    assert sources["ALGORITMEREGISTER-BZK-01"]["class"] == "authoritative-policy"
    assert sources["IAMA-2026"]["class"] == "implementation-method"
    assert all(item["version"] and item["url"].startswith("https://") for item in sources.values())


def test_rules_use_registered_urls_for_national_guidance():
    register = load("sources/source-register.json")
    ruleset = load("jrem/exports/algoritmeregister-fria-2026.1.json")
    registered = {item["url"] for item in register["sources"]}
    national = {
        ref["url"]
        for rule in ruleset["rules"]
        for ref in rule["sourceRefs"]
        if "algoritmes.overheid.nl" in ref.get("url", "")
    }

    assert national
    assert national <= registered
