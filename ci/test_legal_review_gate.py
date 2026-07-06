import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).with_name("legal-review-gate.py")


def write_export(root, name, maturity):
    path = root / "use-cases" / name / "jrem" / "exports" / f"{name}.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"approval": {"type": "self"}, "maturityLevel": maturity}))


def test_l1_self_approval_is_warning_only(tmp_path):
    write_export(tmp_path, "l1", "L1-poc")

    proc = subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp_path, text=True, capture_output=True)

    assert proc.returncode == 0
    assert "1 warnings, 0 blocking" in proc.stdout


def test_l2_self_approval_blocks_gate(tmp_path):
    write_export(tmp_path, "l2", "L2-pilot")

    proc = subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp_path, text=True, capture_output=True)

    assert proc.returncode == 1
    assert "0 warnings, 1 blocking" in proc.stdout
