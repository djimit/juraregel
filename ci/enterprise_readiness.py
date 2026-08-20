#!/usr/bin/env python3
"""Evaluate enterprise-readiness evidence without producing a compliance score."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
link_spec = importlib.util.spec_from_file_location(
    "enterprise_markdown_links", ROOT / "ci" / "check_markdown_links.py"
)
check_markdown_links = importlib.util.module_from_spec(link_spec)
link_spec.loader.exec_module(check_markdown_links)
source_spec = importlib.util.spec_from_file_location(
    "enterprise_source_quality", ROOT / "ci" / "source_quality.py"
)
source_quality = importlib.util.module_from_spec(source_spec)
source_spec.loader.exec_module(source_quality)


def control(
    control_id: str,
    status: str,
    evidence: list[str],
    required_action: str = "",
) -> dict:
    return {
        "controlId": control_id,
        "status": status,
        "evidence": evidence,
        "requiredAction": required_action,
    }


def evaluate(root: Path = ROOT) -> dict:
    compose = (root / "docker-compose.yml").read_text()
    dockerfile = (root / "Dockerfile.api").read_text()
    canonical_gate = (root / "ci" / "run-all-gates.sh").read_text()
    workflow = (root / ".github" / "workflows" / "juraregel-ci.yml").read_text()
    route_sources = {
        path.name: path.read_text()
        for path in (
            root / "api" / "routes" / "assessments.py",
            root / "api" / "routes" / "processing.py",
            root / "api" / "routes" / "evidence.py",
        )
    }
    main_source = (root / "api" / "main.py").read_text()
    evidence = json.loads(
        (root / "evidence" / "ecosystem-status-2026-07-30.json").read_text()
    )

    controls = []
    missing_docs = check_markdown_links.missing_links(root)
    controls.append(
        control(
            "ER-DOC-01",
            "satisfied" if not missing_docs else "not_satisfied",
            ["ci/check_markdown_links.py", f"missing={len(missing_docs)}"],
            "Repair all relative Markdown targets.",
        )
    )

    gate_has_claim_tests = "api/test_*.py tests/test_*.py" in canonical_gate
    controls.append(
        control(
            "ER-CI-01",
            "satisfied" if gate_has_claim_tests else "not_satisfied",
            ["ci/run-all-gates.sh"],
            "Execute API and root assurance tests in the canonical gate.",
        )
    )

    insecure_compose = any(
        marker in compose
        for marker in (
            "192.168.1.28",
            "juraregel:juraregel@",
            'allow_origins=["*"]',
        )
    )
    production_contract = (
        "${DATABASE_URL:?DATABASE_URL is required}" in compose
        and "${KEYCLOAK_URL:?KEYCLOAK_URL is required}" in compose
        and "JURAREGEL_RATE_LIMIT_MODE must be ingress" in compose
        and "USER juraregel" in dockerfile
        and not insecure_compose
    )
    controls.append(
        control(
            "ER-SEC-01",
            "satisfied" if production_contract else "not_satisfied",
            ["docker-compose.yml", "Dockerfile.api", ".env.example"],
            "Remove embedded infrastructure data and require production identity, persistence and CORS configuration.",
        )
    )

    memory_stores = [
        name for name, content in route_sources.items() if "In-memory store" in content
    ]
    prototypes_excluded = (
        'if API_PROFILE == "prototype" and not PRODUCTION:\n    app.include_router(\n        assessments.router'
        in main_source
    )
    controls.append(
        control(
            "ER-DATA-01",
            "satisfied" if not memory_stores or prototypes_excluded else "not_satisfied",
            [f"api/routes/{name}" for name in memory_stores],
            "Keep process-local routes outside production until transactional PostgreSQL storage is implemented.",
        )
    )

    authorization_wired = prototypes_excluded or all(
        "set_tenant_context" in content and "require_role" in content
        for content in route_sources.values()
    )
    controls.append(
        control(
            "ER-AUTHZ-01",
            "satisfied" if authorization_wired else "not_satisfied",
            [f"api/routes/{name}" for name in route_sources],
            "Keep unauthorised prototype routes outside production; require object, role and tenant checks before activation.",
        )
    )

    supply_chain = all(
        marker in workflow.lower()
        for marker in ("sbom-action", "trivy-action", "attest-build-provenance")
    )
    controls.append(
        control(
            "ER-SUPPLY-01",
            "satisfied" if supply_chain else "not_satisfied",
            [".github/workflows/juraregel-ci.yml"],
            "Generate an SBOM, vulnerability result and signed build provenance for release images.",
        )
    )

    source_debt = source_quality.audit(root)
    controls.append(
        control(
            "ER-SOURCE-01",
            "satisfied" if not source_debt["blocking"] else "not_satisfied",
            [
                "ci/source_quality.py",
                f"debt={len(source_debt['debt'])}",
                f"blocking={len(source_debt['blocking'])}",
            ],
            "Keep source debt below L2; promotion requires exact, versioned legal anchors.",
        )
    )

    controls.append(
        control(
            "ER-ECO-01",
            (
                "satisfied"
                if evidence["conclusion"] == "verified"
                else "blocked_external"
            ),
            ["evidence/ecosystem-status-2026-07-30.json"],
            "Persist a versioned OpenMythos run through an approved idempotent Djimitflo transport.",
        )
    )
    controls.append(
        control(
            "ER-LEGAL-01",
            "blocked_external",
            ["ci/legal-review-gate.sh", "docs/review-requests/"],
            "Obtain independent legal acceptance for every use case promoted to L2 or L3.",
        )
    )
    controls.append(
        control(
            "ER-ISO-01",
            "blocked_external",
            ["use-cases/iso27017-assurance/sources/source-register.json"],
            "Register a licensed ISO/NEN source and independent ISO 27017 interpretation review.",
        )
    )
    controls.append(
        control(
            "ER-OPS-01",
            "blocked_external",
            ["docs/production-deployment.md"],
            "Supply deployment-specific TLS, backup/restore, SLO, incident, audit-retention and disaster-recovery evidence.",
        )
    )

    repository_gaps = [
        item["controlId"] for item in controls if item["status"] == "not_satisfied"
    ]
    external_gates = [
        item["controlId"] for item in controls if item["status"] == "blocked_external"
    ]
    status = (
        "repository-incomplete"
        if repository_gaps
        else "external-gates-required"
        if external_gates
        else "review-ready"
    )
    return {
        "profileId": "juraregel-enterprise-readiness",
        "version": "2026-07-30",
        "status": status,
        "repositoryGaps": repository_gaps,
        "externalGates": external_gates,
        "controls": controls,
        "disclaimer": "Non-scoring evidence gate; review-ready is not legal compliance, certification or production approval.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--enforce",
        action="store_true",
        help="Fail unless every repository and external control is satisfied.",
    )
    args = parser.parse_args()
    result = evaluate()
    print(json.dumps(result, indent=2))
    if args.enforce and (result["repositoryGaps"] or result["externalGates"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
