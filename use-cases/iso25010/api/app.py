"""ISO 25010 Software Quality API — Product Quality Model."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "shared"))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("iso25010", JREM_DIR, 8529)


@app.get("/v1/iso25010/quality-model")
def quality_model():
    """Geeft het ISO 25010:2023 kwaliteitsmodel."""
    return {
        "standard": "ISO/IEC 25010:2023",
        "name": "Systems and Software Quality Requirements and Evaluation (SQuaRE)",
        "characteristics": [
            {
                "id": "functional_suitability",
                "name": "Functional Suitability",
                "sub": ["completeness", "correctness", "appropriateness"],
            },
            {
                "id": "performance_efficiency",
                "name": "Performance Efficiency",
                "sub": ["time_behaviour", "resource_utilization", "capacity"],
            },
            {
                "id": "compatibility",
                "name": "Compatibility",
                "sub": ["co_existence", "interoperability"],
            },
            {
                "id": "interaction_capability",
                "name": "Interaction Capability",
                "sub": [
                    "appropriateness_recognizability",
                    "learnability",
                    "operability",
                    "user_error_protection",
                    "user_engagement",
                    "inclusivity",
                    "user_assistance",
                    "self_descriptiveness",
                ],
            },
            {
                "id": "reliability",
                "name": "Reliability",
                "sub": [
                    "maturity",
                    "availability",
                    "fault_tolerance",
                    "recoverability",
                ],
            },
            {
                "id": "security",
                "name": "Security",
                "sub": [
                    "confidentiality",
                    "integrity",
                    "non_repudiation",
                    "accountability",
                    "authenticity",
                ],
            },
            {
                "id": "maintainability",
                "name": "Maintainability",
                "sub": [
                    "modularity",
                    "reusability",
                    "analysability",
                    "modifiability",
                    "testability",
                ],
            },
            {
                "id": "flexibility",
                "name": "Flexibility",
                "sub": ["adaptability", "installability", "replaceability"],
            },
            {
                "id": "safety",
                "name": "Safety",
                "sub": ["health_safety", "environmental_protection"],
            },
        ],
        "total_characteristics": 9,
        "total_sub_characteristics": 31,
    }


@app.post("/v1/iso25010/evaluate")
def evaluate(quality_scores: dict):
    """Evalueer software kwaliteit op basis van ISO 25010."""
    weights = {
        "functional_suitability": 0.15,
        "performance_efficiency": 0.10,
        "compatibility": 0.05,
        "interaction_capability": 0.15,
        "reliability": 0.15,
        "security": 0.15,
        "maintainability": 0.10,
        "flexibility": 0.05,
        "safety": 0.10,
    }

    total_score = 0
    per_char = {}
    for char, weight in weights.items():
        score = quality_scores.get(char, 0)
        weighted = score * weight
        total_score += weighted
        per_char[char] = {
            "score": score,
            "weight": weight,
            "weighted": round(weighted, 2),
        }

    return {
        "overall_quality_score": round(total_score, 2),
        "max_score": 100,
        "grade": "A"
        if total_score >= 90
        else "B"
        if total_score >= 75
        else "C"
        if total_score >= 60
        else "D",
        "per_characteristic": per_char,
        "recommendations": [
            {
                "characteristic": char,
                "action": "Verbeteren" if data["score"] < 60 else "Onderhouden",
            }
            for char, data in per_char.items()
            if data["score"] < 75
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8529)
