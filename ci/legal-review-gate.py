#!/usr/bin/env python3
import glob
import json
import sys

STRICT_MATURITY = {"L2-pilot", "L3-production"}


def main() -> int:
    warn = 0
    fail = 0
    for f in sorted(glob.glob("use-cases/*/jrem/exports/*.json")):
        d = json.load(open(f))
        app = d.get("approval", {})
        maturity = d.get("maturityLevel", "L0-demo")
        if app.get("type") == "self" and maturity in STRICT_MATURITY:
            print(f"  FAIL: {f} is self-approved at {maturity}")
            fail += 1
        elif app.get("type") == "self":
            print(f"  WARN: {f} is self-approved at {maturity}")
            warn += 1
        elif "juristAccordering" in d:
            print(f"  WARN: {f} still uses old juristAccordering")
            warn += 1

    print(f"Checked all JREM exports: {warn} warnings, {fail} blocking")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
