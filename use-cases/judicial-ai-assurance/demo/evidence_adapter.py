#!/usr/bin/env python3
"""Normalize exported OpenMythos and Djimitflo evidence without judging admission."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


FAILED_RUN_STATES = {"cancelled", "error", "failed"}


def artifact_hash(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def evidence_bundle_hash(paths: list[Path]) -> str:
    manifest = [{"name": path.name, "hash": artifact_hash(path)} for path in paths]
    payload = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(payload.encode()).hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def adapt_openmythos(
    run_path: Path,
    oracle_path: Path | None = None,
    run_id: str | None = None,
) -> dict:
    cases = read_jsonl(run_path)
    if not cases:
        raise ValueError("OpenMythos export contains no cases")

    oracles = read_jsonl(oracle_path) if oracle_path else []
    case_ids = [item.get("case_id") for item in cases]
    oracle_ids = [item.get("case_id") for item in oracles]
    if None in case_ids or len(case_ids) != len(set(case_ids)):
        raise ValueError("OpenMythos run case ids must be present and unique")
    if None in oracle_ids or len(oracle_ids) != len(set(oracle_ids)):
        raise ValueError("OpenMythos oracle case ids must be present and unique")
    unknown_oracles = sorted(set(oracle_ids) - set(case_ids))
    if unknown_oracles:
        raise ValueError(f"Oracle refers to unknown run cases: {unknown_oracles}")
    applicable = [item for item in oracles if item.get("oracle_applicable") is True]
    oracle_failures = [item for item in applicable if item.get("oracle_pass") is False]
    transport_failures = [item for item in cases if item.get("error")]
    categories = sorted({str(item.get("category")) for item in cases if item.get("category")})
    models = sorted({str(item.get("model")) for item in cases if item.get("model")})
    artifact_types = ["independent-evaluation"]
    if "injection" in categories:
        artifact_types.append("indirect-prompt-injection-tests")

    status = "failed" if oracle_failures or transport_failures else "observed"
    model_label = ", ".join(models) if models else "unknown model"
    summary = (
        f"OpenMythos export for {model_label}: {len(cases)} cases, "
        f"{len(applicable)} applicable oracle checks, "
        f"{len(oracle_failures)} oracle failures, {len(transport_failures)} transport failures."
    )
    record = {
        "sourceSystem": "openmythos",
        "status": status,
        "artifactRef": "bundle:" + "+".join(
            path.name for path in [run_path, oracle_path] if path is not None
        ),
        "summary": summary,
        "artifactTypes": artifact_types,
        "artifactHash": evidence_bundle_hash(
            [path for path in [run_path, oracle_path] if path is not None]
        ),
    }
    if run_id:
        record["runId"] = run_id
    return record


def _decode_json_field(value: object, default: object) -> object:
    if not isinstance(value, str) or not value:
        return value if value is not None else default
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return default


def adapt_djimitflo(export_path: Path) -> dict:
    payload = json.loads(export_path.read_text())
    if isinstance(payload, list):
        if len(payload) != 1:
            raise ValueError("Djimitflo export must contain exactly one run")
        payload = payload[0]
    if not isinstance(payload, dict) or not payload.get("id"):
        raise ValueError("Djimitflo export has no run id")

    metadata = _decode_json_field(payload.get("metadata"), {})
    categories = _decode_json_field(payload.get("categories_json"), [])
    category_scores = metadata.get("category_scores", {}) if isinstance(metadata, dict) else {}
    category_names = sorted(set(categories or []) | set(category_scores))
    artifact_types = ["independent-evaluation"]
    if "injection" in category_names:
        artifact_types.append("indirect-prompt-injection-tests")

    run_status = str(payload.get("status", "unknown")).lower()
    status = "failed" if run_status in FAILED_RUN_STATES else "observed"
    completed = payload.get("completed_cases", 0)
    total = payload.get("total_cases", 0)
    model = metadata.get("subject_model", "unknown model") if isinstance(metadata, dict) else "unknown model"
    record = {
        "sourceSystem": "djimitflo",
        "status": status,
        "runId": payload["id"],
        "artifactRef": f"djimitflo://openmythos-eval-runs/{payload['id']}",
        "summary": (
            f"Djimitflo evaluation run for {model} {run_status}: "
            f"{completed}/{total} cases completed."
        ),
        "artifactTypes": artifact_types,
        "artifactHash": artifact_hash(export_path),
    }
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="source", required=True)

    openmythos = subparsers.add_parser("openmythos")
    openmythos.add_argument("run", type=Path)
    openmythos.add_argument("--oracle", type=Path)
    openmythos.add_argument("--run-id")

    djimitflo = subparsers.add_parser("djimitflo")
    djimitflo.add_argument("export", type=Path)

    args = parser.parse_args()
    if args.source == "openmythos":
        record = adapt_openmythos(args.run, args.oracle, args.run_id)
    else:
        record = adapt_djimitflo(args.export)
    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
