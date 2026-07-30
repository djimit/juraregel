"""Authentication — OAuth2 / JWT with multi-backend support.

Supports:
- Keycloak (production, full OAuth2/OIDC)
- Local JWT (development, no external dependencies)
- API Key (service-to-service)

Auto-selects backend based on KEYCLOAK_URL environment variable.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
# ─── Configuration ──────────────────────────────────────────────

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "juraregel")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "juraregel-api")
USE_KEYCLOAK = bool(KEYCLOAK_URL)

# Local JWT is development-only and requires an explicit secret.
JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24


# ─── Models ──────────────────────────────────────────────────


@dataclass
class User:
    """Authenticated user."""

    id: str
    username: str
    email: str
    roles: list[str]
    tenant_id: str | None = None


# ─── Local JWT (Development) ─────────────────────────────────


def create_token(
    user_id: str, username: str, roles: list[str], tenant_id: str | None = None
) -> str:
    """Create a local JWT token."""
    try:
        import jwt
    except ImportError as exc:
        raise RuntimeError("PyJWT is required to create signed tokens") from exc
    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET is required for local JWT")

    payload = {
        "sub": user_id,
        "username": username,
        "roles": roles,
        "tenant_id": tenant_id,
        "exp": int(time.time()) + JWT_EXPIRY_HOURS * 3600,
        "iat": int(time.time()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> User | None:
    """Verify a JWT token and return the user."""
    if not JWT_SECRET:
        return None
    try:
        import jwt

        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return User(
            id=payload.get("sub", ""),
            username=payload.get("username", ""),
            email=payload.get("email", ""),
            roles=payload.get("roles", []),
            tenant_id=payload.get("tenant_id"),
        )
    except Exception:
        return None


# ─── Keycloak (Production) ───────────────────────────────────


class KeycloakAuth:
    """Keycloak OAuth2/OIDC authentication."""

    def __init__(self):
        self.url = KEYCLOAK_URL
        self.realm = KEYCLOAK_REALM
        self.client_id = KEYCLOAK_CLIENT_ID
        self._jwks = None

    def get_well_known_url(self) -> str:
        return f"{self.url}/realms/{self.realm}/.well-known/openid-configuration"

    def get_jwks(self) -> dict:
        if self._jwks is None:
            import httpx

            resp = httpx.get(
                f"{self.url}/realms/{self.realm}/protocol/openid-connect/certs"
            )
            self._jwks = resp.json()
        return self._jwks

    def verify_token(self, token: str) -> User | None:
        """Verify a Keycloak JWT token."""
        try:
            import jwt
            from jwt import PyJWKClient

            jwks_url = f"{self.url}/realms/{self.realm}/protocol/openid-connect/certs"
            jwks_client = PyJWKClient(jwks_url)
            signing_key = jwks_client.get_signing_key_from_jwt(token)

            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self.client_id,
            )

            return User(
                id=payload.get("sub", ""),
                username=payload.get("preferred_username", ""),
                email=payload.get("email", ""),
                roles=payload.get("realm_access", {}).get("roles", []),
                tenant_id=payload.get("tenant_id"),
            )
        except Exception:
            return None


# ─── API Key Auth (Service-to-Service) ───────────────────────

def configured_api_keys() -> dict[str, dict]:
    """Load service credentials from an explicit JSON environment value."""
    raw = os.getenv("JURAREGEL_API_KEYS_JSON", "")
    if not raw:
        return {}
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("JURAREGEL_API_KEYS_JSON must contain an object")
    return value


def verify_api_key(api_key: str) -> User | None:
    """Verify an API key."""
    key_data = configured_api_keys().get(api_key)
    if key_data:
        return User(
            id=f"service-{key_data['name']}",
            username=key_data["name"],
            email="",
            roles=key_data["roles"],
            tenant_id=key_data.get("tenant_id"),
        )
    return None


# ─── Unified Auth ─────────────────────────────────────────────


async def authenticate(authorization: str | None) -> User | None:
    """Authenticate a request (Bearer token or API key)."""
    if not authorization:
        return None

    if authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
        if USE_KEYCLOAK:
            kc = KeycloakAuth()
            return kc.verify_token(token)
        return verify_token(token)

    if authorization.startswith("ApiKey "):
        api_key = authorization.replace("ApiKey ", "")
        return verify_api_key(api_key)

    return None


def require_role(user: User, role: str) -> bool:
    """Check if a user has a required role."""
    return role in user.roles or "admin" in user.roles
