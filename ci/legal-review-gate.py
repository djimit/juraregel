#!/usr/bin/env python3
import glob
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from acceptance_metadata import validate_acceptance, validate_l3_boundary


def _is_strict_maturity(maturity: str) -> bool:
    return (maturity or "").startswith(("L2-", "L3-"))


def main() -> int:
    warn = 0
    fail = 0
    for f in sorted(glob.glob("use-cases/*/jrem/exports/*.json")):
        d = json.load(open(f))
        app = d.get("approval", {})
        maturity = d.get("maturityLevel", "L0-demo")
        strict = _is_strict_maturity(maturity)

        if app.get("type") == "self" and strict:
            print(f"  FAIL: {f} is self-approved at {maturity}")
            fail += 1
        elif app.get("type") == "self":
            print(f"  WARN: {f} is self-approved at {maturity}")
            warn += 1
        elif "juristAccordering" in d:
            print(f"  WARN: {f} still uses old juristAccordering")
            warn += 1

        if strict:
            status, message = validate_acceptance(d, require_extended=True)
            if status != "PASS":
                print(f"  FAIL: {f} {message}")
                fail += 1

        l3_status, l3_message = validate_l3_boundary(d)
        if l3_status == "FAIL":
            print(f"  FAIL: {f} {l3_message}")
            fail += 1

    print(f"Checked all JREM exports: {warn} warnings, {fail} blocking")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
