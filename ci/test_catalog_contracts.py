import importlib.util
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared"))

CATALOG_DOMAINS = (
    "algoritmeregister", "api-registratie", "avg-gdpr", "bio2",
    "btw-tarieven", "classificatie", "compliance-debt", "data-overheid-dcat",
    "dpia-model", "eu-ai-act", "forumstandaardisatie", "gegevensdelingsbeleid",
    "ind-verblijfsregels", "ncsc", "nis2", "nora", "overheidsstandaarden",
    "procesreglement", "publicatie", "regulatory-impact", "traceability", "wmo",
    "ww-uitkering",
)


def load_client(domain: str) -> TestClient:
    app_path = ROOT / "use-cases" / domain / "api" / "app.py"
    spec = importlib.util.spec_from_file_location(f"catalog_{domain.replace('-', '_')}", app_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return TestClient(module.app)


@pytest.mark.parametrize("domain", CATALOG_DOMAINS)
def test_unproved_generic_calculation_is_blocked(domain):
    client = load_client(domain)
    health = client.get("/v1/health").json()
    assert health["capabilities"]["calculate"] is False

    response = client.post(f"/v1/{domain}/calculate", json={})
    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "catalog_only"
