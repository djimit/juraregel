import importlib.util
import json
from pathlib import Path


SCRIPT = Path(__file__).with_name("acceptatie-check.py")
spec = importlib.util.spec_from_file_location("acceptatie_check", SCRIPT)
acceptatie_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acceptatie_check)


def write_jrem(tmp_path, accordering, acceptatie_type="full"):
    path = tmp_path / "sample.json"
    path.write_text(
        json.dumps(
            {
                "version": "2026.1",
                "metadata": {
                    "acceptatieType": acceptatie_type,
                    "juristAccordering": accordering,
                },
            }
        )
    )
    return path


def test_draft_without_accordering_is_skipped(tmp_path):
    path = tmp_path / "draft.json"
    path.write_text(json.dumps({"version": "2026.1", "metadata": {"acceptatieType": "draft"}}))

    status, message = acceptatie_check.check_acceptatie(str(path))

    assert status == "SKIP"
    assert "Draft JREM" in message


def test_full_acceptatie_requires_reviewer(tmp_path):
    path = write_jrem(
        tmp_path,
        {"datum": "2026-07-06", "geldigTot": "2099-12-31", "versie": "2026.1"},
    )

    status, message = acceptatie_check.check_acceptatie(str(path))

    assert status == "FAIL"
    assert "geaccondeerdDoor" in message


def test_full_acceptatie_requires_valid_until(tmp_path):
    path = write_jrem(
        tmp_path,
        {"geaccondeerdDoor": "Test Jurist", "datum": "2026-07-06", "versie": "2026.1"},
    )

    status, message = acceptatie_check.check_acceptatie(str(path))

    assert status == "FAIL"
    assert "geldigTot ontbreekt" in message


def test_full_acceptatie_requires_version_match(tmp_path):
    path = write_jrem(
        tmp_path,
        {
            "geaccondeerdDoor": "Test Jurist",
            "datum": "2026-07-06",
            "geldigTot": "2099-12-31",
            "versie": "2025.1",
        },
    )

    status, message = acceptatie_check.check_acceptatie(str(path))

    assert status == "FAIL"
    assert "komt niet overeen" in message


def test_full_acceptatie_passes_when_required_fields_are_valid(tmp_path):
    path = write_jrem(
        tmp_path,
        {
            "geaccondeerdDoor": "Test Jurist",
            "datum": "2026-07-06",
            "geldigTot": "2099-12-31",
            "versie": "2026.1",
        },
    )

    status, message = acceptatie_check.check_acceptatie(str(path))

    assert status == "PASS"
    assert "Test Jurist" in message
