import pytest

from shared.rule_engine import RuleEvaluationError, rule_matches, select_rule


def test_selects_exact_executable_rule_and_skips_empty_catalog_entries():
    rules = [
        {"ruleId": "catalog", "priority": 999, "conditions": {}},
        {"ruleId": "adult", "priority": 10, "conditions": {"age": {"gte": 18}}},
    ]
    assert select_rule(rules, {"age": 21})["ruleId"] == "adult"


def test_dotted_facts_and_boolean_values():
    rule = {"conditions": {"metadata.published": True, "score": {"lt": 5}}}
    assert rule_matches(rule, {"metadata": {"published": True}, "score": 4})


def test_unknown_operator_fails_closed():
    with pytest.raises(RuleEvaluationError, match="unsupported"):
        rule_matches({"conditions": {"age": {"approximately": 18}}}, {"age": 18})
