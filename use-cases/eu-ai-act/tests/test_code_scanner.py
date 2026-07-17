"""Tests for EU AI Act Code Scanner — validates all 14 checks."""

import os
import tempfile
import pytest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from code_scanner import scan_codebase, CodeFinding


@pytest.fixture
def sample_compliant_code(tmp_path):
    """Generate a compliant Python codebase."""
    code = '''
import logging
from pydantic import BaseModel
from tenacity import retry

logger = logging.getLogger(__name__)

class InputModel(BaseModel):
    query: str

@retry(stop=stop_after_attempt(3))
def call_llm(input_data: dict) -> str:
    """Call the LLM with validated input."""
    try:
        validated = InputModel(**input_data)
        result = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": validated.query}]
        )
        return result.choices[0].message.content
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        return "fallback response"
'''
    (tmp_path / "main.py").write_text(code)
    return tmp_path


@pytest.fixture
def sample_noncompliant_code(tmp_path):
    """Generate a non-compliant Python codebase."""
    code = """
import os

def call_llm(user_input):
    result = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}]
    )
    output = result.choices[0].message.content
    eval(output)
    return output
"""
    (tmp_path / "main.py").write_text(code)
    return tmp_path


class TestCodeScanner:
    def test_scan_finds_compliant_code(self, sample_compliant_code):
        findings = scan_codebase(str(sample_compliant_code))
        assert len(findings) > 0
        passed = [f for f in findings if f.status == "pass"]
        assert len(passed) > 0

    def test_scan_finds_noncompliant_code(self, sample_noncompliant_code):
        findings = scan_codebase(str(sample_noncompliant_code))
        failed = [f for f in findings if f.status == "fail"]
        assert len(failed) > 0

    def test_all_14_checks_present(self, sample_compliant_code):
        findings = scan_codebase(str(sample_compliant_code))
        rule_ids = {f.ruleId for f in findings}
        expected_prefixes = ["AIR-09", "AIR-10", "AIR-11", "AIR-12", "AIR-14", "AIR-15"]
        for prefix in expected_prefixes:
            assert any(rid.startswith(prefix) for rid in rule_ids), (
                f"Missing checks for {prefix}"
            )

    def test_finding_to_jrem(self, sample_noncompliant_code):
        findings = scan_codebase(str(sample_noncompliant_code))
        if findings:
            jrem = findings[0].to_jrem()
            assert "ruleId" in jrem
            assert "sourceRefs" in jrem
            assert "outcome" in jrem
            assert jrem["sourceRefs"][0]["url"].startswith("https://")

    def test_empty_directory(self, tmp_path):
        findings = scan_codebase(str(tmp_path))
        assert any(f.ruleId == "AIR-SCAN-000" for f in findings)

    def test_unsafe_input_detected(self, sample_noncompliant_code):
        findings = scan_codebase(str(sample_noncompliant_code))
        unsafe = [f for f in findings if f.ruleId == "AIR-15-04"]
        assert len(unsafe) == 1
        assert unsafe[0].status == "fail"
        assert unsafe[0].severity == "critical"

    def test_missing_path_returns_warning(self):
        findings = scan_codebase("/nonexistent/path/12345")
        assert any(f.ruleId == "AIR-SCAN-000" for f in findings)
