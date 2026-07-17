"""Covenant — YAML policy DSL for agent action enforcement.

Precedence: forbid > require_approval > permit > default_deny.
"""

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Optional

import yaml


class Covenant:
    """Defines what an agent is allowed to do."""

    def __init__(self, agent: str, version: str, rules: list, description: str = ""):
        self.agent = agent
        self.version = version
        self.description = description
        self.rules = rules
        self._hash = None

    @classmethod
    def from_yaml(cls, path: str) -> "Covenant":
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> "Covenant":
        return cls(
            agent=data.get("agent", "unknown"),
            version=data.get("version", "1.0"),
            description=data.get("description", ""),
            rules=data.get("rules", []),
        )

    @property
    def hash(self) -> str:
        if self._hash is None:
            canonical = json.dumps(
                {"agent": self.agent, "version": self.version, "rules": self.rules},
                sort_keys=True,
            )
            self._hash = hashlib.sha256(canonical.encode()).hexdigest()[:16]
        return self._hash

    def evaluate(self, action_name: str, context: dict = None) -> dict:
        """Evaluate an action against the covenant.

        Returns: {decision: permit|require_approval|forbid, rule_matched: str, condition: str}
        """
        context = context or {}

        # Check forbid first (highest precedence)
        for rule in self.rules:
            if "forbid" in rule:
                action = rule["forbid"]
                if self._action_matches(action_name, action):
                    if self._condition_matches(rule.get("when"), context):
                        return {
                            "decision": "forbid",
                            "rule_matched": f"forbid {action}",
                            "condition": rule.get("when", ""),
                        }

        # Check require_approval
        for rule in self.rules:
            if "require_approval" in rule:
                action = rule["require_approval"]
                if self._action_matches(action_name, action):
                    if self._condition_matches(rule.get("when"), context):
                        return {
                            "decision": "require_approval",
                            "rule_matched": f"require_approval {action}",
                            "condition": rule.get("when", ""),
                        }

        # Check permit
        for rule in self.rules:
            if "permit" in rule:
                action = rule["permit"]
                if self._action_matches(action_name, action):
                    if self._condition_matches(rule.get("when"), context):
                        return {
                            "decision": "permit",
                            "rule_matched": f"permit {action}",
                            "condition": rule.get("when", ""),
                        }

        # Default deny
        return {"decision": "forbid", "rule_matched": "default_deny", "condition": ""}

    def _action_matches(self, actual: str, pattern: str) -> bool:
        if pattern == actual:
            return True
        if pattern.endswith("*"):
            return actual.startswith(pattern[:-1])
        if pattern.startswith("*"):
            return actual.endswith(pattern[1:])
        return False

    def _condition_matches(self, condition: Optional[str], context: dict) -> bool:
        if not condition:
            return True
        try:
            for key, value in context.items():
                condition = condition.replace(key, repr(value))
            return eval(condition, {"__builtins__": {}}, {})
        except Exception:
            return True


def load_covenant(path: str) -> Covenant:
    return Covenant.from_yaml(path)
