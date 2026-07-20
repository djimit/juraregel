"""OpenMythos Benchmark API — Compliance evaluation framework."""

from fastapi import APIRouter

router = APIRouter()


def _get_runner():
    """Lazy-load benchmark runner."""
    import importlib.util
    from pathlib import Path

    spec = importlib.util.spec_from_file_location(
        "benchmark_runner",
        Path(__file__).resolve().parents[2]
        / "openmythos-integration"
        / "benchmark_runner.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.benchmark_runner, mod.CATEGORY_MAP


@router.get("/")
async def benchmark_status():
    """Get benchmark status."""
    try:
        runner, _ = _get_runner()
        return {
            "status": "active",
            "total_cases": len(runner._cases),
        }
    except Exception:
        return {"status": "unavailable", "reason": "benchmark_runner import error"}


@router.get("/categories")
async def list_categories():
    """List benchmark categories."""
    try:
        _, category_map = _get_runner()
        return {
            "categories": [{"id": k, "articles": v} for k, v in category_map.items()]
        }
    except Exception as e:
        return {"error": str(e)}


@router.post("/run")
async def run_benchmarks(category=None):
    """Run benchmarks."""
    try:
        runner, _ = _get_runner()
        if category:
            result = runner.run_category(category)
            if not result:
                return {"error": f"Category not found: {category}"}
            return {
                "category": result.category,
                "score": result.score,
                "verdict": result.verdict,
            }

        report = runner.run_all()
        return {
            "run_id": report.run_id,
            "overall_score": report.overall_score,
            "overall_verdict": report.overall_verdict,
            "summary": report.summary,
        }
    except Exception as e:
        return {"error": str(e)}
