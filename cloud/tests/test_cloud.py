"""Tests voor JuraRegel Cloud — Organisations & API Keys."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from organisations import Organisation, OrganisationStore


class TestOrganisation:
    def test_create_organisation(self):
        org = Organisation(
            org_id="test_1", name="Test Org", contact_email="test@example.com"
        )
        assert org.org_id == "test_1"
        assert org.plan == "community"
        assert org.enabled is True

    def test_generate_api_key(self):
        org = Organisation(
            org_id="test_2", name="Test", contact_email="test@example.com"
        )
        key = org.generate_api_key()
        assert key.startswith("jrg_")
        assert len(org.api_keys) == 1

    def test_validate_api_key(self):
        org = Organisation(
            org_id="test_3", name="Test", contact_email="test@example.com"
        )
        key = org.generate_api_key()
        assert org.validate_api_key(key) is True
        assert org.validate_api_key("invalid_key") is False

    def test_rate_limiting(self):
        org = Organisation(
            org_id="test_4",
            name="Test",
            contact_email="test@example.com",
            plan="community",
        )
        assert org.is_within_limits is True
        # Simulate hitting the limit
        org.usage["2026-07"] = {"requests": 1000, "endpoints": {}}
        assert org.is_within_limits is False

    def test_plan_limits(self):
        org = Organisation(
            org_id="test_5",
            name="Test",
            contact_email="test@example.com",
            plan="enterprise",
        )
        assert org.limits["requests_per_month"] == 1_000_000
        assert org.limits["max_api_keys"] == 50

    def test_track_request(self):
        org = Organisation(
            org_id="test_6", name="Test", contact_email="test@example.com"
        )
        org.track_request("/v1/bio2/calculate")
        org.track_request("/v1/bio2/calculate")
        month = "2026-07"
        assert org.usage[month]["requests"] == 2
        assert org.usage[month]["endpoints"]["/v1/bio2/calculate"] == 2


class TestOrganisationStore:
    def test_create_and_get(self, tmp_path):
        store = OrganisationStore(store_path=tmp_path / "test.json")
        org, key = store.create("Gemeente Test", "burgemeester@test.nl", "pro")
        assert org.name == "Gemeente Test"
        assert key.startswith("jrg_")

        fetched = store.get(org.org_id)
        assert fetched is not None
        assert fetched.name == "Gemeente Test"

    def test_get_by_api_key(self, tmp_path):
        store = OrganisationStore(store_path=tmp_path / "test.json")
        org, key = store.create("Test Org", "test@test.nl")
        fetched = store.get_by_api_key(key)
        assert fetched is not None
        assert fetched.org_id == org.org_id

    def test_list_all(self, tmp_path):
        store = OrganisationStore(store_path=tmp_path / "test.json")
        store.create("Org 1", "a@test.nl")
        store.create("Org 2", "b@test.nl")
        assert len(store.list_all()) == 2
