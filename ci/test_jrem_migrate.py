import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "jrem-migrate.py"
SPEC = importlib.util.spec_from_file_location("jrem_migrate", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_migration_does_not_invent_source_dates_from_ruleset_validity():
    data = {
        "schemaVersion": "1.0.0",
        "validFrom": "2026-01-01",
        "rules": [{"sourceRefs": [{"type": "standaard", "title": "Bron"}]}],
    }

    migrated = MODULE.migrate_v1_0_to_v1_1(data)

    assert migrated["schemaVersion"] == "1.1.0"
    assert "bronVersie" not in migrated["rules"][0]["sourceRefs"][0]
    assert "bronDatum" not in migrated["rules"][0]["sourceRefs"][0]


def test_validation_reports_missing_legal_identifier_and_provenance():
    issues = MODULE.validate_migration({
        "schemaVersion": "1.1.0",
        "rules": [{"ruleId": "R-1", "sourceRefs": [{"type": "wet"}]}],
    })

    assert issues == [
        "Rule R-1: wet-type sourceRef missing bwbId",
        "Rule R-1: sourceRef missing provenance date",
    ]
