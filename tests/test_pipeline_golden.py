"""Tests for JLAIF Pipeline (Fase B) and Golden Standard (Fase A)."""

from dataclasses import dataclass

from api.assurance.pipeline import (
    JLAIFPipeline,
    PipelineState,
    ModuleCategory,
)
from api.assurance.pipeline_modules import (
    PIIRedactionModule,
    JurisdictionModule,
    CitationModule,
    TemporalModule,
    SeverityScoringModule,
    ReleaseGateModule,
)
from api.assurance.golden_standard import GoldenStandardDataset


# ─── Pipeline Tests ───────────────────────────────────────────


class TestJLAIFPipeline:
    def test_register_module(self):
        pipeline = JLAIFPipeline("test")
        module = PIIRedactionModule()
        pipeline.register(module)
        assert len(pipeline.get_registered_modules()) == 1

    def test_register_bulk(self):
        pipeline = JLAIFPipeline("test")
        pipeline.register_bulk(
            PIIRedactionModule(),
            JurisdictionModule(),
            CitationModule(),
        )
        assert len(pipeline.get_registered_modules()) == 3

    def test_module_ordering(self):
        pipeline = JLAIFPipeline("test")
        pipeline.register_bulk(
            CitationModule(priority=30),
            PIIRedactionModule(priority=10),
            JurisdictionModule(priority=20),
        )
        modules = pipeline.get_registered_modules()
        priorities = [m["priority"] for m in modules]
        assert priorities == sorted(priorities)

    def test_execute_pipeline_clean(self):
        pipeline = JLAIFPipeline("test-clean")
        pipeline.register_bulk(
            PIIRedactionModule(),
            JurisdictionModule(),
            CitationModule(),
            TemporalModule(),
            SeverityScoringModule(),
            ReleaseGateModule(),
        )
        report = pipeline.execute(
            "Conform artikel 5 AVG worden persoonsgegevens rechtmatig verwerkt.",
            context={"expected_jurisdiction": "nederland", "autonomy_level": 2},
        )
        assert report.modules_executed == 6
        assert report.modules_failed == 0

    def test_execute_pipeline_with_pii(self):
        pipeline = JLAIFPipeline("test-pii")
        pipeline.register_bulk(
            PIIRedactionModule(),
            SeverityScoringModule(),
            ReleaseGateModule(),
        )
        report = pipeline.execute(
            "Patiënt BSN 123456789 heeft recht op inzage.",
            context={"expected_jurisdiction": "nederland", "autonomy_level": 2},
        )
        assert report.release_decision == "NO-GO"
        assert report.total_findings > 0

    def test_critical_module_stops_pipeline(self):
        pipeline = JLAIFPipeline("test-critical")

        @dataclass
        class FailingCriticalModule:
            name: str = "failing-critical"
            priority: int = 50
            category: ModuleCategory = ModuleCategory.POSTPROCESSING
            critical: bool = True

            def execute(self, state):
                raise RuntimeError("Critical failure")

        pipeline.register_bulk(
            PIIRedactionModule(),
            FailingCriticalModule(),
        )
        report = pipeline.execute("Test text", context={})
        assert report.modules_failed == 1
        assert report.modules_executed == 1  # Only PII module ran

    def test_pipeline_report_structure(self):
        pipeline = JLAIFPipeline("test-report")
        pipeline.register_bulk(
            PIIRedactionModule(),
            ReleaseGateModule(),
        )
        report = pipeline.execute("Test", context={})
        assert report.pipeline_id.startswith("pipe-")
        assert report.timestamp
        assert isinstance(report.findings_by_category, dict)
        assert isinstance(report.severity_distribution, dict)


# ─── Golden Standard Tests ────────────────────────────────────


class TestGoldenStandard:
    def test_load_dataset(self):
        gs = GoldenStandardDataset()
        texts = gs.get_all_texts()
        assert len(texts) >= 5

    def test_get_text(self):
        gs = GoldenStandardDataset()
        text = gs.get_text("GS-001")
        assert text is not None
        assert text.domain == "bestuursrecht"

    def test_add_annotation(self):
        gs = GoldenStandardDataset()
        ann = {
            "annotator_id": "jurist-1",
            "text_id": "GS-001",
            "error_type": "bronfout",
            "present": True,
            "severity": "S3",
            "evidence": "Geen artikelverwijzing",
            "confidence": 0.9,
        }
        assert gs.add_annotation("GS-001", ann)

    def test_consensus_findings(self):
        gs = GoldenStandardDataset()
        # Add 2 annotations for same error type
        for annotator in ["jurist-1", "jurist-2"]:
            gs.add_annotation(
                "GS-001",
                {
                    "annotator_id": annotator,
                    "text_id": "GS-001",
                    "error_type": "bronfout",
                    "present": True,
                    "severity": "S3",
                    "evidence": "Geen bron",
                    "confidence": 0.8,
                },
            )
        text = gs.get_text("GS-001")
        consensus = text.consensus_findings
        assert len(consensus) > 0
        assert consensus[0]["type"] == "bronfout"

    def test_cohens_kappa(self):
        gs = GoldenStandardDataset()
        # Add matching annotations
        for annotator in ["jurist-1", "jurist-2"]:
            gs.add_annotation(
                "GS-001",
                {
                    "annotator_id": annotator,
                    "text_id": "GS-001",
                    "error_type": "bronfout",
                    "present": True,
                    "severity": "S3",
                    "evidence": "Geen bron",
                    "confidence": 0.8,
                },
            )
        result = gs.compute_cohens_kappa("GS-001", "jurist-1", "jurist-2")
        assert result.agreement_rate == 1.0
        assert result.cohens_kappa >= 0.0

    def test_confusion_matrix(self):
        gs = GoldenStandardDataset()
        text = gs.get_text("GS-001")
        text.jlaif_result = {"findings": [{"type": "bronfout", "severity": "S3"}]}
        matrix = gs.compute_confusion_matrix("GS-001")
        assert isinstance(matrix, dict)

    def test_f1_per_type(self):
        gs = GoldenStandardDataset()
        f1 = gs.compute_f1_per_type()
        assert isinstance(f1, dict)
        assert len(f1) == 9  # 9 error types


# ─── Pipeline Module Tests ────────────────────────────────────


class TestPipelineModules:
    def test_pii_module(self):
        module = PIIRedactionModule()
        state = PipelineState(
            input_text="BSN: 123456789, email: test@test.nl",
            context={},
        )
        result = module.execute(state)
        assert result.success
        assert len(result.findings) > 0

    def test_jurisdiction_module(self):
        module = JurisdictionModule()
        state = PipelineState(
            input_text="De EU AI Act vereist risicobeheer.",
            context={"expected_jurisdiction": "eu"},
        )
        result = module.execute(state)
        assert result.success

    def test_citation_module(self):
        module = CitationModule()
        state = PipelineState(
            input_text="Persoonsgegevens moeten worden beschermd.",
            context={},
        )
        result = module.execute(state)
        assert result.success

    def test_temporal_module(self):
        module = TemporalModule()
        state = PipelineState(
            input_text="De Privacyrichtlijn 1995 is van toepassing.",
            context={},
        )
        result = module.execute(state)
        assert result.success
        assert len(result.findings) > 0

    def test_severity_scoring_module(self):
        module = SeverityScoringModule()
        state = PipelineState(
            input_text="Test",
            context={},
        )
        state.add_finding({"type": "bronfout", "severity": "S3"})
        result = module.execute(state)
        assert result.success
        assert result.metrics["weighted_score"] > 0

    def test_release_gate_module(self):
        module = ReleaseGateModule()
        state = PipelineState(
            input_text="Test",
            context={"autonomy_level": 2},
        )
        result = module.execute(state)
        assert result.success
        assert result.metrics["decision"] in ("GO", "NO-GO", "CONDITIONAL")
