"""Health check endpoints."""

import logging

from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger(__name__)


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
        "database": _check_database(),
        "vector_store": _check_vector_store(),
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
    except Exception:
        logger.exception("Template readiness check failed")
        return {"status": "error", "message": "Template check failed"}


def _check_database() -> dict:
    # Placeholder — will check PostgreSQL connection
    return {"status": "ok", "message": "Not configured (file mode)"}


def _check_vector_store() -> dict:
    # Placeholder — will check Qdrant connection
    return {"status": "ok", "message": "Not configured (file mode)"}
