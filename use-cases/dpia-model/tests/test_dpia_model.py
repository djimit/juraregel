import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient


path = Path(__file__).parents[1] / "api" / "app.py"
spec = importlib.util.spec_from_file_location("dpia_model_app", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
client = TestClient(module.app)


def test_large_special_category_processing_requires_dpia():
    response = client.get("/v1/dpia/vereist?verwerkingType=grootschalig&persoonsgegevensType=bijzonder")
    assert response.json()["dpiaVereist"] is True


def test_small_regular_processing_does_not_require_dpia():
    response = client.get("/v1/dpia/vereist?verwerkingType=klein&persoonsgegevensType=regulier&monitoring=nee&automatisering=nee")
    assert response.json()["dpiaVereist"] is False
