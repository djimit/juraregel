"""Tests for Integration Validator — OpenMythos × Djimitflo × JLAIF."""

from api.assurance.integration_validator import (
    integration_validator,
    OPENMYTHOS_TO_JLAIF,
    NEDERUS_TO_JLAIF,
)


class TestIntegrationValidator:
    def test_validate_all_runs(self):
        report = integration_validator.validate_all()
        assert report.total_checks > 0
        assert report.pass_rate > 0.8

    def test_openmythos_coverage(self):
        report = integration_validator.validate_all()
        assert report.coverage["openmythos"] >= 0.9

    def test_nederus_coverage(self):
        report = integration_validator.validate_all()
        assert report.coverage["nederus"] >= 0.9

    def test_all_openmythos_categories_mapped(self):
        expected_categories = {
            "hierarchy",
            "injection",
            "tool-scope",
            "value-alignment",
            "calibration",
            "hallucination",
            "temporal-reasoning",
            "cross-lingual",
            "contradiction",
            "dpia-completeness",
            "fria-coverage",
            "evidence-linking",
            "bias-detection",
            "proportionality",
            "data-minimization",
            "security",
            "transparency",
            "accountability",
        }
        mapped = set(OPENMYTHOS_TO_JLAIF.keys())
        assert expected_categories.issubset(mapped)

    def test_all_nederus_controls_mapped(self):
        expected_controls = {"NED-01", "NED-02", "NED-03", "NED-04", "NED-05"}
        mapped = set(NEDERUS_TO_JLAIF.keys())
        assert expected_controls.issubset(mapped)

    def test_error_types_valid(self):
        valid_types = {
            "feitelijke_fout",
            "bronfout",
            "interpretatiefout",
            "jurisdictiefout",
            "temporaliteitsfout",
            "procedurefout",
            "omissiefout",
            "bias_ongelijke_behandeling",
            "vertrouwelijkheidsincident",
        }
        for category, mapping in OPENMYTHOS_TO_JLAIF.items():
            for error_type in mapping.get("error_types", []):
                assert error_type in valid_types, f"Invalid error type: {error_type}"

    def test_severity_levels_valid(self):
        valid_severities = {"S1", "S2", "S3", "S4", "S5"}
        for category, mapping in OPENMYTHOS_TO_JLAIF.items():
            for sev in mapping.get("severity_range", []):
                assert sev in valid_severities, f"Invalid severity: {sev}"

    def test_cross_references_exist(self):
        for category, mapping in OPENMYTHOS_TO_JLAIF.items():
            ned_controls = mapping.get("ned_controls", [])
            assert len(ned_controls) > 0, f"Category '{category}' has no NED controls"

    def test_ned_evidence_specified(self):
        for control_id, mapping in NEDERUS_TO_JLAIF.items():
            evidence = mapping.get("evidence", [])
            assert len(evidence) > 0, (
                f"Control '{control_id}' has no evidence requirements"
            )

    def test_no_critical_failures(self):
        report = integration_validator.validate_all()
        critical_failures = [
            c for c in report.checks if c.severity == "error" and not c.passed
        ]
        assert len(critical_failures) == 0, (
            f"Critical failures: {[c.check_id for c in critical_failures]}"
        )

    def test_overall_coverage_above_90(self):
        report = integration_validator.validate_all()
        assert report.coverage["overall"] >= 0.90
