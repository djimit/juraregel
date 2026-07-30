#!/usr/bin/env python3
"""Evaluate assurance evidence completeness without producing a compliance score."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


STATUSES = {"satisfied", "not_satisfied", "insufficient_evidence", "not_applicable"}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def evaluate(profile: dict, assessment: dict) -> dict:
    if assessment.get("profileId") != profile.get("profileId"):
        raise ValueError("assessment profileId does not match profile")
    if assessment.get("profileVersion") != profile.get("version"):
        raise ValueError("assessment profileVersion does not match profile")

    aspects = profile.get("aspects", [])
    aspect_ids = [item["aspectId"] for item in aspects]
    if len(aspect_ids) != len(set(aspect_ids)):
        raise ValueError("profile contains duplicate aspectId values")

    findings = assessment.get("findings", [])
    finding_ids = [item.get("aspectId") for item in findings]
    if len(finding_ids) != len(set(finding_ids)):
        raise ValueError("assessment contains duplicate aspectId values")
    unknown = sorted(set(finding_ids) - set(aspect_ids))
    if unknown:
        raise ValueError(f"assessment contains unknown aspects: {unknown}")

    by_id = {item["aspectId"]: item for item in findings}
    results = []
    for aspect in aspects:
        finding = by_id.get(aspect["aspectId"])
        reasons = []
        if finding is None:
            status = "insufficient_evidence"
            reasons.append("finding ontbreekt")
            finding = {}
        else:
            status = finding.get("status")
            if status not in STATUSES:
                raise ValueError(f"{aspect['aspectId']} has invalid status: {status}")

        if status == "insufficient_evidence":
            reasons.append("bewijs is onvoldoende")
        elif status == "not_applicable":
            if not finding.get("rationale"):
                reasons.append("rationale ontbreekt")
        else:
            if status in {"satisfied", "not_satisfied"} and not finding.get("evidenceRefs"):
                reasons.append("evidenceRefs ontbreekt")

        for field in ("owner", "reviewedBy", "reviewedAt"):
            if not finding.get(field):
                reasons.append(f"{field} ontbreekt")

        for field in ("risk", "measure", "residualRisk"):
            if status != "not_applicable" and not finding.get(field):
                reasons.append(f"{field} ontbreekt")

        results.append({
            "aspectId": aspect["aspectId"],
            "status": status,
            "complete": not reasons,
            "reasons": reasons,
        })

    incomplete = [item["aspectId"] for item in results if not item["complete"]]
    return {
        "profileId": profile["profileId"],
        "profileVersion": profile["version"],
        "assessmentId": assessment.get("assessmentId"),
        "status": "review-ready" if not incomplete else "evidence-incomplete",
        "aspectCount": len(results),
        "incompleteAspects": incomplete,
        "findings": results,
        "disclaimer": profile["disclaimer"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path)
    parser.add_argument("assessment", type=Path)
    args = parser.parse_args()
    print(json.dumps(evaluate(read_json(args.profile), read_json(args.assessment)), indent=2))


if __name__ == "__main__":
    main()
