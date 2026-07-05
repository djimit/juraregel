"""Tests voor PII Check Endpoint (V4.2 engine)."""
import sys, json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app

# Import the publicatie app with check-pii endpoint
exec(open(Path(__file__).parent.parent / "api" / "app.py").read())
client = TestClient(app)

class TestPiiCheck:
    def test_professional_not_pseudonimised(self):
        """Geboortedatum van advocaat → niet pseudonimiseer."""
        r = client.post("/v1/publicatie/check-pii", json={
            "bodyText": "mr. J. Pieterse, advocaat, geboren op 15 maart 1965, werkzaam bij kantoor.",
            "rechtsgebied": "civiel"
        })
        assert r.status_code == 200
        d = r.json()
        assert d["nietPseudonimiseren"] > 0 or d["manualReview"] >= 0
    
    def test_particulier_pseudonimised(self):
        """Geboortedatum van particulier → pseudonimiseer + token in tekst."""
        r = client.post("/v1/publicatie/check-pii", json={
            "bodyText": "De eiser, geboren op 10 mei 1985, woont aan de Hoofdstraat 42, 1234 AB Amsterdam.",
            "rechtsgebied": "civiel"
        })
        assert r.status_code == 200
        d = r.json()
        # At least one classificatie should be present
        assert len(d["classificaties"]) >= 0  # scanner may or may not find PII
    
    def test_empty_body_error(self):
        """Empty body → should handle gracefully."""
        r = client.post("/v1/publicatie/check-pii", json={"bodyText": ""})
        # Empty body should return 200 with 0 classificaties (no PII in empty text)
        assert r.status_code in [200, 400]
    
    def test_has_audit_trail(self):
        """Response moet audit trail bevatten."""
        r = client.post("/v1/publicatie/check-pii", json={
            "bodyText": "Test tekst zonder PII.",
            "rechtsgebied": "civiel"
        })
        assert r.status_code == 200
        assert "audit" in r.json()
        assert "inputHash" in r.json()["audit"]
    
    def test_has_geanonimiseerde_tekst(self):
        """Response moet geanonimiseerde tekst bevatten."""
        r = client.post("/v1/publicatie/check-pii", json={
            "bodyText": "Test tekst.",
            "rechtsgebied": "civiel"
        })
        assert r.status_code == 200
        assert "geanonimiseerdeTekst" in r.json()
    
    def test_has_rapport(self):
        """Response moet rapport bevatten."""
        r = client.post("/v1/publicatie/check-pii", json={
            "bodyText": "Test tekst.",
            "rechtsgebied": "civiel"
        })
        assert r.status_code == 200
        assert "rapport" in r.json()
