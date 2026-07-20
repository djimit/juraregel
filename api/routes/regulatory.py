"""Regulatory Monitor API — Automated legal change detection."""

from fastapi import APIRouter, Query
from typing import Any

from ..regulatory_monitor import regulatory_monitor

router = APIRouter()


@router.get("/")
async def regulatory_status():
    """Get regulatory monitor status."""
    return {
        "status": "active",
        "sources": [s.source for s in regulatory_monitor.scrapers],
        "total_changes": len(regulatory_monitor._changes),
        "scan_history": len(regulatory_monitor._scan_history),
    }


@router.post("/scan")
async def trigger_scan():
    """Trigger a scan of all regulatory sources."""
    results = regulatory_monitor.scan_all()
    return {
        "scanned_at": results[0].scanned_at if results else None,
        "sources_scanned": len(results),
        "total_changes": sum(r.changes_detected for r in results),
        "results": [
            {
                "source": r.source,
                "changes_detected": r.changes_detected,
                "errors": r.errors,
                "execution_time_ms": r.execution_time_ms,
            }
            for r in results
        ],
    }


@router.get("/changes")
async def get_changes(
    limit: int = Query(50, ge=1, le=200),
    framework: str | None = None,
    critical_only: bool = False,
):
    """Get detected regulatory changes."""
    if framework:
        changes = regulatory_monitor.get_changes_by_framework(framework)
    elif critical_only:
        changes = regulatory_monitor.get_critical_changes()
    else:
        changes = regulatory_monitor.get_recent_changes(limit)

    return {
        "count": len(changes),
        "changes": [
            {
                "id": c.id,
                "source": c.source,
                "type": c.change_type.value,
                "title": c.title,
                "summary": c.summary,
                "url": c.url,
                "impact_level": c.impact_level.value,
                "impact_score": c.impact_score,
                "affected_frameworks": c.affected_frameworks,
                "affected_articles": c.affected_articles,
                "detected_at": c.detected_at,
            }
            for c in changes
        ],
    }


@router.get("/impact/{change_id}")
async def get_impact(change_id: str):
    """Get impact analysis for a specific change."""
    for change in regulatory_monitor._changes:
        if change.id == change_id:
            return {
                "change_id": change.id,
                "title": change.title,
                "impact_level": change.impact_level.value,
                "impact_score": change.impact_score,
                "affected_frameworks": change.affected_frameworks,
                "affected_articles": change.affected_articles,
            }
    return {"error": "Change not found"}


@router.get("/history")
async def get_scan_history(limit: int = Query(10, ge=1, le=50)):
    """Get scan history."""
    history = regulatory_monitor.get_scan_history(limit)
    return {
        "count": len(history),
        "history": [
            {
                "source": h.source,
                "scanned_at": h.scanned_at,
                "changes_detected": h.changes_detected,
                "errors": h.errors,
                "execution_time_ms": h.execution_time_ms,
            }
            for h in history
        ],
    }
