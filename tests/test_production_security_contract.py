import asyncio
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api import auth, main
from api.middleware import AuthMiddleware


def production_environment(monkeypatch):
    monkeypatch.setattr(main, "PRODUCTION", True)
    monkeypatch.setenv(
        "DATABASE_URL", "postgresql+asyncpg://service:secret@db.invalid/juraregel"
    )
    monkeypatch.setenv("KEYCLOAK_URL", "https://identity.invalid")
    monkeypatch.setenv("QDRANT_URL", "https://qdrant.invalid")
    monkeypatch.setenv("JURAREGEL_CORS_ORIGINS", "https://juraregel.invalid")
    monkeypatch.setenv("JURAREGEL_RATE_LIMIT_MODE", "ingress")


def test_production_configuration_fails_closed(monkeypatch):
    monkeypatch.setattr(main, "PRODUCTION", True)
    for name in (
        "DATABASE_URL",
        "KEYCLOAK_URL",
        "QDRANT_URL",
        "JURAREGEL_CORS_ORIGINS",
        "JURAREGEL_RATE_LIMIT_MODE",
    ):
        monkeypatch.delenv(name, raising=False)

    with pytest.raises(RuntimeError, match="production configuration missing"):
        main.validate_runtime_config()


def test_production_configuration_accepts_explicit_secure_boundaries(monkeypatch):
    production_environment(monkeypatch)
    main.validate_runtime_config()


def test_unsigned_local_token_and_embedded_api_key_are_rejected(monkeypatch):
    monkeypatch.setattr(auth, "JWT_SECRET", "")
    monkeypatch.delenv("JURAREGEL_API_KEYS_JSON", raising=False)

    assert auth.verify_token("unsigned-payload") is None
    assert auth.verify_api_key("test-key-123") is None
    assert asyncio.run(auth.authenticate("Bearer unsigned-payload")) is None


def test_auth_middleware_rejects_invalid_and_accepts_configured_service_key(
    monkeypatch,
):
    test_app = FastAPI()
    test_app.add_middleware(AuthMiddleware)

    @test_app.get("/protected")
    async def protected():
        return {"ok": True}

    client = TestClient(test_app)
    assert client.get("/protected").status_code == 401
    monkeypatch.setenv(
        "JURAREGEL_API_KEYS_JSON",
        '{"approved-key":{"name":"ci","roles":["reader"]}}',
    )
    response = client.get(
        "/protected", headers={"Authorization": "ApiKey approved-key"}
    )
    assert response.status_code == 200


def test_production_rejects_process_local_rate_limiting(monkeypatch):
    production_environment(monkeypatch)
    monkeypatch.setenv("JURAREGEL_RATE_LIMIT_MODE", "in_memory")

    with pytest.raises(RuntimeError, match="approved ingress"):
        main.validate_runtime_config()


def test_process_local_record_routes_are_not_in_production_surface():
    source = Path(main.__file__).read_text()
    assert "if not PRODUCTION:\n    app.include_router(\n        assessments.router" in source
