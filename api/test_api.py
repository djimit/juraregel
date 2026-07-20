"""Integration tests for the JuraRegel API."""

import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


class TestHealth:
    def test_health_check(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"

    def test_readiness(self):
        resp = client.get("/ready")
        assert resp.status_code == 200
        data = resp.json()
        assert data["ready"] is True
        assert data["checks"]["templates"]["status"] == "ok"


class TestTemplates:
    def test_list_templates(self):
        resp = client.get("/api/v1/templates/")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 37

    def test_get_template(self):
        resp = client.get("/api/v1/templates/dpia_pre_scan")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == "dpia_pre_scan"
        assert "section_count" in data

    def test_generate_document(self):
        resp = client.post(
            "/api/v1/templates/dpia_pre_scan/generate",
            json={"organisation": "Gemeente Test", "parameters": {"verwerking": "WOZ"}},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "document" in data

    def test_render_markdown(self):
        resp = client.post(
            "/api/v1/templates/dpia_pre_scan/render",
            json={
                "organisation": "Gemeente Test",
                "parameters": {},
                "format": "markdown",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["format"] == "markdown"
        assert len(data["content"]) > 0

    def test_render_html(self):
        resp = client.post(
            "/api/v1/templates/dpia_pre_scan/render",
            json={"organisation": "Gemeente Test", "parameters": {}, "format": "html"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "<h1>" in data["content"]

    def test_validate_document(self):
        resp = client.post(
            "/api/v1/templates/dpia_pre_scan/validate",
            json={"organisation": "Gemeente Test", "parameters": {}},
        )
        assert resp.status_code == 200
        assert resp.json()["valid"] is True

    def test_template_not_found(self):
        resp = client.get("/api/v1/templates/nonexistent")
        assert resp.status_code == 404


class TestAssessments:
    def test_create_assessment(self):
        resp = client.post(
            "/api/v1/assessments/",
            json={
                "organisation_id": "org-1",
                "assessment_type": "dpia",
                "template_id": "dpia_pre_scan",
                "parameters": {"verwerking": "Test"},
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["status"] == "draft"
        assert data["assessment_type"] == "dpia"
        self.assessment_id = data["id"]

    def test_list_assessments(self):
        resp = client.get("/api/v1/assessments/")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_workflow_lifecycle(self):
        # Create
        resp = client.post(
            "/api/v1/assessments/",
            json={
                "organisation_id": "org-1",
                "assessment_type": "dpia",
                "template_id": "dpia_pre_scan",
                "parameters": {},
            },
        )
        aid = resp.json()["id"]

        # Submit
        resp = client.post(f"/api/v1/assessments/{aid}/submit")
        assert resp.json()["status"] == "in_review"

        # Approve
        resp = client.post(
            f"/api/v1/assessments/{aid}/approve",
            json={"approver": "Piet", "role": "FG", "comments": "Akkoord"},
        )
        assert resp.json()["status"] == "approved"

        # Publish
        resp = client.post(f"/api/v1/assessments/{aid}/publish")
        assert resp.json()["status"] == "published"

        # Archive
        resp = client.post(f"/api/v1/assessments/{aid}/archive")
        assert resp.json()["status"] == "archived"


class TestProcessingActivities:
    def test_create_processing_activity(self):
        resp = client.post(
            "/api/v1/processing-activities/?organisation_id=org-1",
            json={
                "name": "WOZ-verwerking",
                "purpose": "Waardering onroerend goed",
                "legal_basis": "Art. 6(1)(e)",
                "data_categories": ["Naam", "Adres", "WOZ-waarde"],
                "data_subjects": ["Eigenaren"],
                "retention_period": "7 jaar",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "WOZ-verwerking"
        assert "id" in data

    def test_list_processing_activities(self):
        resp = client.get("/api/v1/processing-activities/")
        assert resp.status_code == 200


class TestEvidence:
    def test_add_evidence(self):
        # First create an assessment
        resp = client.post(
            "/api/v1/assessments/",
            json={
                "organisation_id": "org-1",
                "assessment_type": "dpia",
                "template_id": "dpia_pre_scan",
                "parameters": {},
            },
        )
        aid = resp.json()["id"]

        resp = client.post(
            f"/api/v1/evidence/{aid}",
            json={
                "section_id": "stap_1",
                "evidence_type": "wetgeving",
                "title": "AVG Art. 35",
                "reference": "https://eur-lex.europa.eu/eli/reg/2016/679/art_35",
            },
        )
        assert resp.status_code == 201
        assert resp.json()["status"] == "active"

    def test_evidence_coverage(self):
        resp = client.get("/api/v1/evidence/nonexistent/coverage")
        assert resp.status_code == 200
        assert resp.json()["total_evidence"] == 0


class TestRoot:
    def test_root(self):
        resp = client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["service"] == "JuraRegel Compliance API"
        assert "endpoints" in data
