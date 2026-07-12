import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient


path = Path(__file__).parents[1] / "api" / "app.py"
spec = importlib.util.spec_from_file_location("gegevensdelingsbeleid_app", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
client = TestClient(module.app)


def test_doelbinding_endpoint():
    response = client.get("/v1/gdb/check-doelbinding?verstrekker=a&ontvanger=b&doel=onderzoek")
    assert response.status_code == 200


def test_biv_endpoint():
    response = client.get("/v1/gdb/biv-classify?beschikbaarheid=3&integriteit=3&vertrouwelijkheid=3")
    assert response.status_code == 200
