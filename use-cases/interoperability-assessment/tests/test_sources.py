import json
from pathlib import Path


USE_CASE = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict:
    return json.loads((USE_CASE / relative).read_text())


def test_profile_has_authoritative_sources_and_human_publication_boundary():
    sources = {item["id"]: item for item in load("sources/source-register.json")["sources"]}
    profile = load("profiles/interoperability-assessment-2026.json")

    assert sources["EU-INTEROPERABLE-EUROPE-ACT"]["class"] == "binding-law"
    assert all(ref["sourceId"] in sources for aspect in profile["aspects"] for ref in aspect["sourceRefs"])
    publication = next(item for item in profile["aspects"] if item["aspectId"] == "IOPA-04")
    assert "expliciete-menselijke-goedkeuring" in publication["evidenceRequired"]
