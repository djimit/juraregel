import importlib.util
import json
from pathlib import Path


USE_CASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("acict_assess", USE_CASE / "assess.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def load(relative: str) -> dict:
    return json.loads((USE_CASE / relative).read_text())


def keys(value):
    if isinstance(value, dict):
        return set(value) | {key for item in value.values() for key in keys(item)}
    if isinstance(value, list):
        return {key for item in value for key in keys(item)}
    return set()


def test_profiles_are_non_scoring_and_self_assessment_fails_closed():
    project = load("profiles/projecten-2026.json")
    maintenance = load("profiles/beheer-onderhoud-2025.json")
    assessment = load("assessments/juraregel-projecten-2026.json")

    assert len(project["aspects"]) == 14
    assert len(maintenance["aspects"]) == 18
    assert "score" not in keys([project, maintenance])

    result = module.evaluate(project, assessment)
    assert result["status"] == "evidence-incomplete"
    assert result["aspectCount"] == 14
    assert "projecten-2026.4.3" in result["incompleteAspects"]
    assert "projecten-2026.7.5" in result["incompleteAspects"]

    completed = json.loads(json.dumps(assessment))
    completed["findings"] = [
        {
            "aspectId": aspect["aspectId"],
            "status": "satisfied",
            "evidenceRefs": ["evidence://independently-reviewed"],
            "owner": "system-owner",
            "reviewedBy": "independent-reviewer",
            "reviewedAt": "2026-07-29"
        }
        for aspect in project["aspects"]
    ]
    assert module.evaluate(project, completed)["status"] == "review-ready"
