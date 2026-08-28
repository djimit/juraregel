import json
from pathlib import Path


EXPORT = Path(__file__).resolve().parents[1] / "jrem/exports/procesreglement-civiel-2026.1.json"


def test_unverified_process_rules_are_quarantined():
    ruleset = json.loads(EXPORT.read_text())

    assert ruleset["metadata"]["sourceStatus"] == "quarantined"
    assert ruleset["validUntil"] == "2026-06-30"
    assert ruleset["scenarios"] == []
    assert all(rule["outcome"]["confidence"] == "insufficient_evidence" for rule in ruleset["rules"])
    assert all(rule["outcome"]["manualReviewRequired"] is True for rule in ruleset["rules"])
    assert all(rule["outcome"]["category"] == "quarantined" for rule in ruleset["rules"])
