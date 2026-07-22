"""Tests for Agent and Regulatory Monitor auditors."""

from api.assurance.agent_auditor import agent_auditor
from api.assurance.regulatory_monitor_auditor import regulatory_monitor_auditor


# ─── Agent Auditor Tests ──────────────────────────────────────


class TestAgentAuditor:
    def test_successful_agent(self):
        result = {
            "agent": "DPIA Agent",
            "status": "success",
            "confidence": 0.9,
            "trace": [
                {"step": "pre_scan", "status": "complete"},
                {"step": "generate", "status": "complete"},
                {"step": "risk_analysis", "status": "complete"},
            ],
            "citations": [{"source": "AVG Art. 35"}],
            "hallucination_flags": [],
            "recommendations": ["Do X"],
        }
        report = agent_auditor.audit(result, expected_steps=3)
        assert len(report.findings) == 0
        assert report.release_decision == "GO"

    def test_missing_steps(self):
        result = {
            "agent": "Test Agent",
            "status": "success",
            "confidence": 0.9,
            "trace": [{"step": "step1", "status": "complete"}],
            "citations": [{"source": "Art. 5"}],
            "hallucination_flags": [],
            "recommendations": ["Rec"],
        }
        report = agent_auditor.audit(result, expected_steps=4)
        assert any(f.error_type.value == "omissiefout" for f in report.findings)

    def test_high_confidence_low_status(self):
        result = {
            "agent": "Test Agent",
            "status": "partial",
            "confidence": 0.97,
            "trace": [{"step": "s1", "status": "complete"}],
            "citations": [{"source": "Art. 5"}],
            "hallucination_flags": [],
            "recommendations": ["Rec"],
        }
        report = agent_auditor.audit(result, expected_steps=1)
        assert any(f.error_type.value == "interpretatiefout" for f in report.findings)

    def test_hallucination_flag(self):
        result = {
            "agent": "Test Agent",
            "status": "success",
            "confidence": 0.9,
            "trace": [{"step": "s1", "status": "complete"}],
            "citations": [{"source": "Art. 5"}],
            "hallucination_flags": [{"claim": "fake"}],
            "recommendations": ["Rec"],
        }
        report = agent_auditor.audit(result, expected_steps=1)
        assert any(f.severity.value == "S4" for f in report.findings)

    def test_no_citations(self):
        result = {
            "agent": "Test Agent",
            "status": "success",
            "confidence": 0.9,
            "trace": [{"step": "s1", "status": "complete"}],
            "citations": [],
            "hallucination_flags": [],
            "recommendations": ["Rec"],
        }
        report = agent_auditor.audit(result, expected_steps=1)
        assert any(f.error_type.value == "bronfout" for f in report.findings)


# ─── Regulatory Monitor Auditor Tests ─────────────────────────


class TestRegulatoryMonitorAuditor:
    def test_clean_scan(self):
        result = {
            "changes_detected": 2,
            "sources_scanned": 3,
            "changes": [
                {
                    "title": "New regulation",
                    "impact_level": "high",
                    "impact_score": 0.8,
                    "effective_date": "2026-08-01",
                    "affected_frameworks": ["EU AI Act"],
                },
            ],
            "errors": [],
        }
        report = regulatory_monitor_auditor.audit(result)
        assert report.release_decision == "GO"

    def test_scan_with_errors(self):
        result = {
            "changes_detected": 0,
            "sources_scanned": 2,
            "changes": [],
            "errors": ["Timeout", "404"],
        }
        report = regulatory_monitor_auditor.audit(result)
        assert any(f.error_type.value == "procedurefout" for f in report.findings)

    def test_inconsistent_impact(self):
        result = {
            "changes_detected": 1,
            "sources_scanned": 2,
            "changes": [
                {
                    "title": "High impact change",
                    "impact_level": "low",
                    "impact_score": 0.9,
                    "effective_date": "2026-01-01",
                    "affected_frameworks": ["AVG"],
                },
            ],
            "errors": [],
        }
        report = regulatory_monitor_auditor.audit(result)
        assert any(f.error_type.value == "interpretatiefout" for f in report.findings)

    def test_missing_impact_assessment(self):
        result = {
            "changes_detected": 1,
            "sources_scanned": 2,
            "changes": [
                {
                    "title": "Change without impact",
                    "impact_level": None,
                    "impact_score": 0.5,
                    "effective_date": "2026-01-01",
                    "affected_frameworks": ["AVG"],
                },
            ],
            "errors": [],
        }
        report = regulatory_monitor_auditor.audit(result)
        assert any(f.error_type.value == "omissiefout" for f in report.findings)

    def test_outdated_change(self):
        result = {
            "changes_detected": 1,
            "sources_scanned": 2,
            "changes": [
                {
                    "title": "Old change",
                    "impact_level": "high",
                    "impact_score": 0.8,
                    "effective_date": "2022-06-01",
                    "affected_frameworks": ["AVG"],
                },
            ],
            "errors": [],
        }
        report = regulatory_monitor_auditor.audit(result)
        assert any(f.error_type.value == "temporaliteitsfout" for f in report.findings)
