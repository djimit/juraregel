from pathlib import Path

from fastapi.testclient import TestClient

from shared import api_base


def test_auth_middleware_covers_catalog_and_custom_routes(monkeypatch):
    monkeypatch.setattr(api_base, "AUTH_ENABLED", True)
    monkeypatch.setenv("JURAREGEL_API_KEY", "secret")
    jrem = Path(__file__).parents[1] / "use-cases" / "griffierecht" / "jrem" / "exports"
    client = TestClient(api_base.create_app("griffierecht", jrem, 8490, calculate_capability=True))

    assert client.get("/v1/griffierecht/versions").status_code == 401
    assert client.get(
        "/v1/griffierecht/versions", headers={"Authorization": "Bearer secret"}
    ).status_code == 200
