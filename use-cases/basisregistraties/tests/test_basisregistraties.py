import sys
from pathlib import Path

import importlib.util

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))

# Load the specific app.py to avoid module name conflicts across use cases
_app_path = Path(__file__).parent.parent / "api" / "app.py"
_spec = importlib.util.spec_from_file_location("basisregistraties_app", _app_path)
_app_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_app_module)
app = _app_module.app

from fastapi.testclient import TestClient

client = TestClient(app)

def test_health():
    r = client.get("/v1/health")
    assert r.status_code == 200

def test_brp_overheidsorgaan_met_grondslag_toegang():
    r = client.post("/v1/basisregistraties/calculate", json={"registratie": "BRP", "vrager": "overheidsorgaan", "doel": "wettelijke_taak", "grondslag": "aanwezig"})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["toegang"] is True

def test_brp_zonder_grondslag_geen_toegang():
    r = client.post("/v1/basisregistraties/calculate", json={"registratie": "BRP", "vrager": "overheidsorgaan", "doel": "wettelijke_taak", "grondslag": "afwezig"})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["toegang"] is False

def test_brp_derde_zonder_wettelijke_taak_geen_toegang():
    r = client.post("/v1/basisregistraties/calculate", json={"registratie": "BRP", "vrager": "derde", "doel": "niet_wettelijk"})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["toegang"] is False

def test_bag_open_data_toegang():
    r = client.post("/v1/basisregistraties/calculate", json={"registratie": "BAG"})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["toegang"] is True

def test_nhr_publiek_toegang():
    r = client.post("/v1/basisregistraties/calculate", json={"registratie": "NHR", "vrager": "publiek", "gebruiksdoel": "commercieel_of_recht"})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["toegang"] is True

def test_nhr_commercieel_leges():
    r = client.post("/v1/basisregistraties/calculate", json={"registratie": "NHR", "vrager": "publiek", "gebruiksdoel": "commercieel"})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["leges"] is True

def test_brt_open_data():
    r = client.post("/v1/basisregistraties/calculate", json={"registratie": "BRT"})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["toegang"] is True

def test_woz_belastingorgaan_toegang():
    r = client.post("/v1/basisregistraties/calculate", json={"registratie": "WOZ", "vrager": "belastingorgaan", "doel": "heffing"})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["toegang"] is True

def test_woz_burger_eigen_woning_toegang():
    r = client.post("/v1/basisregistraties/calculate", json={"registratie": "WOZ", "vrager": "burger", "doel": "bezwaar_of_inzicht", "eigenObject": True})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["toegang"] is True

def test_woz_derde_zonder_grondslag_geen_toegang():
    r = client.post("/v1/basisregistraties/calculate", json={"registratie": "WOZ", "vrager": "derde", "doel": "niet_belasting", "wettelijkeGrondslag": "afwezig"})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["toegang"] is False

def test_doelbinding_zonder_geregistreerd_doel():
    r = client.post("/v1/basisregistraties/calculate", json={"registratie": "BRP", "vrager": "overheidsorgaan", "doel": "wettelijke_taak", "grondslag": "aanwezig", "doelGeregistreerd": False})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["toegang"] is False

def test_avg22_geen_geautomatiseerde_besluitvorming_zonder_controle():
    r = client.post("/v1/basisregistraties/calculate", json={"registratie": "BRP", "vrager": "overheidsorgaan", "doel": "wettelijke_taak", "grondslag": "aanwezig", "besluitvorming": "geautomatiseerd", "menselijkeControle": False})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["toegang"] is False

def test_explain():
    r = client.post("/v1/basisregistraties/explain", json={"registratie": "BAG"})
    assert r.status_code == 200

def test_versions():
    r = client.get("/v1/basisregistraties/versions")
    assert r.status_code == 200
