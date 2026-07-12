from ci.source_quality import issues_for_rule


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
