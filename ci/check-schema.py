#!/usr/bin/env python3
import json

import jsonschema


for path in ("shared/jrem-core.json", "shared/jrem-schema-v1.1.0.json"):
    with open(path) as schema_file:
        schema = json.load(schema_file)
    jsonschema.Draft202012Validator.check_schema(schema)
    print(f"Schema OK: {path}")
