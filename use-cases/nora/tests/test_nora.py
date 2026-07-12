import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient


path = Path(__file__).parents[1] / "api" / "app.py"
spec = importlib.util.spec_from_file_location("nora_app", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
client = TestClient(module.app)


def test_principles_are_available_as_catalog():
    assert client.get("/v1/nora/principes").json()["totaal"] >= 15


def test_matrix_is_available_as_catalog():
    assert client.get("/v1/nora/matrix").json()["totaal"] >= 15
