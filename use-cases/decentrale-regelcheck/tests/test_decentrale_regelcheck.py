import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from decentrale_regelcheck import DecentraleRegelcheckRequest, check_decentrale_regel
from sources.cvdr_sru_connector import CVDRSRUConnector

FIXTURES = ROOT / "sources" / "fixtures"
JREM = Path(__file__).resolve().parents[1] / "jrem" / "exports" / "decentrale-regelcheck-2026.1.json"


def _records():
    return CVDRSRUConnector().normalize((FIXTURES / "cvdr-sru.sample.json").read_text())["records"]


def test_postcode_product_returns_local_regulation_and_authority():
    result = check_decentrale_regel(
        DecentraleRegelcheckRequest("1011 AB", "evenementenvergunning", bestuurslaag="gemeente"),
        _records(),
    )

    assert result["bevoegdGezag"] == "gemeente Amsterdam"
    assert result["regeling"] == "Algemene Plaatselijke Verordening Amsterdam 2008"
    assert result["procedureType"] == "vergunning"
    assert result["manualReviewRequired"] is True
    assert "DRC-006" in result["appliedRules"]
    assert result["sourceRefs"][0]["title"] == "Lokale wet- en regelgeving"


def test_unknown_postcode_product_requires_manual_review():
    result = check_decentrale_regel(
        DecentraleRegelcheckRequest("9999 ZZ", "evenementenvergunning"),
        _records(),
    )

    assert result["matches"] == []
    assert result["manualReviewRequired"] is True
    assert "DRC-009" in result["appliedRules"]


def test_jrem_export_validates_against_shared_schema():
    import jsonschema

    schema = json.loads((ROOT / "shared" / "jrem-schema.json").read_text())
    instance = json.loads(JREM.read_text())
    errors = list(jsonschema.Draft202012Validator(schema).iter_errors(instance))
    assert errors == []


def test_jrem_has_l1_rules_with_source_refs():
    instance = json.loads(JREM.read_text())
    assert len(instance["rules"]) == 9
    assert instance["metadata"]["acceptatieType"] == "draft"
    for rule in instance["rules"]:
        assert rule["ruleId"].startswith("DRC-")
        assert rule["sourceRefs"]
