"""
JuraRegel MCP Server — Exposes all JuraRegel Rule APIs as MCP tools.

Usage:
  python3 juraregel_mcp.py

Or with OpenCode/Claude config:
  mcpServers:
    juraregel:
      command: python3
      args: ["/path/to/juraregel/mcp-server/juraregel_mcp.py"]
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

# ─── Domain Registry ──────────────────────────────────────────
# Maps domain → (port, jrem_path)
# Ports match the use case app.py files

DOMAINS = {
    "griffierecht":         {"port": 8490, "version": "2026.1"},
    "procesreglement":      {"port": 8491, "version": "2026.1"},
    "classificatie":        {"port": 8492, "version": "2026.1"},
    "publicatie":           {"port": 8493, "version": "2026.1"},
    "bio2":                 {"port": 8494, "version": "2025.1"},
    "forumstandaardisatie": {"port": 8495, "version": "2025.1"},
    "overheidsstandaarden": {"port": 8496, "version": "2025.1"},
    "nora":                 {"port": 8497, "version": "2025.1"},
    "eu-ai-act":            {"port": 8498, "version": "2025.1"},
    "avg-gdpr":             {"port": 8499, "version": "2025.1"},
    "ncsc":                 {"port": 8500, "version": "2025.1"},
    "nis2":                 {"port": 8501, "version": "2025.1"},
    "btw-tarieven":         {"port": 8502, "version": "2025.1"},
    "ww-uitkering":         {"port": 8503, "version": "2025.1"},
    "ind-verblijfsregels":  {"port": 8504, "version": "2025.1"},
    "wmo":                  {"port": 8505, "version": "2025.1"},
    "gegevensdelingsbeleid": {"port": 8506, "version": "2025.1"},
    "dpia-model":           {"port": 8507, "version": "2025.1"},
    "algoritmeregister":    {"port": 8508, "version": "2025.1"},
    "data-overheid-dcat":   {"port": 8509, "version": "2025.1"},
    "api-registratie":      {"port": 8510, "version": "2025.1"},
    "traceability":         {"port": 8511, "version": "2025.1"},
    "compliance-debt":      {"port": 8512, "version": "2025.1"},
    "regulatory-impact":    {"port": 8513, "version": "2025.1"},
    "toeslagen":            {"port": 8514, "version": "2025.1"},
    "omgevingswet":         {"port": 8515, "version": "2025.1"},
    "basisregistraties":    {"port": 8516, "version": "2025.1"},
    "participatiewet":      {"port": 8517, "version": "2025.1"},
}

# ─── JREM Direct Access (no API server needed) ────────────────
# For MCP, we read JREM files directly — no need to run 28 API servers

JREM_BASE = Path(__file__).parent.parent / "use-cases"

_jrem_cache: dict[str, dict] = {}

def load_jrem(domain: str) -> dict:
    """Load the latest JREM export for a domain."""
    if domain in _jrem_cache:
        return _jrem_cache[domain]
    
    jrem_dir = JREM_BASE / domain / "jrem" / "exports"
    if not jrem_dir.exists():
        raise FileNotFoundError(f"No JREM exports for domain '{domain}' at {jrem_dir}")
    
    files = sorted(jrem_dir.glob("*.json"), key=lambda f: f.name, reverse=True)
    if not files:
        raise FileNotFoundError(f"No JREM files in {jrem_dir}")
    
    with open(files[0]) as f:
        data = json.load(f)
    
    _jrem_cache[domain] = data
    return data

def list_all_domains() -> list[dict]:
    """List all available domains with metadata."""
    result = []
    for domain, info in DOMAINS.items():
        try:
            jrem = load_jrem(domain)
            result.append({
                "domain": domain,
                "version": jrem.get("version", "?"),
                "validFrom": jrem.get("validFrom"),
                "validUntil": jrem.get("validUntil"),
                "ruleCount": len(jrem.get("rules", [])),
                "port": info["port"],
                "jurisdiction": jrem.get("jurisdiction", "NL"),
            })
        except Exception:
            result.append({"domain": domain, "error": "JREM not found", "port": info["port"]})
    return result

def get_rules(domain: str, rule_id: str = None) -> list[dict] | dict:
    """Get rules for a domain, optionally filtered by ruleId."""
    jrem = load_jrem(domain)
    rules = jrem.get("rules", [])
    if rule_id:
        for r in rules:
            if r["ruleId"] == rule_id:
                return {"rule": r, "rulesetVersion": jrem["version"]}
        return {"error": f"Rule {rule_id} not found in {domain}"}
    return rules

def search_rules(query: str, domain: str = None) -> list[dict]:
    """Search rules by keyword in ruleId, name, or sourceRefs."""
    results = []
    domains_to_search = [domain] if domain else list(DOMAINS.keys())
    
    query_words = [w.lower() for w in query.split() if len(w) >= 3]
    
    for d in domains_to_search:
        try:
            jrem = load_jrem(d)
            for rule in jrem.get("rules", []):
                # Search in ruleId, name, sourceRefs
                searchable = (
                    rule.get("ruleId", "") + " " +
                    rule.get("name", "") + " " +
                    " ".join(s.get("title", "") + " " + s.get("section", "") for s in rule.get("sourceRefs", []))
                ).lower()
                
                # Match if ALL query words are found in the searchable text
                if all(word in searchable for word in query_words):
                    results.append({
                        "ruleId": rule["ruleId"],
                        "domain": d,
                        "name": rule["name"][:100],
                        "sourceRefs": rule.get("sourceRefs", [])[:2],
                        "relevance": "high" if all(w in rule.get("ruleId", "").lower() for w in query_words) else "partial"
                    })
        except Exception:
            continue
    
    return results[:20]  # limit to 20 results

def match_rule(domain: str, input_data: dict) -> dict:
    """
    Match input against rules in a domain and return the first matching rule's outcome.
    Uses priority-sorted first-match semantics.
    """
    jrem = load_jrem(domain)
    rules = jrem.get("rules", [])
    sorted_rules = sorted(rules, key=lambda r: r.get("priority", 0), reverse=True)
    
    for rule in sorted_rules:
        conditions = rule.get("conditions", {})
        all_match = True
        
        for key, condition in conditions.items():
            if key == "periode":
                continue
            
            val = input_data.get(key)
            
            # Match logic
            if condition is None:
                continue
            elif val is None:
                all_match = False
                break
            elif isinstance(condition, str):
                if val != condition:
                    all_match = False
                    break
            elif isinstance(condition, list):
                if val not in condition:
                    all_match = False
                    break
            elif isinstance(condition, dict):
                # Filter out non-comparison keys like "periode"
                cond_filtered = {k: v for k, v in condition.items() if k in ("gt", "gte", "lt", "lte")}
                if not isinstance(val, (int, float)):
                    all_match = False
                    break
                if "gt" in cond_filtered and not (val > cond_filtered["gt"]):
                    all_match = False
                    break
                if "gte" in cond_filtered and not (val >= cond_filtered["gte"]):
                    all_match = False
                    break
                if "lt" in cond_filtered and not (val < cond_filtered["lt"]):
                    all_match = False
                    break
                if "lte" in cond_filtered and not (val <= cond_filtered["lte"]):
                    all_match = False
                    break
            elif isinstance(condition, bool):
                if val != condition:
                    all_match = False
                    break
            else:
                if val != condition:
                    all_match = False
                    break
        
        if all_match:
            import hashlib
            from datetime import datetime, timezone
            input_hash = hashlib.sha256(json.dumps(input_data, sort_keys=True).encode()).hexdigest()[:16]
            ruleset_hash = hashlib.sha256(json.dumps(jrem, sort_keys=True).encode()).hexdigest()[:16]
            
            return {
                "calculationId": f"calc-{input_hash}",
                "ruleSetVersion": jrem["version"],
                "domain": domain,
                "result": {
                    "matchedRule": {"ruleId": rule["ruleId"], "name": rule["name"]},
                    "outcome": rule.get("outcome", {})
                },
                "explanation": {
                    "summary": rule["name"],
                    "appliedRules": [rule["ruleId"]],
                    "sourceRefs": rule.get("sourceRefs", []),
                    "conditions": rule.get("conditions", {})
                },
                "audit": {
                    "inputHash": f"sha256:{input_hash}",
                    "rulesetHash": f"sha256:{ruleset_hash}",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
    
    return {
        "domain": domain,
        "result": {"matchedRule": None, "outcome": {}},
        "explanation": {"summary": "Geen passende regel gevonden voor deze input"},
        "warnings": ["Geen match — verifieer input of raadpleeg een jurist"]
    }

def get_sources(domain: str) -> list[dict]:
    """Get all unique source references for a domain."""
    jrem = load_jrem(domain)
    sources = {}
    for rule in jrem.get("rules", []):
        for ref in rule.get("sourceRefs", []):
            key = f"{ref.get('title', '')}|{ref.get('section', '')}"
            if key not in sources:
                sources[key] = {
                    "title": ref.get("title", ""),
                    "section": ref.get("section", ""),
                    "type": ref.get("type", ""),
                    "url": ref.get("url", "")
                }
    return list(sources.values())

def get_audit_trail(domain: str, rule_id: str) -> dict:
    """Get the full traceability chain for a rule: wet → code → test → audit."""
    jrem = load_jrem(domain)
    rule = None
    for r in jrem.get("rules", []):
        if r["ruleId"] == rule_id:
            rule = r
            break
    
    if not rule:
        return {"error": f"Rule {rule_id} not found in {domain}"}
    
    # Find test file
    test_file = JREM_BASE / domain / "tests" / f"test_{domain.replace('-', '_')}.py"
    test_refs = []
    if test_file.exists():
        content = test_file.read_text()
        if rule_id in content:
            # Find test functions that reference this rule
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if "def test_" in line and i < len(lines):
                    # Check next 10 lines for rule_id reference
                    context = "\n".join(lines[i:i+15])
                    if rule_id in context:
                        test_name = line.split("def ")[1].split("(")[0]
                        test_refs.append(test_name)
    
    return {
        "ruleId": rule_id,
        "domain": domain,
        "wet": [ref.get("title", "") + " " + ref.get("section", "") for ref in rule.get("sourceRefs", [])],
        "code": f"use-cases/{domain}/api/app.py",
        "jrem": f"use-cases/{domain}/jrem/exports/",
        "tests": test_refs,
        "review": f"docs/review-requests/review-request-{domain}.md",
        "openapi": f"openapi/{domain}.yaml",
        "version": jrem.get("version"),
        "validFrom": jrem.get("validFrom"),
        "validUntil": jrem.get("validUntil")
    }

def version_diff(domain: str, v1: str, v2: str) -> dict:
    """Compare two JREM versions of a domain."""
    jrem_dir = JREM_BASE / domain / "jrem" / "exports"
    results = {"added": [], "removed": [], "modified": []}
    
    versions = {}
    for f in jrem_dir.glob("*.json"):
        data = json.loads(f.read_text())
        versions[data["version"]] = data
    
    if v1 not in versions:
        return {"error": f"Version {v1} not found. Available: {list(versions.keys())}"}
    if v2 not in versions:
        return {"error": f"Version {v2} not found. Available: {list(versions.keys())}"}
    
    rules_v1 = {r["ruleId"]: r for r in versions[v1]["rules"]}
    rules_v2 = {r["ruleId"]: r for r in versions[v2]["rules"]}
    
    for rid in rules_v2:
        if rid not in rules_v1:
            results["added"].append(rid)
        elif rules_v1[rid] != rules_v2[rid]:
            results["modified"].append(rid)
    
    for rid in rules_v1:
        if rid not in rules_v2:
            results["removed"].append(rid)
    
    return results


def semantic_search(query: str, domain: str = None, limit: int = 10) -> list:
    """Semantic search via Qdrant vector store. Falls back to keyword store if Qdrant unavailable."""
    repo_root = Path(__file__).parent.parent
    try:
        from tools.jkb_vectorstore import init_qdrant, search as vec_search
        client = init_qdrant(str(repo_root / ".qdrant"))
        return vec_search(client, query, domain=domain, limit=limit)
    except Exception:
        # Fallback: keyword search via SQLite FTS5
        import sqlite3
        db_path = repo_root / ".keyword.db"
        if not db_path.exists():
            return [
                {
                    "rule_id": r["ruleId"],
                    "ruleId": r["ruleId"],
                    "domain": r["domain"],
                    "name": r["name"],
                    "sourceRefs": r.get("sourceRefs", []),
                    "nl_text": r["name"],
                    "score": None,
                }
                for r in search_rules(query, domain)[:limit]
            ]
        conn = sqlite3.connect(str(db_path))
        terms = query.replace('"', '').strip().split()
        fts_query = " ".join('"' + t + '"' for t in terms if t)
        if domain:
            sql = "SELECT rule_id, domain, name, nl_text FROM rules WHERE rules MATCH ? AND domain = ? ORDER BY rank LIMIT ?"
            rows = conn.execute(sql, (fts_query, domain, limit)).fetchall()
        else:
            sql = "SELECT rule_id, domain, name, nl_text FROM rules WHERE rules MATCH ? ORDER BY rank LIMIT ?"
            rows = conn.execute(sql, (fts_query, limit)).fetchall()
        conn.close()
        return [{"rule_id": r[0], "domain": r[1], "name": r[2], "nl_text": r[3][:200], "score": None} for r in rows]

def build_reasoning(matched_result: dict) -> list[str]:
    """Build reasoning steps from a matched rule result."""
    steps = []
    rule = matched_result.get("result", {}).get("matchedRule", {})
    explanation = matched_result.get("explanation", {})
    conditions = explanation.get("conditions", {})
    
    steps.append(f"Regel {rule.get('ruleId', '?')} '{rule.get('name', '?')}' geevalueerd")
    
    for key, val in conditions.items():
        if key == "periode":
            continue
        if isinstance(val, dict):
            parts = []
            for op, v in val.items():
                if op == "periode":
                    continue
                op_map = {"gt": ">", "gte": ">=", "lt": "<", "lte": "<="}
                parts.append(f"{op_map.get(op, op)} {v}")
            steps.append(f"Voorwaarde {key}: {' en '.join(parts)}")
        else:
            steps.append(f"Voorwaarde {key}: {val}")
    
    outcome = matched_result.get("result", {}).get("outcome", {})
    outcome_parts = [f"{k}: {v}" for k, v in outcome.items() if k not in ("confidence", "manualReviewRequired")]
    if outcome_parts:
        steps.append(f"Uitkomst: {'; '.join(outcome_parts)}")
    
    if matched_result.get("result", {}).get("matchedRule", {}).get("ruleId") is None:
        steps.append("Geen regel matchte met de gegeven input")
    
    return steps

def explain(domain: str, input_data: dict) -> dict:
    """Explain a calculation in natural language with reasoning steps."""
    result = match_rule(domain, input_data)
    return {
        "summary": result.get("explanation", {}).get("summary", ""),
        "reasoning_steps": build_reasoning(result),
        "source_refs": result.get("explanation", {}).get("sourceRefs", []),
        "conditions_checked": result.get("explanation", {}).get("conditions", {}),
        "outcome": result.get("result", {}).get("outcome", {}),
        "matched_rule": result.get("result", {}).get("matchedRule"),
    }

def check_compliance(domain: str, framework: str = None) -> dict:
    """Check compliance of a domain against a framework (BIO2, NIS2, AVG)."""
    jrem = load_jrem(domain)
    rules = jrem.get("rules", [])
    
    total = len(rules)
    compliant = 0
    manual_review = 0
    gaps = []
    
    for rule in rules:
        outcome = rule.get("outcome", {})
        if outcome.get("compliant") == True or outcome.get("vergunningplichtig") == False:
            compliant += 1
        elif outcome.get("manualReviewRequired"):
            manual_review += 1
            gaps.append({
                "rule_id": rule["ruleId"],
                "name": rule["name"],
                "status": "manual_review_required",
                "source_refs": rule.get("sourceRefs", [])
            })
        else:
            gaps.append({
                "rule_id": rule["ruleId"],
                "name": rule["name"],
                "status": "unknown",
                "source_refs": rule.get("sourceRefs", [])
            })
    
    return {
        "domain": domain,
        "framework": framework or domain,
        "total_rules": total,
        "compliant": compliant,
        "manual_review": manual_review,
        "compliance_percentage": round(compliant / total * 100, 1) if total > 0 else 0,
        "gaps": gaps[:10],
        "gap_count": len(gaps),
        "version": jrem.get("version"),
    }

def get_playbook(playbook_id: str) -> dict:
    """Get an agent playbook by ID."""
    playbooks_dir = Path(__file__).parent.parent / "docs" / "agent-playbooks"
    playbook_file = playbooks_dir / f"{playbook_id}.md"
    
    if playbook_file.exists():
        return {"playbook_id": playbook_id, "content": playbook_file.read_text(), "source": str(playbook_file)}
    
    # List available playbooks
    available = []
    if playbooks_dir.exists():
        available = [f.stem for f in playbooks_dir.glob("*.md") if f.name != "_template.md"]
    
    return {"error": f"Playbook '{playbook_id}' not found", "available": available}

def get_governance(domain: str, rule_id: str = None) -> dict:
    """Get governance info for a domain or specific rule."""
    governance_dir = Path(__file__).parent.parent / "governance"
    registry_file = governance_dir / "governance-registry.jsonld"
    
    if registry_file.exists():
        registry = json.loads(registry_file.read_text())
        if rule_id:
            for entry in registry.get("@graph", []):
                if entry.get("@id") == f"rule:{rule_id}":
                    return entry
            return {"error": f"Rule {rule_id} not in governance registry"}
        graph = registry.get("@graph", [])
        if domain:
            for entry in graph:
                if entry.get("domain") == domain:
                    return entry
            return {"error": f"Domain {domain} not in governance registry", "available": [e.get("domain") for e in graph]}
        return registry
    
    # Fallback: derive from JREM
    jrem = load_jrem(domain)
    return {
        "domain": domain,
        "version": jrem.get("version"),
        "governance_level": "rijk",
        "note": "Governance registry not yet built — using JREM defaults",
        "rules_count": len(jrem.get("rules", [])),
    }

# ─── MCP Protocol (stdio) ─────────────────────────────────────
# Simple MCP-over-stdio implementation for agent integration


# ─── MCP Resources ─────────────────────────────────────────────

def get_resource_list() -> list[dict]:
    """List all available MCP resources."""
    domains_summary = []
    for domain, info in DOMAINS.items():
        try:
            jrem = load_jrem(domain)
            domains_summary.append({
                "domain": domain,
                "version": jrem.get("version", "?"),
                "ruleCount": len(jrem.get("rules", [])),
                "validFrom": jrem.get("validFrom"),
                "validUntil": jrem.get("validUntil"),
            })
        except Exception:
            domains_summary.append({"domain": domain, "error": "JREM not found"})
    
    return [
        {
            "uri": "laws://list",
            "name": "Alle beschikbare wetten/domeinen",
            "description": "Lijst van alle JuraRegel domeinen met metadata (versie, regelcount, geldigheid).",
            "mimeType": "application/json",
        },
        {
            "uri": "laws://summary",
            "name": "Knowledge Base samenvatting",
            "description": "Samenvatting van alle 665+ regels per domein uit de JKB index.",
            "mimeType": "application/json",
        },
    ] + [
        {
            "uri": f"laws://{d['domain']}/spec",
            "name": f"Specificatie: {d['domain']}",
            "description": f"Volledige JREM specificatie voor domein {d['domain']} ({d.get('ruleCount', '?')} regels, versie {d.get('version', '?')}).",
            "mimeType": "application/json",
        }
        for d in domains_summary if "error" not in d
    ]

def read_resource(uri: str) -> dict | list | None:
    """Read a specific MCP resource by URI."""
    if uri == "laws://list":
        return list_all_domains()
    
    if uri == "laws://summary":
        kb_path = Path(__file__).parent.parent / "knowledge-base" / "jkb-summary.json"
        if kb_path.exists():
            return json.loads(kb_path.read_text())
        return {"error": "Knowledge base summary not found. Run: python3 tools/jkb-builder.py"}
    
    if uri.startswith("laws://") and uri.endswith("/spec"):
        domain = uri.replace("laws://", "").replace("/spec", "")
        try:
            return load_jrem(domain)
        except Exception as e:
            return {"error": str(e)}
    
    if uri.startswith("profile://"):
        domain = uri.replace("profile://", "")
        try:
            jrem = load_jrem(domain)
            # Extract input/output profile from rules
            input_fields = set()
            output_fields = set()
            for rule in jrem.get("rules", []):
                input_fields.update(rule.get("conditions", {}).keys())
                outcome = rule.get("outcome", {})
                for k, v in outcome.items():
                    if k not in ("confidence", "manualReviewRequired"):
                        output_fields.add(k)
            return {
                "domain": domain,
                "input_profile": sorted(input_fields),
                "output_profile": sorted(output_fields),
                "version": jrem.get("version"),
                "rule_count": len(jrem.get("rules", [])),
            }
        except Exception as e:
            return {"error": str(e)}
    
    return None

# ─── MCP Prompts ──────────────────────────────────────────────

def get_prompt_list() -> list[dict]:
    """List all available MCP prompts."""
    return [
        {
            "name": "check_all_benefits",
            "description": "Controleer alle mogelijke uitkeringen/toeslagen voor een persoon (zorgtoeslag, huurtoeslag, bijstand, AOW).",
            "arguments": [
                {"name": "leeftijd", "description": "Leeftijd van de persoon", "required": True},
                {"name": "inkomen", "description": "Jaarinkomen in euro", "required": True},
                {"name": "huishouden", "description": "Type huishouden (alleenstaande, samenwonend, alleenstaande_ouder)", "required": True},
            ],
        },
        {
            "name": "explain_calculation",
            "description": "Leg een JuraRegel berekening uit in natuurlijke taal met redeneerstappen en bronverwijzingen.",
            "arguments": [
                {"name": "domain", "description": "Domein (bijv. toeslagen, participatiewet)", "required": True},
                {"name": "input", "description": "Input data als JSON object", "required": True},
            ],
        },
        {
            "name": "compare_scenarios",
            "description": "Vergelijk twee scenario's voor hetzelfde domein (bijv. alleenstaand vs samenwonend).",            "arguments": [
                {"name": "domain", "description": "Domein", "required": True},
                {"name": "scenario_a", "description": "Eerste scenario als JSON", "required": True},
                {"name": "scenario_b", "description": "Tweede scenario als JSON", "required": True},
            ],
        },
    ]

def get_prompt(name: str, arguments: dict) -> dict | None:
    """Get a specific prompt with filled-in arguments."""
    if name == "check_all_benefits":
        leeftijd = arguments.get("leeftijd")
        inkomen = arguments.get("inkomen")
        huishouden = arguments.get("huishouden")
        return {
            "messages": [
                {
                    "role": "user",
                    "content": f"Controleer alle mogelijke uitkeringen voor een {huishouden} persoon van {leeftijd} jaar met een jaarinkomen van EUR {inkomen}. Gebruik juraregel.check_compliance voor BIO2 en juraregel.calculate voor toeslagen en bijstand.",
                }
            ],
            "metadata": {"domains": ["toeslagen", "participatiewet"], "input": arguments},
        }
    
    if name == "explain_calculation":
        domain = arguments.get("domain", "")
        input_data = arguments.get("input", {})
        return {
            "messages": [
                {
                    "role": "user",
                    "content": f"Leg de {domain} berekening uit voor input {json.dumps(input_data, ensure_ascii=False)}. Gebruik juraregel.explain om de redeneerstappen, bronverwijzingen en voorwaarden te tonen.",
                }
            ],
            "metadata": {"domain": domain, "input": input_data},
        }
    
    if name == "compare_scenarios":
        domain = arguments.get("domain", "")
        a = arguments.get("scenario_a", {})
        b = arguments.get("scenario_b", {})
        return {
            "messages": [
                {
                    "role": "user",
                    "content": f"Vergelijk deze twee scenario's voor {domain}:\nScenario A: {json.dumps(a, ensure_ascii=False)}\nScenario B: {json.dumps(b, ensure_ascii=False)}\nGebruik juraregel.calculate voor beide en toon de verschillen.",
                }
            ],
            "metadata": {"domain": domain, "scenario_a": a, "scenario_b": b},
        }
    
    return None

def handle_request(msg: dict) -> dict:
    """Handle an MCP tool call."""
    method = msg.get("method", "")
    params = msg.get("params", {})
    msg_id = msg.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}, "resources": {}, "prompts": {}},
                "serverInfo": {"name": "juraregel", "version": "2.1.0"}
            }
        }
    
    elif method == "resources/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"resources": get_resource_list()}
        }
    
    elif method == "resources/read":
        uri = params.get("uri", "")
        data = read_resource(uri)
        if data is None:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32602, "message": f"Unknown resource: {uri}"}
            }
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "contents": [{"uri": uri, "mimeType": "application/json", "text": json.dumps(data, indent=2, ensure_ascii=False)}]
            }
        }
    
    elif method == "prompts/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {"prompts": get_prompt_list()}
        }
    
    elif method == "prompts/get":
        name = params.get("name", "")
        arguments = params.get("arguments", {})
        prompt = get_prompt(name, arguments)
        if prompt is None:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32602, "message": f"Unknown prompt: {name}"}
            }
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": prompt
        }
    
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": [
                    {
                        "name": "juraregel.list_domains",
                        "description": "List all available JuraRegel domains with metadata (rule count, version, validity).",
                        "inputSchema": {"type": "object", "properties": {}}
                    },
                    {
                        "name": "juraregel.get_rules",
                        "description": "Get all rules for a domain, or a specific rule by ruleId. Returns JREM structured rules with conditions, outcomes, and source references.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "domain": {"type": "string", "description": "Domain name (e.g. 'toeslagen', 'omgevingswet', 'bio2')"},
                                "rule_id": {"type": "string", "description": "Optional: specific rule ID to look up"}
                            },
                            "required": ["domain"]
                        }
                    },
                    {
                        "name": "juraregel.search_rules",
                        "description": "Search rules across all or one domain by keyword. Searches in ruleId, name, and source references.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Search query (keyword or phrase)"},
                                "domain": {"type": "string", "description": "Optional: limit search to one domain"}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "juraregel.calculate",
                        "description": "Calculate a legal result by matching input against rules. Returns the matched rule, outcome, explanation, source references, and audit trail.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "domain": {"type": "string", "description": "Domain name (e.g. 'toeslagen', 'omgevingswet')"},
                                "input": {"type": "object", "description": "Input data matching the domain's rule conditions"}
                            },
                            "required": ["domain", "input"]
                        }
                    },
                    {
                        "name": "juraregel.get_sources",
                        "description": "Get all unique source references (wetten, besluiten, richtlijnen) for a domain.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "domain": {"type": "string", "description": "Domain name"}
                            },
                            "required": ["domain"]
                        }
                    },
                    {
                        "name": "juraregel.trace",
                        "description": "Get the full traceability chain for a rule: wet → code → JREM → test → review → OpenAPI. Enables audit and compliance verification.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "domain": {"type": "string", "description": "Domain name"},
                                "rule_id": {"type": "string", "description": "Rule ID to trace"}
                            },
                            "required": ["domain", "rule_id"]
                        }
                    },
                    {
                        "name": "juraregel.version_diff",
                        "description": "Compare two versions of a domain's ruleset. Shows added, removed, and modified rules.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "domain": {"type": "string", "description": "Domain name"},
                                "v1": {"type": "string", "description": "First version (e.g. '2025.1')"},
                                "v2": {"type": "string", "description": "Second version (e.g. '2026.1')"}
                            },
                            "required": ["domain", "v1", "v2"]
                        }
                    },
                    {
                        "name": "juraregel.semantic_search",
                        "description": "Semantisch zoeken in alle JuraRegel regels. Gebruikt vector embeddings (Qdrant) of keyword search (SQLite FTS5) als fallback.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Zoekopdracht in natuurlijke taal"},
                                "domain": {"type": "string", "description": "Optioneel: beperk tot domein"},
                                "limit": {"type": "integer", "description": "Max resultaten (default 10)"}
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "juraregel.explain",
                        "description": "Verklaar een berekening in natuurlijke taal met redeneerstappen, bronverwijzingen en voorwaarden.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "domain": {"type": "string", "description": "Domein naam"},
                                "input": {"type": "object", "description": "Input data voor de berekening"}
                            },
                            "required": ["domain", "input"]
                        }
                    },
                    {
                        "name": "juraregel.check_compliance",
                        "description": "Compliance check voor een domein tegen een framework (BIO2, NIS2, AVG). Geeft percentage en gaps.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "domain": {"type": "string", "description": "Domein naam"},
                                "framework": {"type": "string", "description": "Framework (bio2, nis2, avg-gdpr). Optioneel."}
                            },
                            "required": ["domain"]
                        }
                    },
                    {
                        "name": "juraregel.get_playbook",
                        "description": "Haal een agent playbook op. Geeft stappen, tools, escalation en voorbeelden.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "playbook_id": {"type": "string", "description": "Playbook ID (bijv. toeslagen, bio2, nis2)"}
                            },
                            "required": ["playbook_id"]
                        }
                    },
                    {
                        "name": "juraregel.get_governance",
                        "description": "Haal governance informatie op voor een domein of regel. Geeft niveau, bronnen, lokale variaties.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "domain": {"type": "string", "description": "Domein naam"},
                                "rule_id": {"type": "string", "description": "Optioneel: specifieke regel ID"}
                            },
                            "required": ["domain"]
                        }
                    },
                ]
            }
        }
    
    elif method == "tools/call":
        tool_name = params.get("name", "")
        args = params.get("arguments", {})
        
        try:
            if tool_name == "juraregel.list_domains":
                result = list_all_domains()
            elif tool_name == "juraregel.get_rules":
                result = get_rules(args["domain"], args.get("rule_id"))
            elif tool_name == "juraregel.search_rules":
                result = search_rules(args["query"], args.get("domain"))
            elif tool_name == "juraregel.calculate":
                result = match_rule(args["domain"], args["input"])
            elif tool_name == "juraregel.get_sources":
                result = get_sources(args["domain"])
            elif tool_name == "juraregel.trace":
                result = get_audit_trail(args["domain"], args["rule_id"])
            elif tool_name == "juraregel.version_diff":
                result = version_diff(args["domain"], args["v1"], args["v2"])
            elif tool_name == "juraregel.semantic_search":
                result = semantic_search(args["query"], args.get("domain"), args.get("limit", 10))
            elif tool_name == "juraregel.explain":
                result = explain(args["domain"], args["input"])
            elif tool_name == "juraregel.check_compliance":
                result = check_compliance(args["domain"], args.get("framework"))
            elif tool_name == "juraregel.get_playbook":
                result = get_playbook(args["playbook_id"])
            elif tool_name == "juraregel.get_governance":
                result = get_governance(args["domain"], args.get("rule_id"))
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}
                }
            
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2, ensure_ascii=False)}]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32603, "message": str(e)}
            }
    
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "error": {"code": -32601, "message": f"Unknown method: {method}"}
    }

def main():
    """MCP server main loop over stdio."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            response = handle_request(msg)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            continue

if __name__ == "__main__":
    main()
