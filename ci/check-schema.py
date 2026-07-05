#!/usr/bin/env python3
import json, sys
with open("shared/jrem-core.json") as f:
    json.load(f)
print("Core schema OK")
with open("shared/jrem-schema-v1.1.0.json") as f:
    json.load(f)
print("v1.1.0 schema OK")
