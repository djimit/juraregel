import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "enterprise_readiness", ROOT / "ci" / "enterprise_readiness.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_repository_and_external_gaps_remain_explicit():
    result = module.evaluate(ROOT)

    assert result["status"] == "external-gates-required"
    assert result["repositoryGaps"] == []
    assert result["externalGates"] == [
        "ER-ECO-01",
        "ER-LEGAL-01",
        "ER-ISO-01",
        "ER-OPS-01",
    ]
    assert "score" not in result
