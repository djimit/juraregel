import sys
from pathlib import Path

import importlib.util

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))

# Load the specific app.py to avoid module name conflicts across use cases
_app_path = Path(__file__).parent.parent / "api" / "app.py"
_spec = importlib.util.spec_from_file_location("omgevingswet_app", _app_path)
_app_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_app_module)
app = _app_module.app

from fastapi.testclient import TestClient

client = TestClient(app)

def test_health():
    r = client.get("/v1/health")
    assert r.status_code == 200

def test_bouwen_vergunningplichtig_hoog():
    r = client.post("/v1/omgevingswet/calculate", json={"activiteit": "bouwen", "bouwhoogte": 10})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["vergunningplichtig"] is True

def test_bouwen_meldingplichtig_gemiddeld():
    r = client.post("/v1/omgevingswet/calculate", json={"activiteit": "bouwen", "bouwhoogte": 3})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["meldingplichtig"] is True

def test_bouwen_vrij_laag():
    r = client.post("/v1/omgevingswet/calculate", json={"activiteit": "bouwen", "bouwhoogte": 0.5})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["vrij"] is True

def test_slopen_vergunningplichtig_groot():
    r = client.post("/v1/omgevingswet/calculate", json={"activiteit": "slopen", "volume": 100})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["vergunningplichtig"] is True

def test_slopen_meldingplichtig_klein():
    r = client.post("/v1/omgevingswet/calculate", json={"activiteit": "slopen", "volume": 30})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["meldingplichtig"] is True

def test_kappen_meldingplichtig_grote_boom():
    r = client.post("/v1/omgevingswet/calculate", json={"activiteit": "kappen", "boomHoogte": 10, "stamomtrek": 50})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["meldingplichtig"] is True

def test_kappen_vrij_kleine_boom():
    r = client.post("/v1/omgevingswet/calculate", json={"activiteit": "kappen", "boomHoogte": 3, "stamomtrek": 30})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["vrij"] is True

def test_geluid_vergunningplichtig_boven_drempel():
    r = client.post("/v1/omgevingswet/calculate", json={"activiteit": "geluid_installatie", "geluidsniveau": 65, "locatie": "woning"})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["vergunningplichtig"] is True

def test_geluid_vrij_onder_drempel():
    r = client.post("/v1/omgevingswet/calculate", json={"activiteit": "geluid_installatie", "geluidsniveau": 40, "locatie": "woning"})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["vrij"] is True

def test_storten_vergunningplichtig_groot():
    r = client.post("/v1/omgevingswet/calculate", json={"activiteit": "storten", "volume": 200})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["vergunningplichtig"] is True

def test_storten_meldingplichtig_gemiddeld():
    r = client.post("/v1/omgevingswet/calculate", json={"activiteit": "storten", "volume": 50})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["meldingplichtig"] is True

def test_storten_vrij_klein():
    r = client.post("/v1/omgevingswet/calculate", json={"activiteit": "storten", "volume": 5})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["vrij"] is True

def test_wateronttrekking_vergunningplichtig_groot():
    r = client.post("/v1/omgevingswet/calculate", json={"activiteit": "water_onttrekking", "volume": 200000, "periode": "jaar"})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["vergunningplichtig"] is True

def test_wateronttrekking_vrij_klein():
    r = client.post("/v1/omgevingswet/calculate", json={"activiteit": "water_onttrekking", "volume": 50000, "periode": "jaar"})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["vrij"] is True

def test_monument_bouwen_altijd_vergunning():
    r = client.post("/v1/omgevingswet/calculate", json={"activiteit": "bouwen", "bouwhoogte": 0.5, "monument": True})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["vergunningplichtig"] is True

def test_tijdelijke_bouw():
    r = client.post("/v1/omgevingswet/calculate", json={"activiteit": "bouwen", "bouwhoogte": 10, "tijdelijk": True})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["type"] == "tijdelijke_omgevingsvergunning"

def test_explain():
    r = client.post("/v1/omgevingswet/explain", json={"activiteit": "bouwen", "bouwhoogte": 10})
    assert r.status_code == 200

def test_versions():
    r = client.get("/v1/omgevingswet/versions")
    assert r.status_code == 200
