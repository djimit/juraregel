import json
from pathlib import Path


USE_CASE = Path(__file__).resolve().parents[1]


def load(relative: str) -> dict:
    return json.loads((USE_CASE / relative).read_text())


def test_eudi_sources_separate_law_from_technical_evidence():
    sources = {item["id"]: item for item in load("sources/source-register.json")["sources"]}

    assert sources["EIDAS-2024-1183"]["class"] == "binding-law"
    assert sources["EUDI-ARF-3.0.0"]["release"] == "3.0.0"
    assert sources["EUDI-ARF-3.0.0"]["class"] == "authoritative-technical-framework"
    assert sources["EUDI-TECHNICAL-SPECIFICATIONS"]["retrievedOn"] == "2026-08-28"


def test_wallet_rules_use_versioned_arf_as_supporting_source():
    rules = {item["ruleId"]: item for item in load("jrem/exports/eidas-2026.2.json")["rules"]}
    arf_url = "https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/releases/tag/v3.0.0"

    for rule_id in ("EID-008", "EID-032"):
        refs = rules[rule_id]["sourceRefs"]
        arf = next(ref for ref in refs if ref["url"] == arf_url)
        assert arf["bronVersie"] == "2026-07-21"
        assert arf["type"] == "standaard"
