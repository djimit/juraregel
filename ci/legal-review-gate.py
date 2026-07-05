#!/usr/bin/env python3
import json, glob, sys

warn = 0
for f in sorted(glob.glob("use-cases/*/jrem/exports/*.json")):
    d = json.load(open(f))
    app = d.get("approval", {})
    if app.get("type") == "self":
        print(f"  WARN: {f} is self-approved")
        warn += 1
    elif "juristAccordering" in d:
        print(f"  WARN: {f} still uses old juristAccordering")
        warn += 1

print(f"Checked all JREM exports: {warn} need review")
sys.exit(1 if warn > 0 else 0)
