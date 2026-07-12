from governance.resolver import check_override


def test_governance_level_alone_never_decides_override():
    result = check_override("eu-ai-act", "algoritmeregister")
    assert result["overrides"] is None
    assert result["decision"] == "requires_legal_analysis"
