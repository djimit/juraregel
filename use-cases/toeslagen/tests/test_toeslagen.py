import sys
from pathlib import Path

import importlib.util

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))

# Load the specific app.py to avoid module name conflicts across use cases
_app_path = Path(__file__).parent.parent / "api" / "app.py"
_spec = importlib.util.spec_from_file_location("toeslagen_app", _app_path)
_app_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_app_module)
app = _app_module.app

from fastapi.testclient import TestClient

client = TestClient(app)

def test_health():
    r = client.get("/v1/health")
    assert r.status_code == 200

def test_zorgtoeslag_alleenstaande_onder_grens():
    r = client.post("/v1/toeslagen/calculate", json={
        "toeslagType": "zorgtoeslag",
        "leeftijd": 25,
        "alleenstaande": True,
        "inkomen": 30000
    })
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["recht"] is True

def test_zorgtoeslag_alleenstaande_boven_grens():
    r = client.post("/v1/toeslagen/calculate", json={
        "toeslagType": "zorgtoeslag",
        "leeftijd": 30,
        "alleenstaande": True,
        "inkomen": 40000
    })
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["recht"] is False

def test_zorgtoeslag_samenwonend_onder_grens():
    r = client.post("/v1/toeslagen/calculate", json={
        "toeslagType": "zorgtoeslag",
        "leeftijd": 35,
        "alleenstaande": False,
        "toeslagenpartner": True,
        "inkomen": 45000
    })
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["recht"] is True

def test_zorgtoeslag_samenwonend_boven_grens():
    r = client.post("/v1/toeslagen/calculate", json={
        "toeslagType": "zorgtoeslag",
        "leeftijd": 40,
        "alleenstaande": False,
        "toeslagenpartner": True,
        "inkomen": 50000
    })
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["recht"] is False

def test_huurtoeslag_onder_huurgrens():
    r = client.post("/v1/toeslagen/calculate", json={
        "toeslagType": "huurtoeslag",
        "leeftijd": 25,
        "alleenstaande": True,
        "huur": 700,
        "inkomen": 20000
    })
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["recht"] is True

def test_huurtoeslag_boven_huurgrens():
    r = client.post("/v1/toeslagen/calculate", json={
        "toeslagType": "huurtoeslag",
        "leeftijd": 30,
        "alleenstaande": True,
        "huur": 900,
        "inkomen": 20000
    })
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["recht"] is False

def test_huurtoeslag_jongere_18_22():
    r = client.post("/v1/toeslagen/calculate", json={
        "toeslagType": "huurtoeslag",
        "leeftijd": 20,
        "alleenstaande": True,
        "huur": 400,
        "inkomen": 20000
    })
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["recht"] is True

def test_kinderopvangtoeslag_laag_inkomen():
    r = client.post("/v1/toeslagen/calculate", json={
        "toeslagType": "kinderopvangtoeslag",
        "kindOpOpvang": True,
        "inkomen": 30000
    })
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["recht"] is True
    assert data["result"]["outcome"]["percentage"] == 96

def test_kinderopvangtoeslag_hoog_inkomen():
    r = client.post("/v1/toeslagen/calculate", json={
        "toeslagType": "kinderopvangtoeslag",
        "kindOpOpvang": True,
        "inkomen": 150000
    })
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["recht"] is False

def test_kindgebonden_budget_alleenstaande_onder_grens():
    r = client.post("/v1/toeslagen/calculate", json={
        "toeslagType": "kindgebonden_budget",
        "heeftKind": True,
        "alleenstaande": True,
        "inkomen": 50000
    })
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["recht"] is True

def test_kindgebonden_budget_alleenstaande_boven_grens():
    r = client.post("/v1/toeslagen/calculate", json={
        "toeslagType": "kindgebonden_budget",
        "heeftKind": True,
        "alleenstaande": True,
        "inkomen": 55000
    })
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["recht"] is False

def test_kindgebonden_budget_samenwonend_onder_grens():
    r = client.post("/v1/toeslagen/calculate", json={
        "toeslagType": "kindgebonden_budget",
        "heeftKind": True,
        "alleenstaande": False,
        "toeslagenpartner": True,
        "inkomen": 65000
    })
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["recht"] is True

def test_kindgebonden_budget_samenwonend_boven_grens():
    r = client.post("/v1/toeslagen/calculate", json={
        "toeslagType": "kindgebonden_budget",
        "heeftKind": True,
        "alleenstaande": False,
        "toeslagenpartner": True,
        "inkomen": 70000
    })
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["recht"] is False

def test_geen_toeslag_detentie():
    r = client.post("/v1/toeslagen/calculate", json={
        "toeslagType": "zorgtoeslag",
        "leeftijd": 30,
        "alleenstaande": True,
        "inkomen": 30000,
        "gedetineerd": True
    })
    assert r.status_code == 200
    data = r.json()
    assert data["result"]["outcome"]["recht"] is False

def test_explain():
    r = client.post("/v1/toeslagen/explain", json={
        "toeslagType": "zorgtoeslag",
        "leeftijd": 25,
        "alleenstaande": True,
        "inkomen": 30000
    })
    assert r.status_code == 200

def test_versions():
    r = client.get("/v1/toeslagen/versions")
    assert r.status_code == 200
