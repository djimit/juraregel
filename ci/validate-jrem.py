#!/usr/bin/env python3
import json, glob, sys, os

CI_MODE = os.environ.get("JURAREGEL_CI_MODE", "pooc")
STRICT = CI_MODE == "pooc"

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

with open("shared/jrem-core.json") as f:
    core_schema = json.load(f)

errors = 0
warnings = 0

for f in sorted(glob.glob("use-cases/*/jrem/exports/*.json")):
    data = json.load(open(f))

    if "schemaVersion" not in data:
        print("  ERROR: {} missing schemaVersion".format(f))
        errors += 1
    elif data.get("schemaVersion") != "1.1.0":
        msg = "  {}: uses schemaVersion {}".format(f, data.get("schemaVersion"))
        if STRICT:
            print("ERROR" + msg)
            errors += 1
        else:
            print("WARN" + msg)
            warnings += 1

    if not data.get("rules"):
        print("  ERROR: {} has no rules".format(f))
        errors += 1

    if "approval" not in data:
        print("  WARN: {} missing approval object".format(f))
        warnings += 1

    for rule in data.get("rules", []):
        rid = rule.get("ruleId", "?")
        for ref in rule.get("sourceRefs", []):
            if ref.get("type") == "wet" and not ref.get("bwbId"):
                print("  WARN: {} rule {} wet-ref missing bwbId".format(f, rid))

if HAS_JSONSCHEMA:
    for f in sorted(glob.glob("use-cases/*/jrem/exports/*.json")):
        data = json.load(open(f))
        try:
            jsonschema.validate(data, core_schema)
        except jsonschema.ValidationError as e:
            msg = "  {}: {}".format(f, e.message[:80])
            if STRICT:
                print("ERROR" + msg)
                errors += 1
            else:
                print("WARN" + msg)
                warnings += 1

print("Validated: {} errors, {} warnings".format(errors, warnings))
print("CI mode: {}".format(CI_MODE))
sys.exit(1 if errors > 0 else 0)
