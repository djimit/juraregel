"""
Review Queue Web Interface (FastAPI).

ponytail: JSON file als DB ipv PostgreSQL — <1000 items, single user
Upgrade pad: multi-user/production → PostgreSQL + auth
"""
import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException

app = FastAPI(title="JuraRegel Rule Review Queue")

REVIEW_DB = Path(".data/review-queue.json")


def load_review_db() -> list[dict]:
    if REVIEW_DB.exists():
        return json.loads(REVIEW_DB.read_text())
    return []


def save_review_db(items: list[dict]):
    REVIEW_DB.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_DB.write_text(json.dumps(items, indent=2, ensure_ascii=False))


@app.get("/api/review/pending")
def get_pending():
    """Get all pending review items."""
    items = load_review_db()
    return [i for i in items if i.get("status") == "pending"]


@app.post("/api/review/{rule_id}/approve")
def approve(rule_id: str, reviewer: str = "system", notes: str = ""):
    """Approve a rule for JREM export."""
    items = load_review_db()
    for i in items:
        if i["rule_id"] == rule_id:
            i["status"] = "approved"
            i["reviewer"] = reviewer
            i["review_notes"] = notes
            save_review_db(items)
            return {"status": "approved", "rule_id": rule_id}
    raise HTTPException(404, "Rule not found")


@app.post("/api/review/{rule_id}/reject")
def reject(rule_id: str, reviewer: str = "system", notes: str = ""):
    """Reject a rule."""
    items = load_review_db()
    for i in items:
        if i["rule_id"] == rule_id:
            i["status"] = "rejected"
            i["reviewer"] = reviewer
            i["review_notes"] = notes
            save_review_db(items)
            return {"status": "rejected", "rule_id": rule_id}
    raise HTTPException(404, "Rule not found")


@app.post("/api/export/approved")
def export_approved(domain: str):
    """Export all approved rules to JREM format."""
    items = load_review_db()
    approved = [i for i in items if i.get("status") == "approved" and i.get("domain") == domain]
    return {
        "ruleSetId": f"{domain}-extracted",
        "version": "auto",
        "rules": [{
            "ruleId": i["rule_id"],
            "name": i["name"],
            "conditions": i["conditions"],
            "outcome": i["outcome"],
            "sourceRefs": i.get("source_refs", []),
        } for i in approved]
    }


@app.post("/api/review/add")
def add_review_item(item: dict):
    """Add a rule to the review queue."""
    items = load_review_db()
    items.append(item)
    save_review_db(items)
    return {"status": "added", "rule_id": item.get("rule_id")}
