import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from dienstverlening_engine import DienstverleningRequest, check_dienstverlening
from sources.tooi_roo_connector import TOOIROOConnector
from sources.upl_connector import UPLConnector

FIXTURES = ROOT / "sources" / "fixtures"
JREM = Path(__file__).resolve().parents[1] / "jrem" / "exports" / "dienstverlening-check-2026.1.json"


def _data():
    products = UPLConnector().normalize((FIXTURES / "upl-actueel.sample.json").read_text())["products"]
    organisations = TOOIROOConnector().normalize((FIXTURES / "tooi-roo.sample.json").read_text())["organisations"]
    return products, organisations


def test_gemeente_product_matches_bestuurslaag():
    products, organisations = _data()
    result = check_dienstverlening(
        DienstverleningRequest("gemeente Amsterdam", "evenementenvergunning", "gemeente"),
        products,
        organisations,
    )

    assert result["uniformeProductnaam"] == "evenementenvergunning"
    assert result["organisatie"] == "gemeente Amsterdam"
    assert result["bestuurslaagfit"] is True
    assert result["signals"]["sdg"] is True
    assert result["manualReviewRequired"] is False
    assert {"DVC-001", "DVC-002", "DVC-006", "DVC-007"}.issubset(set(result["appliedRules"]))
    assert len(result["sourceRefs"]) >= 2


def test_product_bestuurslaag_mismatch_requires_manual_review():
    products, organisations = _data()
    result = check_dienstverlening(
        DienstverleningRequest("provincie Noord-Holland", "evenementenvergunning", "provincie"),
        products,
        organisations,
    )

    assert result["bestuurslaagfit"] is False
    assert result["manualReviewRequired"] is True
    assert "DVC-009" in result["appliedRules"]


def test_unknown_organisation_requires_manual_review():
    products, organisations = _data()
    result = check_dienstverlening(
        DienstverleningRequest("gemeente Atlantis", "evenementenvergunning", "gemeente"),
        products,
        organisations,
    )

    assert result["manualReviewRequired"] is True
    assert "Organisatie niet gevonden" in result["manualReviewReason"]


def test_jrem_export_validates_against_shared_schema():
    import jsonschema

    schema = json.loads((ROOT / "shared" / "jrem-schema.json").read_text())
    instance = json.loads(JREM.read_text())
    errors = list(jsonschema.Draft202012Validator(schema).iter_errors(instance))
    assert errors == []


def test_jrem_has_10_l1_rules_with_source_refs():
    instance = json.loads(JREM.read_text())
    assert len(instance["rules"]) == 10
    assert instance["metadata"]["acceptatieType"] == "draft"
    for rule in instance["rules"]:
        assert rule["ruleId"].startswith("DVC-")
        assert rule["sourceRefs"]
