#!/usr/bin/env python3
"""Measure source debt and block L2/L3 rules without reproducible anchors."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "ci/source-quality-baseline.json"
LEGISLATIVE_TYPES = {"wet", "wetsartikel", "besluit"}
BWB_URL = re.compile(r"https://wetten\.overheid\.nl/BWBR\d+", re.IGNORECASE)
CELEX_URL = re.compile(r"[?&]uri=CELEX(?::|%3A)[0-9A-Z]+", re.IGNORECASE)
GENERIC_LEGAL_URLS = {
    "https://wetten.overheid.nl",
    "https://wetten.overheid.nl/",
    "https://eur-lex.europa.eu",
    "https://eur-lex.europa.eu/",
}


def issues_for_rule(rule: dict, ruleset: dict) -> list[str]:
    issues = []
    rule_id = rule.get("ruleId", "?")
    for index, ref in enumerate(rule.get("sourceRefs", [])):
        prefix = f"{rule_id}.sourceRefs[{index}]"
        url = ref.get("url", "")
        if not url or url in GENERIC_LEGAL_URLS:
            issues.append(f"{prefix}: missing url")
        if not (
            ref.get("bronVersie")
            or ref.get("bronDatum")
            or (ref.get("retrievedOn") and ref.get("type") not in LEGISLATIVE_TYPES)
        ):
            issues.append(f"{prefix}: missing source version/date")
        if ref.get("section") in (None, "", rule_id):
            issues.append(f"{prefix}: section is not an exact legal anchor")
        if ref.get("type") in LEGISLATIVE_TYPES and not (
            ref.get("bwbId")
            or ref.get("celexId")
            or ref.get("eli")
            or "/eli/" in url
            or BWB_URL.match(url)
            or CELEX_URL.search(url)
        ):
            issues.append(f"{prefix}: missing BWB/CELEX/ELI identifier")
    return issues


def audit(root: Path = ROOT, baseline_path: Path | None = None) -> dict:
    debt = []
    blocking = []
    counts = {}
    for path in sorted(root.glob("use-cases/*/jrem/exports/*.json")):
        ruleset = json.loads(path.read_text())
        maturity = ruleset.get("maturityLevel", "L0-demo")
        relative = str(path.relative_to(root))
        for rule in ruleset.get("rules", []):
            for issue in issues_for_rule(rule, ruleset):
                item = f"{relative}: {issue}"
                debt.append(item)
                counts[relative] = counts.get(relative, 0) + 1
                if maturity.startswith(("L2-", "L3-")):
                    blocking.append(item)
    baseline_file = baseline_path or (BASELINE if root == ROOT else None)
    baseline = json.loads(baseline_file.read_text()) if baseline_file and baseline_file.exists() else {}
    regressions = [
        f"{path}: {count} debt item(s), baseline {baseline.get(path, 0)}"
        for path, count in counts.items() if count > baseline.get(path, 0)
    ]
    return {"debt": debt, "blocking": blocking, "regressions": regressions}


if __name__ == "__main__":
    result = audit()
    for issue in result["blocking"][:50]:
        print(f"ERROR: {issue}")
    for issue in result["regressions"][:50]:
        print(f"REGRESSION: {issue}")
    print(
        f"Source quality: {len(result['debt'])} debt item(s), "
        f"{len(result['blocking'])} blocking, {len(result['regressions'])} regression(s)"
    )
    raise SystemExit(bool(result["blocking"] or result["regressions"]))
