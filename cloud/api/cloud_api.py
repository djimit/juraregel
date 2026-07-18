"""JuraRegel Cloud API — Multi-tenant compliance platform.

Endpoints:
  POST /v1/cloud/organisations — Registreer organisatie
  GET  /v1/cloud/organisations/{org_id} — Org details
  POST /v1/cloud/organisations/{org_id}/keys — Genereer API key
  GET  /v1/cloud/organisations/{org_id}/usage — Usage stats
  GET  /v1/cloud/organisations/{org_id}/compliance — Compliance scores
  GET  /v1/cloud/health — Health check
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from fastapi import FastAPI, HTTPException, Header
from api_base import create_app

from organisations import get_store, Organisation

app = FastAPI(
    title="JuraRegel Cloud",
    description="Multi-tenant compliance platform",
    version="1.0.0",
)

# ─── Framework compliance scores ────────────────────────────
FRAMEWORK_SCORES = {
    "bio2": {"port": 8494, "total_rules": 162, "name": "BIO2"},
    "eidas": {"port": 8523, "total_rules": 32, "name": "eIDAS 2.0"},
    "eu-ai-act": {"port": 8498, "total_rules": 12, "name": "EU AI Act"},
    "avg-gdpr": {"port": 8499, "total_rules": 10, "name": "AVG/GDPR"},
    "nis2": {"port": 8501, "total_rules": 32, "name": "NIS2"},
    "nora": {"port": 8497, "total_rules": 15, "name": "NORA"},
    "ncsc": {"port": 8500, "total_rules": 32, "name": "NCSC"},
    "iso27001": {"port": 8526, "total_rules": 28, "name": "ISO 27001"},
    "dpia-generator": {"port": 8525, "total_rules": 51, "name": "DPIA Generator"},
    "bia-biv-dpia": {"port": 8524, "total_rules": 32, "name": "BIA-BIV-DPIA"},
    "forumstandaardisatie": {
        "port": 8495,
        "total_rules": 22,
        "name": "Forum Standaardisatie",
    },
    "overheidsstandaarden": {
        "port": 8496,
        "total_rules": 24,
        "name": "Overheidsstandaarden",
    },
    "algoritmeregister": {"port": 8508, "total_rules": 20, "name": "Algoritmeregister"},
}


def verify_api_key(x_api_key: str | None = Header(None)) -> Organisation:
    """Verify API key from header."""
    if not x_api_key:
        raise HTTPException(
            status_code=401, detail="API key required (X-API-Key header)"
        )
    org = get_store().get_by_api_key(x_api_key)
    if not org:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if not org.enabled:
        raise HTTPException(status_code=403, detail="Organisation disabled")
    if not org.is_within_limits:
        raise HTTPException(status_code=429, detail="Monthly request limit reached")
    return org


# ─── Endpoints ──────────────────────────────────────────────


@app.post("/v1/cloud/organisations")
def create_organisation(name: str, contact_email: str, plan: str = "community"):
    """Registreer een nieuwe organisatie."""
    store = get_store()
    org, api_key = store.create(name, contact_email, plan)
    return {
        "organisation": org.to_dict(),
        "api_key": api_key,
        "message": "Bewaar deze API key — hij wordt niet opnieuw getoond",
    }


@app.get("/v1/cloud/organisations/{org_id}")
def get_organisation(org_id: str, org: Organisation = verify_api_key):
    """Haal organisatie details op."""
    target = get_store().get(org_id)
    if not target:
        raise HTTPException(status_code=404, detail="Organisation not found")
    return target.to_dict()


@app.post("/v1/cloud/organisations/{org_id}/keys")
def generate_key(
    org_id: str, name: str = "new-key", org: Organisation = verify_api_key
):
    """Genereer een nieuwe API key."""
    target = get_store().get(org_id)
    if not target:
        raise HTTPException(status_code=404, detail="Organisation not found")
    new_key = target.generate_api_key(name)
    get_store().update(target)
    return {"api_key": new_key, "name": name}


@app.get("/v1/cloud/organisations/{org_id}/usage")
def get_usage(org_id: str, org: Organisation = verify_api_key):
    """Haal usage statistieken op."""
    target = get_store().get(org_id)
    if not target:
        raise HTTPException(status_code=404, detail="Organisation not found")
    return {
        "org_id": target.org_id,
        "plan": target.plan,
        "limits": target.limits,
        "current_month_requests": target.current_month_usage,
        "remaining_requests": max(
            0, target.limits["requests_per_month"] - target.current_month_usage
        ),
        "usage_history": target.usage,
    }


@app.get("/v1/cloud/organisations/{org_id}/compliance")
def get_compliance(org_id: str, org: Organisation = verify_api_key):
    """Haal compliance scores per framework op."""
    target = get_store().get(org_id)
    if not target:
        raise HTTPException(status_code=404, detail="Organisation not found")

    # Track this request
    org.track_request("/compliance")
    get_store().update(org)

    return {
        "org_id": target.org_id,
        "org_name": target.name,
        "generated_at": target.created_at,
        "frameworks": FRAMEWORK_SCORES,
        "total_rules_available": sum(
            f["total_rules"] for f in FRAMEWORK_SCORES.values()
        ),
        "note": "Gebruik de individuele framework API's voor per-framework scores",
    }


@app.get("/v1/cloud/health")
def health():
    """Health check."""
    store = get_store()
    return {
        "status": "ok",
        "service": "juraregel-cloud",
        "version": "1.0.0",
        "organisations": len(store.list_all()),
        "frameworks": len(FRAMEWORK_SCORES),
        "total_rules": sum(f["total_rules"] for f in FRAMEWORK_SCORES.values()),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8527)
