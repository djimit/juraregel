import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient


path = Path(__file__).parents[1] / "api" / "app.py"
spec = importlib.util.spec_from_file_location("bio2_app", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
client = TestClient(module.app)


def test_measures_are_available_as_catalog():
    response = client.get("/v1/bio2/maatregelen")
    assert response.status_code == 200
    assert response.json()["totaal"] >= 160


def test_report_without_evidence_is_explicitly_unknown():
    report = client.get("/v1/bio2/rapport/test-org").json()
    assert report["compliant"] == 0
    assert report["geenEvidence"] == report["totaalMaatregelen"]
    assert report["score"] == 0.0


def test_assessment_evidence_drives_report(tmp_path, monkeypatch):
    monkeypatch.setenv("BIO2_EVIDENCE_DB", str(tmp_path / "bio2.db"))
    assessment = client.post("/v1/bio2/assessments", json={
        "organisationId": "test-org",
        "measures": [{"maatregelId": "5.01.01", "status": "compliant", "evidenceType": "test"}],
    }).json()
    report = client.get(f"/v1/bio2/rapport/test-org?assessmentId={assessment['assessmentId']}").json()
    assert report["compliant"] == 1
    assert report["audit"]["evidenceCount"] == 1
