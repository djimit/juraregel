#!/usr/bin/env python3
"""Gate 14: Jurist-acceptatie check. SKIP voor drafts (geen juristAccordering)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from acceptance_metadata import validate_acceptance

def check_acceptatie(jrem_path: str) -> tuple[str, str]:
    """Returns (status, message). status: PASS, FAIL, or SKIP."""
    with open(jrem_path) as f:
        data = json.load(f)
    return validate_acceptance(data)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: acceptatie-check.py <jrem-file>")
        sys.exit(2)
    status, msg = check_acceptatie(sys.argv[1])
    print(f"Gate 14/14: Jurist-acceptatie — {status}: {msg}")
    sys.exit(0 if status != "FAIL" else 1)
