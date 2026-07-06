from sources.bwb_connector import BWBConnector
from sources.plooi_connector import PLOOIConnector
from sources.rechtspraak_connector import RechtspraakConnector
from sources.scheduler import SOURCE_HEALTH_STATUSES


class FakeResponse:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def fake_urlopen(expected_method):
    def _fake_urlopen(request, timeout=10):
        assert request.get_method() == expected_method
        return FakeResponse()

    return _fake_urlopen


def test_bwb_health_uses_public_get_endpoint(monkeypatch):
    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen("GET"))

    result = BWBConnector().health_check()

    assert result["status"] == "ok"
    assert result["checked_url"].endswith("/BWBR0033715")


def test_rechtspraak_health_uses_get_for_atom_feed(monkeypatch):
    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen("GET"))

    result = RechtspraakConnector().health_check()

    assert result["status"] == "ok"
    assert "uitspraken/zoeken?max=1" in result["checked_url"]


def test_plooi_health_is_classified_as_deprecated(monkeypatch):
    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen("GET"))

    result = PLOOIConnector().health_check()

    assert result["status"] == "deprecated"
    assert result["checked_url"] == "https://zoek.officielebekendmakingen.nl"


def test_source_health_status_contract_includes_degraded_and_unsupported_method():
    assert SOURCE_HEALTH_STATUSES == {"ok", "degraded", "deprecated", "unsupported_method", "error"}
