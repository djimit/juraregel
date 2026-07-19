"""Tests voor Gemeente Pilot Onboarding Flow."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "cloud" / "lib"))
sys.path.insert(0, str(Path(__file__).parent.parent / "workflows"))

from organisations import OrganisationStore
from gemeente_onboarding import GemeenteOnboarding


@pytest.fixture
def store(tmp_path):
    return OrganisationStore(store_path=tmp_path / "test.json")


@pytest.fixture
def org(store):
    org, key = store.create("Gemeente Test", "burgemeester@test.nl", "pro")
    return org


class TestGemeenteOnboarding:
    def test_init(self, org, store):
        pilot = GemeenteOnboarding(org.org_id, store_path=store.store_path)
        assert pilot.org.name == "Gemeente Test"

    def test_stappen_definieerd(self, org, store):
        pilot = GemeenteOnboarding(org.org_id, store_path=store.store_path)
        assert len(pilot.STAPPEN) == 8

    def test_bia_stap(self, org, store):
        pilot = GemeenteOnboarding(org.org_id, store_path=store.store_path)
        resultaat = pilot.voer_uit("bia")
        assert resultaat["status"] == "complete"
        assert resultaat["processen_totaal"] > 0
        assert resultaat["kritieke_processen"] > 0

    def test_biv_stap(self, org, store):
        pilot = GemeenteOnboarding(org.org_id, store_path=store.store_path)
        resultaat = pilot.voer_uit("biv")
        assert resultaat["status"] == "complete"
        assert resultaat["systemen_totaal"] > 0

    def test_biv_score(self, org, store):
        pilot = GemeenteOnboarding(org.org_id, store_path=store.store_path)
        score = pilot._bereken_biv_score(
            {
                "beschikbaarheid": "zeer_hoog",
                "integriteit": "hoog",
                "vertrouwelijkheid": "zeer_hoog",
            }
        )
        assert score == 11

    def test_risico_stap(self, org, store):
        pilot = GemeenteOnboarding(org.org_id, store_path=store.store_path)
        resultaat = pilot.voer_uit("risico")
        assert resultaat["status"] == "complete"
        assert resultaat["risicos_totaal"] > 0

    def test_risico_strategie(self, org, store):
        pilot = GemeenteOnboarding(org.org_id, store_path=store.store_path)
        pilot.voer_uit("risico")
        risicos = pilot.resultaten["risico"]["details"]
        for r in risicos:
            if r["risico_score"] >= 15:
                assert r["strategie"] == "vermijden"
            elif r["risico_score"] >= 5:
                assert r["strategie"] == "verminderen"

    def test_dpia_verplicht(self, org, store):
        pilot = GemeenteOnboarding(org.org_id, store_path=store.store_path)
        resultaat = pilot.voer_uit(
            "dpia_check", {"gegevens_soorten": ["bijzondere_categorie"]}
        )
        assert resultaat["dpia_verplicht"] is True

    def test_dpia_niet_verplicht(self, org, store):
        pilot = GemeenteOnboarding(org.org_id, store_path=store.store_path)
        resultaat = pilot.voer_uit(
            "dpia_check", {"gegevens_soorten": ["geen_persoonsgegevens"]}
        )
        assert resultaat["dpia_verplicht"] is False

    def test_actieplan(self, org, store):
        pilot = GemeenteOnboarding(org.org_id, store_path=store.store_path)
        pilot.voer_uit("bia")
        pilot.voer_uit("risico")
        pilot.voer_uit("dpia_check")
        resultaat = pilot.voer_uit("actieplan")
        assert resultaat["status"] == "complete"
        assert resultaat["acties_totaal"] > 0

    def test_rapport(self, org, store):
        pilot = GemeenteOnboarding(org.org_id, store_path=store.store_path)
        pilot.voer_uit("bia")
        pilot.voer_uit("biv")
        pilot.voer_uit("risico")
        pilot.voer_uit("dpia_check")
        pilot.voer_uit("actieplan")
        resultaat = pilot.voer_uit("rapport")
        assert resultaat["status"] == "complete"
        assert "compliance_score" in resultaat
        assert 0 <= resultaat["compliance_score"] <= 100

    def test_alles(self, org, store):
        pilot = GemeenteOnboarding(org.org_id, store_path=store.store_path)
        resultaten = pilot.voer_alles_uit()
        assert "bia" in resultaten
        assert "biv" in resultaten
        assert "risico" in resultaten
        assert "actieplan" in resultaten
        assert "rapport" in resultaten
