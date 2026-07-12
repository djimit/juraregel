#!/usr/bin/env python3
"""
JuraRegel Knowledge Base (JKB) Index Builder.

Leest alle JREM exports en genereert drie representaties per regel:
1. JREM JSON (machine-structured)
2. Nederlandse natuurlijke taal (human-readable)
3. Embedding-ready tekst (LLM-searchable)

Output: .data/knowledge-base/jkb-index.json + jkb-summary.json (generated, untracked)
"""
import json
import hashlib
import argparse
import sys
from pathlib import Path
from typing import Any

def generate_nl_text(rule: dict, domain: str, jrem: dict) -> str:
    """Generate a natural language description of a rule."""
    sources = ", ".join(
        f"{ref.get('title', '')} {ref.get('section', '')}".strip()
        for ref in rule.get("sourceRefs", [])
    )
    
    conditions_parts = []
    for k, v in rule.get("conditions", {}).items():
        if k == "periode":
            continue
        if isinstance(v, str):
            conditions_parts.append(f"{k} is {v}")
        elif isinstance(v, bool):
            conditions_parts.append(f"{k} is {'ja' if v else 'nee'}")
        elif isinstance(v, dict):
            ops = []
            for op, val in v.items():
                if op == "periode": continue
                op_map = {"gt": "groter dan", "gte": "minimaal", "lt": "kleiner dan", "lte": "maximaal"}
                ops.append(f"{op_map.get(op, op)} {val}")
            conditions_parts.append(f"{k} {' en '.join(ops)}" if ops else f"{k} {v}")
        elif isinstance(v, list):
            conditions_parts.append(f"{k} is een van {v}")
        else:
            conditions_parts.append(f"{k} = {v}")
    
    conditions_text = "; ".join(conditions_parts) if conditions_parts else "geen specifieke voorwaarden"
    
    outcome = rule.get("outcome", {})
    outcome_parts = []
    for k, v in outcome.items():
        if k in ("confidence", "manualReviewRequired"):
            continue
        if isinstance(v, dict):
            outcome_parts.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
        elif isinstance(v, bool):
            outcome_parts.append(f"{k}: {'ja' if v else 'nee'}")
        else:
            outcome_parts.append(f"{k}: {v}")
    outcome_text = "; ".join(outcome_parts) if outcome_parts else "geen uitkomst"
    
    return (
        f"Regel {rule['ruleId']} uit domein '{domain}' (versie {jrem.get('version', '?')}): "
        f"{rule['name']}. "
        f"Voorwaarden: {conditions_text}. "
        f"Uitkomst: {outcome_text}. "
        f"Bron: {sources}."
    )

def generate_embedding_text(rule: dict, domain: str) -> str:
    """Generate text optimized for embedding search."""
    sources = " ".join(ref.get("title", "") for ref in rule.get("sourceRefs", []))
    conditions = " ".join(str(v) for v in rule.get("conditions", {}).values() if not isinstance(v, dict))
    outcome = " ".join(str(v) for k, v in rule.get("outcome", {}).items() if k not in ("confidence", "manualReviewRequired"))
    return f"{domain} {rule['ruleId']} {rule['name']} {sources} {conditions} {outcome}"

def extract_graph_nodes(rule: dict, domain: str) -> list[dict]:
    """Extract knowledge graph nodes from a rule."""
    nodes = []
    for ref in rule.get("sourceRefs", []):
        nodes.append({
            "type": "legal_source",
            "title": ref.get("title", ""),
            "section": ref.get("section", ""),
            "url": ref.get("url", "")
        })
    for key, val in rule.get("conditions", {}).items():
        if key == "periode":
            continue
        nodes.append({
            "type": "condition",
            "field": key,
            "value": val if not isinstance(val, dict) else json.dumps(val, ensure_ascii=False)
        })
    outcome = rule.get("outcome", {})
    for key, val in outcome.items():
        if key in ("confidence", "manualReviewRequired"):
            continue
        nodes.append({
            "type": "outcome",
            "field": key,
            "value": val if not isinstance(val, dict) else json.dumps(val, ensure_ascii=False)
        })
    return nodes

def build_jkb_index(use_cases_dir: Path, output_dir: Path) -> int:
    """Build the JKB index from all JREM exports."""
    index = []
    
    for domain_dir in sorted(use_cases_dir.iterdir()):
        if not domain_dir.is_dir():
            continue
        jrem_dir = domain_dir / "jrem" / "exports"
        if not jrem_dir.exists():
            continue
        
        for jrem_file in sorted(jrem_dir.glob("*.json")):
            try:
                jrem = json.loads(jrem_file.read_text())
            except json.JSONDecodeError:
                continue
            
            domain = jrem.get("domain", domain_dir.name)
            
            for rule in jrem.get("rules", []):
                entry = {
                    "rule_id": rule["ruleId"],
                    "domain": domain,
                    "version": jrem.get("version", "?"),
                    "valid_from": jrem.get("validFrom"),
                    "valid_until": jrem.get("validUntil"),
                    "name": rule["name"],
                    "conditions": rule.get("conditions", {}),
                    "outcome": rule.get("outcome", {}),
                    "source_refs": rule.get("sourceRefs", []),
                    "priority": rule.get("priority", 0),
                    "jurist_acordering": jrem.get("juristAccordering", {}),
                    "nl_text": generate_nl_text(rule, domain, jrem),
                    "embedding_text": generate_embedding_text(rule, domain),
                    "graph_nodes": extract_graph_nodes(rule, domain),
                    "content_hash": hashlib.sha256(
                        json.dumps(rule, sort_keys=True, ensure_ascii=False).encode()
                    ).hexdigest(),
                }
                index.append(entry)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "jkb-index.json").write_text(
        json.dumps(index, indent=2, ensure_ascii=False)
    )
    
    # Per-domain summary
    domains = {}
    for entry in index:
        d = entry["domain"]
        if d not in domains:
            domains[d] = {"rule_count": 0, "versions": set(), "source_types": set()}
        domains[d]["rule_count"] += 1
        domains[d]["versions"].add(entry["version"])
        for ref in entry["source_refs"]:
            domains[d]["source_types"].add(ref.get("type", "unknown"))
    
    summary = {
        "total_rules": len(index),
        "total_domains": len(domains),
        "domains": {
            d: {
                "rule_count": v["rule_count"],
                "versions": sorted(v["versions"]),
                "source_types": sorted(v["source_types"])
            }
            for d, v in sorted(domains.items())
        }
    }
    (output_dir / "jkb-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False)
    )
    
    return len(index)

def validate_index(use_cases_dir: Path, index_path: Path) -> dict:
    """Validate that the JKB index contains all rules from all JREM exports."""
    # Count rules in JREM exports
    jrem_count = 0
    jrem_rule_ids = set()
    for domain_dir in use_cases_dir.iterdir():
        if not domain_dir.is_dir():
            continue
        jrem_dir = domain_dir / "jrem" / "exports"
        if not jrem_dir.exists():
            continue
        for jrem_file in jrem_dir.glob("*.json"):
            try:
                jrem = json.loads(jrem_file.read_text())
                for rule in jrem.get("rules", []):
                    jrem_count += 1
                    jrem_rule_ids.add(rule["ruleId"])
            except json.JSONDecodeError:
                continue
    
    # Count rules in index
    if not index_path.exists():
        return {"valid": False, "error": "Index file not found", "jrem_count": jrem_count, "index_count": 0}
    
    index = json.loads(index_path.read_text())
    index_count = len(index)
    index_rule_ids = {e["rule_id"] for e in index}
    
    missing = jrem_rule_ids - index_rule_ids
    extra = index_rule_ids - jrem_rule_ids
    
    # Check each entry has required fields
    incomplete = []
    for e in index:
        for field in ("nl_text", "embedding_text", "graph_nodes", "content_hash"):
            if field not in e or not e[field]:
                incomplete.append({"rule_id": e["rule_id"], "missing": field})
    
    return {
        "valid": len(missing) == 0 and len(extra) == 0 and len(incomplete) == 0,
        "jrem_count": jrem_count,
        "index_count": index_count,
        "missing_rules": sorted(missing)[:10],
        "extra_rules": sorted(extra)[:10],
        "incomplete_entries": incomplete[:10]
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    repo_root = Path(__file__).parent.parent
    use_cases = repo_root / "use-cases"
    output = args.output or repo_root / ".data" / "knowledge-base"
    
    if args.check_only:
        result = validate_index(use_cases, output / "jkb-index.json")
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["valid"] else 1)
    
    count = build_jkb_index(use_cases, output)
    print(f"JKB index built: {count} rules indexed")
    
    # Validate
    result = validate_index(use_cases, output / "jkb-index.json")
    print(f"Validation: {'PASS' if result['valid'] else 'FAIL'}")
    if not result["valid"]:
        print(json.dumps(result, indent=2))
        sys.exit(1)
    
    # Print summary
    summary = json.loads((output / "jkb-summary.json").read_text())
    print(f"Domains: {summary['total_domains']}")
    print(f"Total rules: {summary['total_rules']}")
