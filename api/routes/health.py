"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Service health check."""
    return {
        "status": "healthy",
        "service": "juraregel-api",
        "version": "1.0.0",
    }


@router.get("/ready")
async def readiness_check():
    """Readiness probe — checks all dependencies."""
    checks = {
        "templates": _check_templates(),
        "database": await _check_database(),
        "vector_store": await _check_vector_store(),
    }
    all_ready = all(c["status"] == "ok" for c in checks.values())
    return {
        "ready": all_ready,
        "checks": checks,
    }


def _check_templates() -> dict:
    try:
        from docs.templates import list_documents

        count = len(list_documents())
        return {"status": "ok", "template_count": count}
    except Exception as e:
        return {"status": "error", "message": str(e)}


async def _check_database() -> dict:
    from ..database import IS_POSTGRES, USE_DATABASE, engine

    if not USE_DATABASE:
        return {"status": "unavailable", "message": "DATABASE_URL not configured"}
    if not IS_POSTGRES:
        return {"status": "degraded", "message": "Non-PostgreSQL development backend"}
    if engine is None:
        return {"status": "error", "message": "PostgreSQL engine unavailable"}
    try:
        import sqlalchemy

        async with engine.connect() as connection:
            await connection.execute(sqlalchemy.text("SELECT 1"))
        return {"status": "ok", "message": "PostgreSQL reachable"}
    except Exception as exc:
        return {"status": "error", "message": type(exc).__name__}


async def _check_vector_store() -> dict:
    import os

    qdrant_url = os.getenv("QDRANT_URL", "")
    if not qdrant_url:
        return {"status": "unavailable", "message": "QDRANT_URL not configured"}
    try:
        import httpx

        async with httpx.AsyncClient(timeout=2) as client:
            response = await client.get(f"{qdrant_url.rstrip('/')}/collections")
            response.raise_for_status()
        return {"status": "ok", "message": "Qdrant reachable"}
    except Exception as exc:
        return {"status": "error", "message": type(exc).__name__}
