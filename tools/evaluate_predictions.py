#!/usr/bin/env python3
"""Evaluate versioned rule/PII predictions from JSONL without ML dependencies."""

import argparse
import json
from collections import defaultdict
from pathlib import Path


def evaluate(rows: list[dict]) -> dict:
    counts = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})
    abstained = 0
    for row in rows:
        expected = set(row.get("expected", []))
        predicted_raw = row.get("predicted")
        if predicted_raw is None:
            predicted = set()
            abstained += 1
        else:
            predicted = set(predicted_raw)
        for label in expected & predicted:
            counts[label]["tp"] += 1
        for label in predicted - expected:
            counts[label]["fp"] += 1
        for label in expected - predicted:
            counts[label]["fn"] += 1

    tp = sum(value["tp"] for value in counts.values())
    fp = sum(value["fp"] for value in counts.values())
    fn = sum(value["fn"] for value in counts.values())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "examples": len(rows),
        "abstained": abstained,
        "micro": {"precision": precision, "recall": recall, "f1": f1},
        "perLabel": dict(sorted(counts.items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=Path, help="JSONL with expected and predicted label arrays")
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.dataset.read_text().splitlines() if line.strip()]
    print(json.dumps(evaluate(rows), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
