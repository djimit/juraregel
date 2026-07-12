#!/usr/bin/env python3
"""Validate or generate OpenAPI directly from the actual FastAPI apps."""

import argparse
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared"))


def schemas() -> dict[str, dict]:
    result = {}
    for app_path in sorted(ROOT.glob("use-cases/*/api/app.py")):
        domain = app_path.parents[1].name
        spec = importlib.util.spec_from_file_location(f"openapi_{domain.replace('-', '_')}", app_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result[domain] = module.app.openapi()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="Optional generated artifact directory")
    args = parser.parse_args()
    result = schemas()
    if args.output:
        args.output.mkdir(parents=True, exist_ok=True)
        for domain, schema in result.items():
            (args.output / f"{domain}.json").write_text(json.dumps(schema, indent=2))
    print(f"OpenAPI: {len(result)} application schema(s) valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
