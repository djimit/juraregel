"""CI Gates API — Compliance-as-Code for CI/CD pipelines."""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

from ..ci_gates import CIGates

router = APIRouter()


class CIGateRequest(BaseModel):
    """CI gate request."""

    commit_sha: str = "unknown"
    branch: str = "unknown"
    assessment_id: str | None = None
    current_state: dict = {}
    policy_context: dict = {}
    evidence: list[dict] = []
    benchmark_category: str | None = None
    template_id: str = "dpia_pre_scan"


@router.get("/")
async def ci_status():
    """Get CI gates status."""
    gates = CIGates()
    return {
        "status": "active",
        "gates": [g.__name__ for g in gates.gates],
    }


@router.post("/run")
async def run_ci_gates(request: CIGateRequest):
    """Run all CI gates."""
    gates = CIGates()
    report = gates.run_all(request.dict())

    return {
        "passed": report.overall_passed,
        "score": report.overall_score,
        "commit_sha": report.commit_sha,
        "branch": report.branch,
        "results": [
            {
                "gate": r.gate,
                "passed": r.passed,
                "score": r.score,
                "findings": r.findings,
                "duration_ms": r.duration_ms,
            }
            for r in report.results
        ],
    }


@router.post("/gate/{gate_name}")
async def run_specific_gate(gate_name: str, request: CIGateRequest):
    """Run a specific CI gate."""
    gates = CIGates()
    for gate_fn in gates.gates:
        if gate_fn.__name__ == f"_gate_{gate_name}":
            result = gate_fn(request.dict())
            return {
                "gate": result.gate,
                "passed": result.passed,
                "score": result.score,
                "findings": result.findings,
            }
    return {"error": f"Gate not found: {gate_name}"}
