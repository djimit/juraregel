import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from sources.woo_diwoo_connector import WooDiWooConnector
from woo_publicatieplicht_preflight import WooPreflightRequest, check_woo_publicatieplicht

FIXTURES = ROOT / "sources" / "fixtures"
JREM = Path(__file__).resolve().parents[1] / "jrem" / "exports" / "woo-publicatieplicht-preflight-2026.1.json"


def _documents():
    return WooDiWooConnector().normalize((FIXTURES / "woo-diwoo.sample.json").read_text())["documents"]


def test_complete_woo_metadata_passes_preflight():
    result = check_woo_publicatieplicht(
        WooPreflightRequest("gemeente Amsterdam", "beschikking"),
        _documents(),
    )

    assert result["documentFound"] is True
    assert result["missingMetadata"] == []
    assert result["manualReviewRequired"] is False
    assert {"WOO-002", "WOO-003", "WOO-004", "WOO-005", "WOO-006"}.issubset(result["appliedRules"])


def test_live_woo_category_plural_matches_document_type():
    documents = [{
        "organisatie": "gemeente amsterdam",
        "organisatieLabel": "Gemeente Amsterdam",
        "documentType": "beschikkingen",
        "documentTypeLabel": "Beschikkingen",
        "location": "https://zoek.officielebekendmakingen.nl/resultaten?q=beschikking",
        "metadata": {
            "tooiCode": "gm0363",
            "documentType": "beschikkingen",
            "publishedAt": "2026-07-01",
            "sourceUrl": "https://zoek.officielebekendmakingen.nl/resultaten?q=beschikking",
        },
        "sourceRefs": [{"title": "Woo-index", "url": "https://organisaties.overheid.nl/woo/25698/Gemeente_Amsterdam"}],
    }]

    result = check_woo_publicatieplicht(WooPreflightRequest("gemeente Amsterdam", "beschikking"), documents)

    assert result["documentFound"] is True
    assert result["missingMetadata"] == []


def test_missing_diwoo_metadata_requires_manual_review():
    result = check_woo_publicatieplicht(
        WooPreflightRequest("gemeente Amsterdam", "convenant"),
        _documents(),
    )

    assert result["documentFound"] is True
    assert set(result["missingMetadata"]) == {"tooiCode", "publishedAt"}
    assert result["manualReviewRequired"] is True
    assert "WOO-007" in result["appliedRules"]


def test_unknown_document_type_requires_manual_review():
    result = check_woo_publicatieplicht(
        WooPreflightRequest("gemeente Amsterdam", "subsidiebesluit"),
        _documents(),
    )

    assert result["documentFound"] is False
    assert result["manualReviewRequired"] is True
    assert "WOO-008" in result["appliedRules"]


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
        assert rule["ruleId"].startswith("WOO-")
        assert rule["sourceRefs"]
