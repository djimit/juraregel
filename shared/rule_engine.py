"""Small, deterministic evaluator for executable JREM conditions."""

from __future__ import annotations

from typing import Any, Iterable


COMPARISON_OPERATORS = {"eq", "in", "gt", "gte", "lt", "lte"}
METADATA_KEYS = {"periode"}


class RuleEvaluationError(ValueError):
    """Raised when a rule uses condition syntax the evaluator cannot prove."""


def get_value(data: dict, path: str) -> Any:
    value: Any = data
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def matches_value(value: Any, condition: Any) -> bool:
    if condition is None:
        return True
    if isinstance(condition, list):
        return value in condition
    if not isinstance(condition, dict):
        return value == condition

    operators = {key: operand for key, operand in condition.items() if key not in METADATA_KEYS}
    unknown = set(operators) - COMPARISON_OPERATORS
    if unknown:
        raise RuleEvaluationError(f"unsupported condition operator(s): {', '.join(sorted(unknown))}")
    if not operators:
        raise RuleEvaluationError("condition contains metadata but no executable operator")
    if value is None:
        return False

    for operator, operand in operators.items():
        if operator == "eq" and value != operand:
            return False
        if operator == "in" and value not in operand:
            return False
        if operator in {"gt", "gte", "lt", "lte"}:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return False
            if operator == "gt" and not value > operand:
                return False
            if operator == "gte" and not value >= operand:
                return False
            if operator == "lt" and not value < operand:
                return False
            if operator == "lte" and not value <= operand:
                return False
    return True


def rule_matches(rule: dict, facts: dict, *, allow_unconditional: bool = False) -> bool:
    conditions = rule.get("conditions") or {}
    if not conditions:
        return allow_unconditional
    return all(
        matches_value(get_value(facts, field), condition)
        for field, condition in conditions.items()
        if field not in METADATA_KEYS
    )


def select_rule(rules: Iterable[dict], facts: dict) -> dict | None:
    """Return the highest-priority matching executable rule."""
    ordered = sorted(rules, key=lambda rule: rule.get("priority", 0), reverse=True)
    return next((rule for rule in ordered if rule_matches(rule, facts)), None)
