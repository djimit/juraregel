from sources.preflight_spikes import get_preflight_source, list_preflight_sources


def test_preflight_spikes_cover_planned_followup_use_cases():
    sources = list_preflight_sources()
    use_cases = {s["useCase"] for s in sources}

    assert "decentrale-regelcheck" in use_cases
    assert "woo-publicatieplicht-preflight" in use_cases
    assert "digitale-dienst-compliance-check" in use_cases
    assert "sttr-preflight" in use_cases
    assert "interoperability-assessment-builder" in use_cases


def test_preflight_spikes_have_urls_and_manual_boundaries():
    for source in list_preflight_sources():
        assert source["urls"]
        assert source["manualReviewBoundary"]


def test_get_preflight_source_by_id():
    source = get_preflight_source("sttr-rtr")
    assert source["useCase"] == "sttr-preflight"
