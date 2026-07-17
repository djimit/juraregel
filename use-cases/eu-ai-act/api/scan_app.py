"""
EU AI Act Code Compliance Scanner API — extends the base JuraRegel API.

Adds:
  POST /v1/eu-ai-act/scan  →  run code compliance scan on a directory
  GET  /v1/eu-ai-act/scan/rules  →  list all 14 code scanning rules
  GET  /v1/eu-ai-act/evidence →  generate evidence bundle summary
"""

import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))

from api_base import create_app
from lib.code_scanner import scan_codebase, CodeFinding

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("eu-ai-act", JREM_DIR, 8498)


class ScanRequest(BaseModel):
    path: str = Field(..., description="Absolute path to codebase to scan")
    include_passes: bool = Field(True, description="Include passing checks in results")


class ScanResponse(BaseModel):
    scanId: str
    timestamp: str
    targetPath: str
    totalFiles: int
    totalChecks: int
    passed: int
    warnings: int
    failed: int
    findings: list
    summary: dict


@app.post("/v1/eu-ai-act/scan", response_model=ScanResponse, tags=["code-compliance"])
async def scan_code(request: ScanRequest):
    """Run EU AI Act code compliance scan on a codebase directory."""
    scan_path = Path(request.path)
    if not scan_path.exists():
        raise HTTPException(status_code=404, detail=f"Path not found: {request.path}")
    if not scan_path.is_dir():
        raise HTTPException(
            status_code=400, detail=f"Path is not a directory: {request.path}"
        )

    findings = scan_codebase(str(scan_path))

    passed = sum(1 for f in findings if f.status == "pass")
    warnings = sum(1 for f in findings if f.status == "warn")
    failed = sum(1 for f in findings if f.status == "fail")

    result_findings = (
        findings
        if request.include_passes
        else [f for f in findings if f.status != "pass"]
    )

    import uuid

    return ScanResponse(
        scanId=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
        targetPath=str(scan_path.resolve()),
        totalFiles=_count_source_files(str(scan_path)),
        totalChecks=len(findings),
        passed=passed,
        warnings=warnings,
        failed=failed,
        findings=[_finding_to_dict(f) for f in result_findings],
        summary={
            "complianceScore": round((passed / max(len(findings), 1)) * 100),
            "riskLevel": "high" if failed > 0 else "medium" if warnings > 0 else "low",
            "articles": _summarize_articles(findings),
            "maturity": "L1",
            "framework": "EU AI Act",
            "scannerVersion": "2026.1-air-port",
        },
    )


@app.get("/v1/eu-ai-act/scan/rules", tags=["code-compliance"])
async def list_scan_rules():
    """List all 14 code scanning rules with their EU AI Act article mapping."""
    return {
        "totalRules": 14,
        "rules": [
            {
                "ruleId": "AIR-09-01",
                "article": "Art 9(1)",
                "name": "LLM call error handling",
                "category": "risk-management",
            },
            {
                "ruleId": "AIR-09-02",
                "article": "Art 9(2)",
                "name": "Fallback/recovery patterns",
                "category": "risk-management",
            },
            {
                "ruleId": "AIR-10-01",
                "article": "Art 10(2)",
                "name": "Input validation / schema enforcement",
                "category": "data-governance",
            },
            {
                "ruleId": "AIR-10-02",
                "article": "Art 10(3)",
                "name": "PII handling in code",
                "category": "data-governance",
            },
            {
                "ruleId": "AIR-11-01",
                "article": "Art 11(1)",
                "name": "Code documentation (docstrings)",
                "category": "documentation",
            },
            {
                "ruleId": "AIR-11-02",
                "article": "Art 11(2)",
                "name": "Type annotations",
                "category": "documentation",
            },
            {
                "ruleId": "AIR-12-01",
                "article": "Art 12(1)",
                "name": "Application logging",
                "category": "record-keeping",
            },
            {
                "ruleId": "AIR-12-02",
                "article": "Art 12(2)",
                "name": "Tracing / observability",
                "category": "record-keeping",
            },
            {
                "ruleId": "AIR-14-01",
                "article": "Art 14(1)",
                "name": "Human-in-the-loop patterns",
                "category": "human-oversight",
            },
            {
                "ruleId": "AIR-14-02",
                "article": "Art 14(3)",
                "name": "Usage limits / budget controls",
                "category": "human-oversight",
            },
            {
                "ruleId": "AIR-15-01",
                "article": "Art 15(1)",
                "name": "Retry / backoff logic",
                "category": "robustness",
            },
            {
                "ruleId": "AIR-15-02",
                "article": "Art 15(2)",
                "name": "Prompt injection defense",
                "category": "robustness",
            },
            {
                "ruleId": "AIR-15-03",
                "article": "Art 15(3)",
                "name": "LLM output validation",
                "category": "robustness",
            },
            {
                "ruleId": "AIR-15-04",
                "article": "Art 15(4)",
                "name": "Unsafe code execution",
                "category": "robustness",
            },
        ],
    }


@app.get("/v1/eu-ai-act/evidence", tags=["code-compliance"])
async def get_evidence_summary():
    """Return evidence bundle metadata for audit purposes."""
    return {
        "framework": "EU AI Act",
        "scannerVersion": "2026.1-air-port",
        "totalChecks": 14,
        "coverage": {
            "articles": ["Art 9", "Art 10", "Art 11", "Art 12", "Art 14", "Art 15"],
            "gaps": ["Art 13 (transparency)"],
        },
        "detectionTypes": ["auto", "hybrid", "manual"],
        "maturity": "L1",
        "disclaimer": "This is a code-level compliance scan. It does not replace legal review or conformity assessment under Art 43.",
    }


def _finding_to_dict(f: CodeFinding) -> dict:
    return {
        "ruleId": f.ruleId,
        "article": f.article,
        "name": f.name,
        "status": f.status,
        "evidence": f.evidence,
        "detection": f.detection,
        "fix_hint": f.fix_hint,
        "files": [_rel_path(p) for p in f.files[:5]],
        "severity": f.severity,
        "maturity": f.maturity,
    }


def _rel_path(filepath: str) -> str:
    return os.path.relpath(filepath)


def _count_source_files(scan_path: str) -> int:
    count = 0
    skip = {"node_modules", ".git", "__pycache__", ".venv", "venv", ".swarm"}
    for root, dirs, files in os.walk(scan_path):
        dirs[:] = [d for d in dirs if d not in skip]
        for f in files:
            if f.endswith((".py", ".ts", ".tsx", ".js", ".jsx")):
                count += 1
    return count


def _summarize_articles(findings: list) -> dict:
    articles = {}
    for f in findings:
        key = f.article
        if key not in articles:
            articles[key] = {"passed": 0, "warnings": 0, "failed": 0}
        if f.status == "pass":
            articles[key]["passed"] += 1
        elif f.status == "warn":
            articles[key]["warnings"] += 1
        else:
            articles[key]["failed"] += 1
    return articles


import os

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8498)
