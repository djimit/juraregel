import json

from ci.source_quality import audit, issues_for_rule


def test_reproducible_source_anchor_passes():
    rule = {"ruleId": "R-1", "sourceRefs": [{
        "type": "wet", "title": "Wet", "section": "art. 1 lid 2",
        "url": "https://example.test/BWBR0000001/2026-01-01",
        "bwbId": "BWBR0000001", "bronVersie": "2026-01-01",
    }]}
    assert issues_for_rule(rule, {}) == []


def test_internal_rule_id_is_not_a_legal_anchor():
    rule = {"ruleId": "R-1", "sourceRefs": [{"type": "wet", "title": "Wet", "section": "R-1"}]}
    issues = issues_for_rule(rule, {})
    assert any("exact legal anchor" in issue for issue in issues)
    assert any("BWB/CELEX/ELI" in issue for issue in issues)


def test_canonical_eli_and_bwb_urls_are_reproducible_legal_identifiers():
    for url in (
        "https://eur-lex.europa.eu/eli/reg/2024/1689",
        "https://wetten.overheid.nl/BWBR0045754/2024-01-01",
    ):
        rule = {"ruleId": "R-1", "sourceRefs": [{
            "type": "wet",
            "title": "Wet",
            "section": "Artikel 1",
            "url": url,
            "bronDatum": "2024-01-01",
        }]}
        assert issues_for_rule(rule, {}) == []


def test_ruleset_identifier_does_not_mask_a_different_source():
    rule = {"ruleId": "R-1", "sourceRefs": [{
        "type": "wet", "title": "Andere wet", "section": "Artikel 1",
        "url": "https://example.test/wet", "bronVersie": "2026-01-01",
    }]}
    issues = issues_for_rule(rule, {"bwbId": "BWBR0000001"})
    assert any("BWB/CELEX/ELI" in issue for issue in issues)


def test_living_non_legal_source_can_use_retrieval_date():
    rule = {"ruleId": "R-1", "sourceRefs": [{
        "type": "standaard", "title": "Levende bron", "section": "Onderdeel A",
        "url": "https://example.test/source", "retrievedOn": "2026-08-28",
    }]}
    assert issues_for_rule(rule, {}) == []


def test_generic_legal_homepage_is_not_a_reproducible_url():
    rule = {"ruleId": "R-1", "sourceRefs": [{
        "type": "wetsartikel", "title": "Wet", "section": "Artikel 1",
        "url": "https://wetten.overheid.nl/", "bwbId": "BWBR0000001",
        "bronVersie": "2026-01-01",
    }]}
    assert any("missing url" in issue for issue in issues_for_rule(rule, {}))


def test_source_debt_cannot_exceed_baseline(tmp_path):
    export = tmp_path / "use-cases/demo/jrem/exports/demo.json"
    export.parent.mkdir(parents=True)
    export.write_text(json.dumps({"rules": [{
        "ruleId": "R-1", "sourceRefs": [{"type": "wet", "section": "R-1"}],
    }]}))
    baseline = tmp_path / "baseline.json"
    baseline.write_text(json.dumps({str(export.relative_to(tmp_path)): 4}))
    assert audit(tmp_path, baseline)["regressions"] == []

    baseline.write_text(json.dumps({str(export.relative_to(tmp_path)): 3}))
    assert audit(tmp_path, baseline)["regressions"]
