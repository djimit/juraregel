"""Local code-pattern benchmark API; not an OpenMythos benchmark result."""

from fastapi import APIRouter

from ..benchmark_runner import benchmark_runner, CATEGORY_MAP

router = APIRouter()


@router.get("/")
async def benchmark_status():
    """Get benchmark status."""
    return {
        "status": "local-static-analysis",
        "total_cases": len(benchmark_runner._cases),
        "evidence_status": "evidence-incomplete",
        "disclaimer": "Locally defined checks; no external OpenMythos or legal-compliance conclusion.",
    }


@router.get("/categories")
async def list_categories():
    """List benchmark categories."""
    return {"categories": [{"id": k, "articles": v} for k, v in CATEGORY_MAP.items()]}


@router.post("/run")
async def run_benchmarks(category: str | None = None):
    """Run benchmarks."""
    if category:
        result = benchmark_runner.run_category(category)
        if not result:
            return {"error": f"Category not found: {category}"}
        return {
            "category": result.category,
            "score": result.score,
            "verdict": result.verdict,
            "passed": result.passed,
            "total": result.total,
            "findings": result.findings,
        }

    report = benchmark_runner.run_all()
    return {
        "run_id": report.run_id,
        "evidence_status": "evidence-incomplete",
        "disclaimer": "Locally defined code-pattern checks; no external OpenMythos grade.",
        "overall_score": report.overall_score,
        "overall_verdict": report.overall_verdict,
        "summary": report.summary,
        "results": [
            {
                "case_id": r.case_id,
                "category": r.category,
                "score": r.score,
                "verdict": r.verdict,
            }
            for r in report.results
        ],
    }
