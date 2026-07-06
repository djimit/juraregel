import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).with_name("legal-review-gate.py")


def valid_accordering():
    return {
        "geaccondeerdDoor": "Test Jurist",
        "rol": "juridisch eigenaar",
        "organisatie": "Testorganisatie",
        "datum": "2026-07-06",
        "geldigTot": "2099-12-31",
        "versie": "2026.1",
        "scope": "Pilot scope",
        "bronSnapshot": "source-set-2026-07-07",
        "verklaring": "Akkoord binnen scope.",
        "beperkingen": ["Niet buiten scope gebruiken"],
    }


def write_export(root, name, maturity, approval=None, metadata=None):
    path = root / "use-cases" / name / "jrem" / "exports" / f"{name}.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        json.dumps(
            {
                "version": "2026.1",
                "approval": approval or {"type": "self"},
                "maturityLevel": maturity,
                "metadata": metadata or {"acceptatieType": "draft"},
            }
        )
    )


def test_l1_self_approval_is_warning_only(tmp_path):
    write_export(tmp_path, "l1", "L1-poc")

    proc = subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp_path, text=True, capture_output=True)

    assert proc.returncode == 0
    assert "1 warnings, 0 blocking" in proc.stdout


def test_l2_self_approval_blocks_gate(tmp_path):
    write_export(tmp_path, "l2", "L2-pilot")

    proc = subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp_path, text=True, capture_output=True)

    assert proc.returncode == 1
    assert "blocking" in proc.stdout


def test_valid_l2_jurist_acceptance_passes_gate(tmp_path):
    write_export(
        tmp_path,
        "l2",
        "L2-pilot",
        approval={"type": "jurist"},
        metadata={"acceptatieType": "full", "juristAccordering": valid_accordering()},
    )

    proc = subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp_path, text=True, capture_output=True)

    assert proc.returncode == 0
    assert "0 warnings, 0 blocking" in proc.stdout


def test_expired_l2_acceptance_blocks_gate(tmp_path):
    accordering = valid_accordering()
    accordering["geldigTot"] = "2020-01-01"
    write_export(
        tmp_path,
        "l2",
        "L2-pilot",
        approval={"type": "jurist"},
        metadata={"acceptatieType": "full", "juristAccordering": accordering},
    )

    proc = subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp_path, text=True, capture_output=True)

    assert proc.returncode == 1
    assert "Acceptatie verlopen" in proc.stdout


def test_l3_without_indicator_disclaimer_blocks_gate(tmp_path):
    write_export(
        tmp_path,
        "l3",
        "L3-production",
        approval={"type": "jurist"},
        metadata={"acceptatieType": "full", "juristAccordering": valid_accordering()},
    )

    proc = subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp_path, text=True, capture_output=True)

    assert proc.returncode == 1
    assert "indicatorDisclaimer ontbreekt" in proc.stdout


def test_l3_with_indicator_boundary_passes_gate(tmp_path):
    write_export(
        tmp_path,
        "l3",
        "L3-production",
        approval={"type": "jurist"},
        metadata={
            "acceptatieType": "full",
            "juristAccordering": valid_accordering(),
            "indicatorDisclaimer": "Dit is een indicatie, geen besluit.",
            "manualReviewBoundary": "indicator-only",
        },
    )

    proc = subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp_path, text=True, capture_output=True)

    assert proc.returncode == 0
    assert "0 warnings, 0 blocking" in proc.stdout
