"""API Middleware — Rate limiting, tenant isolation, auth."""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
from collections import defaultdict


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiter."""

    def __init__(self, app, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self._requests: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        # Clean old entries
        self._requests[client_ip] = [
            t for t in self._requests[client_ip] if now - t < 60
        ]

        if len(self._requests[client_ip]) >= self.requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded", "retry_after": 60},
            )

        self._requests[client_ip].append(now)
        response = await call_next(request)
        return response


class TenantMiddleware(BaseHTTPMiddleware):
    """Extract tenant ID from header and set context."""

    async def dispatch(self, request: Request, call_next):
        # Skip for health checks and docs
        if request.url.path in ("/health", "/ready", "/docs", "/openapi.json", "/"):
            return await call_next(request)

        tenant_id = request.headers.get("X-Tenant-ID")
        if tenant_id:
            request.state.tenant_id = tenant_id

        response = await call_next(request)
        return response


class AuthMiddleware(BaseHTTPMiddleware):
    """OAuth2 Bearer token validation (placeholder for Keycloak integration)."""

    def __init__(self, app, exclude_paths: set[str] | None = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or {
            "/health",
            "/ready",
            "/docs",
            "/openapi.json",
            "/",
            "/auth/token",
        }

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            raise HTTPException(
                status_code=401, detail="Missing or invalid authorization header"
            )

        token = auth.replace("Bearer ", "")
        # Placeholder — validate against Keycloak
        # For now, accept any non-empty token
        if not token:
            raise HTTPException(status_code=401, detail="Invalid token")

        request.state.user = {"token": token, "roles": ["compliance_officer"]}
        response = await call_next(request)
        return response
