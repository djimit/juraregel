#!/usr/bin/env python3
import json, glob, sys, os

CI_MODE = os.environ.get("JURAREGEL_CI_MODE", "poc").lower()
STRICT_SCHEMA = CI_MODE in ("pilot", "production")
STRICT_LEGAL = CI_MODE in ("pilot", "production")
NON_BWB_WET_REFS = {"AVG", "EU AI Act"}

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
        if STRICT_SCHEMA:
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
                if ref.get("title") in NON_BWB_WET_REFS:
                    continue
                print("  WARN: {} rule {} wet-ref missing bwbId".format(f, rid))
                warnings += 1

if HAS_JSONSCHEMA:
    for f in sorted(glob.glob("use-cases/*/jrem/exports/*.json")):
        data = json.load(open(f))
        try:
            jsonschema.validate(data, core_schema)
        except jsonschema.ValidationError as e:
            msg = "  {}: {}".format(f, e.message[:80])
            if STRICT_SCHEMA:
                print("ERROR" + msg)
                errors += 1
            else:
                print("WARN" + msg)
                warnings += 1

        maturity = data.get("maturityLevel", "L0-demo")
        approval = data.get("approval", {})
        approval_type = approval.get("type", "none")
        for rule in data.get("rules", []):
            rid = rule.get("ruleId", "?")

            # L2+ requires independent review
            if maturity in ("L2-pilot", "L3-production") and approval_type == "self":
                print("  ERROR: {} rule {} maturity {} requires independent review".format(f, rid, maturity))
                errors += 1

            # L2+ requires approval object
            if maturity in ("L2-pilot", "L3-production") and not approval:
                print("  ERROR: {} rule {} maturity {} requires approval object".format(f, rid, maturity))
                errors += 1

print("Validated: {} errors, {} warnings".format(errors, warnings))
print("CI mode: {}".format(CI_MODE))
sys.exit(1 if errors > 0 else 0)
