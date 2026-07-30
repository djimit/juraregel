"""Local evidence questionnaire API; no OpenMythos-grade is inferred."""

from fastapi import APIRouter

from ..continuous_evaluation import continuous_evaluation

router = APIRouter()


@router.get("/")
async def evaluation_status():
    """Get evaluation engine status."""
    return {
        "status": "evidence-incomplete",
        "modules_evaluated": len(continuous_evaluation.CRITERIA),
        "criteria_total": sum(
            len(c["checks"]) for c in continuous_evaluation.CRITERIA.values()
        ),
        "disclaimer": "Local self-check criteria; no external OpenMythos or compliance conclusion.",
    }


@router.post("/run")
async def run_evaluation():
    """Run continuous evaluation across all modules."""
    report = continuous_evaluation.evaluate_all()

    return {
        "report_id": report.report_id,
        "timestamp": report.timestamp,
        "overall_score": report.overall_score,
        "overall_grade": report.overall_grade,
        "evidence_status": "evidence-incomplete",
        "disclaimer": "Scores reflect missing/present local evidence only; no external benchmark grade.",
        "results": [
            {
                "module": r.module,
                "category": r.category,
                "score": r.score,
                "max_score": r.max_score,
                "percentage": round(r.score / r.max_score * 100, 1)
                if r.max_score > 0
                else 0,
                "passed": r.passed,
                "findings": r.findings,
                "recommendations": r.recommendations,
            }
            for r in report.results
        ],
        "improvements": report.improvements,
        "regressions": report.regressions,
        "action_items": report.action_items,
    }


@router.get("/modules")
async def list_modules():
    """List evaluated modules."""
    return {
        "modules": [
            {"id": k, "description": v["description"], "checks": len(v["checks"])}
            for k, v in continuous_evaluation.CRITERIA.items()
        ]
    }
