import sys
from pathlib import Path

import importlib.util

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))

# Load the specific app.py to avoid module name conflicts across use cases
_app_path = Path(__file__).parent.parent / "api" / "app.py"
_spec = importlib.util.spec_from_file_location("participatiewet_app", _app_path)
_app_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_app_module)
app = _app_module.app

from fastapi.testclient import TestClient

client = TestClient(app)

def test_health():
    r = client.get("/v1/health")
    assert r.status_code == 200

def test_bijstandsnorm_alleenstaande():
    r = client.post("/v1/participatiewet/calculate", json={"huishoudenType": "alleenstaande", "leeftijd": 25})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["bijstandsnorm"]["amount"] == 1460.32

def test_bijstandsnorm_gehuwden():
    r = client.post("/v1/participatiewet/calculate", json={"huishoudenType": "gehuwden", "leeftijd": 30})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["bijstandsnorm"]["amount"] == 2087.48

def test_bijstandsnorm_alleenstaande_ouder():
    r = client.post("/v1/participatiewet/calculate", json={"huishoudenType": "alleenstaande_ouder", "leeftijd": 28})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["bijstandsnorm"]["amount"] == 1768.47

def test_vermogen_alleenstaande_onder_grens():
    r = client.post("/v1/participatiewet/calculate", json={"huishoudenType": "alleenstaande", "leeftijd": 30, "vermogen": 5000})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["vermogenAkkoord"] is True

def test_vermogen_alleenstaande_boven_grens():
    r = client.post("/v1/participatiewet/calculate", json={"huishoudenType": "alleenstaande", "leeftijd": 30, "vermogen": 8000})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["vermogenAkkoord"] is False

def test_vermogen_gehuwden_onder_grens():
    r = client.post("/v1/participatiewet/calculate", json={"huishoudenType": "gehuwden", "leeftijd": 35, "vermogen": 12000})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["vermogenAkkoord"] is True

def test_vermogen_gehuwden_boven_grens():
    r = client.post("/v1/participatiewet/calculate", json={"huishoudenType": "gehuwden", "leeftijd": 35, "vermogen": 15000})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["vermogenAkkoord"] is False

def test_onder_21_geen_bijstand():
    r = client.post("/v1/participatiewet/calculate", json={"huishoudenType": "alleenstaande", "leeftijd": 19})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["bijstand"] is False

def test_kostendelersnorm_met_medebewoner():
    r = client.post("/v1/participatiewet/calculate", json={"huishoudenType": "alleenstaande", "leeftijd": 25, "alleenstaande": True, "medebewoners": 1, "medebewonerZelfstandigeHuishouding": False})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["kostendelersnorm"] is True

def test_kostendelersnorm_zonder_medebewoners():
    r = client.post("/v1/participatiewet/calculate", json={"huishoudenType": "alleenstaande", "leeftijd": 25, "alleenstaande": True, "medebewoners": 0})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["kostendelersnorm"] is False

def test_vrijlating_inkomen_eerste_4_maanden():
    r = client.post("/v1/participatiewet/calculate", json={"huishoudenType": "alleenstaande", "leeftijd": 30, "inkomenUitWerk": True, "maandenAanHetWerk": 2})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["vrijlatingPercentage"] == 100

def test_vrijlating_inkomen_maanden_5_12():
    r = client.post("/v1/participatiewet/calculate", json={"huishoudenType": "alleenstaande", "leeftijd": 30, "inkomenUitWerk": True, "maandenAanHetWerk": 8})
    assert r.status_code == 200
    data = r.json()
    assert "vrijlatingPercentage" in data["result"]["outcome"]

def test_verwijtbare_werkloosheid_sanctie():
    r = client.post("/v1/participatiewet/calculate", json={"huishoudenType": "alleenstaande", "leeftijd": 30, "verwijtbareWerkloosheid": True})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["sanctie"] is True

def test_sollicitatieplicht():
    r = client.post("/v1/participatiewet/calculate", json={"huishoudenType": "alleenstaande", "leeftijd": 30, "uitkeringOntvangen": True, "arbeidsgeschikt": True})
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["sollicitatieplicht"] is True

def test_explain():
    r = client.post("/v1/participatiewet/explain", json={"huishoudenType": "alleenstaande", "leeftijd": 25})
    assert r.status_code == 200

def test_versions():
    r = client.get("/v1/participatiewet/versions")
    assert r.status_code == 200
