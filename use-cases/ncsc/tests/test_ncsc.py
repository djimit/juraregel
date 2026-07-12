import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient


path = Path(__file__).parents[1] / "api" / "app.py"
spec = importlib.util.spec_from_file_location("ncsc_app", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
client = TestClient(module.app)


def test_lists_real_guidelines():
    response = client.get("/v1/ncsc/richtlijnen")
    assert response.status_code == 200
    assert response.json()["totaal"] >= 30


def test_report_is_inventory_not_compliance_score():
    response = client.get("/v1/ncsc/rapport/test")
    assert response.status_code == 200
    assert response.json()["totaalRichtlijnen"] >= 30
