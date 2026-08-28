import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "shared"))
sys.path.insert(0, str(ROOT / "ci"))

from rule_engine import select_rule
from source_quality import issues_for_rule


EXPORT = ROOT / "use-cases/classificatie/jrem/exports/classificatie-zaak-intake-2026.1.json"


def load_ruleset():
    return json.loads(EXPORT.read_text())


def test_narrow_classification_slice_is_source_clean():
    ruleset = load_ruleset()
    assert len(ruleset["rules"]) == 3
    assert [issue for rule in ruleset["rules"] for issue in issues_for_rule(rule, ruleset)] == []


def test_article_93_boundary_and_manual_review_paths():
    rules = load_ruleset()["rules"]
    kanton = select_rule(rules, {
        "vorderingType": "geldvordering", "vorderingWaarde": 25000,
        "bijzondereCategorie": "geen",
    })
    above = select_rule(rules, {
        "vorderingType": "geldvordering", "vorderingWaarde": 25000.01,
        "bijzondereCategorie": "geen",
    })
    unknown = select_rule(rules, {"vorderingType": "onbepaalde_waarde"})

    assert kanton["ruleId"] == "CL-2026-001"
    assert kanton["outcome"]["manualReviewRequired"] is False
    assert above["ruleId"] == "CL-2026-003"
    assert above["outcome"]["manualReviewRequired"] is True
    assert unknown["ruleId"] == "CL-2026-002"
    assert unknown["outcome"]["manualReviewRequired"] is True


def test_special_categories_remain_outside_the_pilot():
    assert select_rule(load_ruleset()["rules"], {
        "vorderingType": "geldvordering", "vorderingWaarde": 1000,
        "bijzondereCategorie": "arbeid",
    }) is None
