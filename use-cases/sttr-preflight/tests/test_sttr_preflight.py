import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from sources.sttr_rtr_connector import STTRRTRConnector
from sttr_preflight import STTRPreflightRequest, check_sttr_package

FIXTURES = ROOT / "sources" / "fixtures"
JREM = Path(__file__).resolve().parents[1] / "jrem" / "exports" / "sttr-preflight-2026.1.json"


def _packages():
    return STTRRTRConnector().normalize((FIXTURES / "sttr-rtr.sample.json").read_text())["packages"]


def test_valid_sttr_package_passes_preflight():
    result = check_sttr_package(STTRPreflightRequest("evenement-melding-amsterdam"), _packages())

    assert result["packageFound"] is True
    assert result["sttrVersionFit"] is True
    assert result["imtrVersionFit"] is True
    assert result["rtrVersionFit"] is True
    assert result["jremMappingFit"] is True
    assert result["manualReviewRequired"] is False
    assert {"STTR-002", "STTR-003", "STTR-004", "STTR-005"}.issubset(result["appliedRules"])


def test_legacy_sttr_package_requires_manual_review():
    result = check_sttr_package(STTRPreflightRequest("kapvergunning-legacy"), _packages())

    assert result["packageFound"] is True
    assert result["sttrVersionFit"] is False
    assert result["imtrVersionFit"] is False
    assert result["jremMappingFit"] is False
    assert result["manualReviewRequired"] is True
    assert "STTR-006" in result["appliedRules"]
    assert "STTR-007" in result["appliedRules"]


def test_unknown_package_requires_manual_review():
    result = check_sttr_package(STTRPreflightRequest("onbekend"), _packages())

    assert result["packageFound"] is False
    assert result["manualReviewRequired"] is True
    assert result["appliedRules"] == ["STTR-008"]


def test_missing_rtr_version_blocks_preflight():
    packages = [{
        "packageId": "zonder-rtr",
        "packageLabel": "zonder-rtr",
        "sttrVersion": "3.0.1",
        "imtrVersion": "3.0.1",
        "rtrVersion": "",
        "status": "metadata-only",
        "issues": [],
        "jremMapping": {"mappedRuleIds": ["DRC-001"]},
        "sourceRefs": [],
    }]

    result = check_sttr_package(STTRPreflightRequest("zonder-rtr"), packages)

    assert result["rtrVersionFit"] is False
    assert result["manualReviewRequired"] is True
    assert "RTR-versie ontbreekt." in result["manualReviewReason"]


def test_missing_mapped_rule_ids_blocks_preflight():
    packages = [{
        "packageId": "zonder-mapping",
        "packageLabel": "zonder-mapping",
        "sttrVersion": "3.0.1",
        "imtrVersion": "3.0.1",
        "rtrVersion": "2026.1",
        "status": "metadata-only",
        "issues": [],
        "jremMapping": {"mappedRuleIds": []},
        "sourceRefs": [],
    }]

    result = check_sttr_package(STTRPreflightRequest("zonder-mapping"), packages)

    assert result["jremMappingFit"] is False
    assert result["manualReviewRequired"] is True
    assert "STTR-007" in result["appliedRules"]


def test_jrem_export_validates_against_shared_schema():
    import jsonschema

    schema = json.loads((ROOT / "shared" / "jrem-schema.json").read_text())
    instance = json.loads(JREM.read_text())
    errors = list(jsonschema.Draft202012Validator(schema).iter_errors(instance))
    assert errors == []


def test_jrem_has_l1_rules_with_source_refs():
    instance = json.loads(JREM.read_text())
    assert len(instance["rules"]) == 8
    assert instance["metadata"]["acceptatieType"] == "draft"
    for rule in instance["rules"]:
        assert rule["ruleId"].startswith("STTR-")
        assert rule["sourceRefs"]
