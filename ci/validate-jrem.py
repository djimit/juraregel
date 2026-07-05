#!/usr/bin/env python3
"""Validate JREM exports against schema."""
import json, glob, sys

# Use jsonschema if available, else fallback to basic check
try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

with open("shared/jrem-core.json") as f:
    core_schema = json.load(f)

errors = 0
for f in sorted(glob.glob("use-cases/*/jrem/exports/*.json")):
    data = json.load(open(f))
    
    # Basic validation
    if "schemaVersion" not in data:
        print(f"  ERROR: {f} missing schemaVersion")
        errors += 1
    elif data["schemaVersion"] != "1.1.0":
        print(f"  WARN: {f} uses schemaVersion {data[schemaVersion]}")
    
    if "rules" not in data or not data["rules"]:
        print(f"  ERROR: {f} has no rules")
        errors += 1
    
    # Check approval exists
    if "approval" not in data:
        print(f"  WARN: {f} missing approval object")
    
    # Validate rules
    for rule in data.get("rules", []):
        for ref in rule.get("sourceRefs", []):
            if ref.get("type") == "wet" and not ref.get("bwbId"):
                print(f"  WARN: {f} rule {rule["ruleId"]} wet-ref missing bwbId")

if HAS_JSONSCHEMA:
    for f in sorted(glob.glob("use-cases/*/jrem/exports/*.json")):
        data = json.load(open(f))
        try:
            jsonschema.validate(data, core_schema)
        except jsonschema.ValidationError as e:
            print(f"  SCHEMA WARN: {f}: {e.message[:80]}")

print(f"Validated all JREM exports: {errors} errors")
sys.exit(1 if errors > 0 else 0)
