import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient


path = Path(__file__).parents[1] / "api" / "app.py"
spec = importlib.util.spec_from_file_location("forumstandaardisatie_app", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
client = TestClient(module.app)


def test_standards_are_available_as_catalog():
    assert client.get("/v1/fs/standaarden").json()["totaal"] >= 20


def test_report_is_inventory_not_compliance_score():
    assert client.get("/v1/fs/rapport/test").json()["totaalStandaarden"] >= 20
