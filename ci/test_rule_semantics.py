import importlib.util
from pathlib import Path


path = Path(__file__).with_name("validate-rule-semantics.py")
spec = importlib.util.spec_from_file_location("validate_rule_semantics", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_executable_rule_semantics_are_consistent():
    assert module.validate() == []
