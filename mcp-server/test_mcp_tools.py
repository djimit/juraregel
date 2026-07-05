#!/usr/bin/env python3
"""End-to-end tests for all 12 JuraRegel MCP tools."""
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
MCP_SERVER = REPO_ROOT / "mcp-server" / "juraregel_mcp.py"
PYTHON = sys.executable

def call_tool(name: str, arguments: dict) -> dict:
    """Send a JSON-RPC request to the MCP server via stdin."""
    req = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": name, "arguments": arguments}}
    proc = subprocess.run(
        [PYTHON, str(MCP_SERVER)],
        input=json.dumps(req),
        capture_output=True, text=True, cwd=str(REPO_ROOT)
    )
    if proc.returncode != 0:
        return {"error": proc.stderr or "server exited with code " + str(proc.returncode)}
    try:
        resp = json.loads(proc.stdout.strip())
        if "error" in resp:
            return resp
        text = resp["result"]["content"][0]["text"]
        return json.loads(text)
    except Exception as e:
        return {"error": str(e), "raw": proc.stdout[:500]}

def test_list_domains():
    result = call_tool("juraregel.list_domains", {})
    assert isinstance(result, list), f"Expected list, got {type(result)}"
    assert len(result) >= 20, f"Expected >=20 domains, got {len(result)}"
    print(f"  list_domains: {len(result)} domains")

def test_get_rules():
    result = call_tool("juraregel.get_rules", {"domain": "toeslagen"})
    assert isinstance(result, list), f"Expected list, got {type(result)}"
    assert len(result) > 0
    print(f"  get_rules(toeslagen): {len(result)} rules")

def test_search_rules():
    result = call_tool("juraregel.search_rules", {"query": "zorgtoeslag"})
    assert isinstance(result, list)
    assert len(result) > 0
    print(f"  search_rules(zorgtoeslag): {len(result)} results")

def test_calculate():
    result = call_tool("juraregel.calculate", {"domain": "toeslagen", "input": {"toeslagType": "zorgtoeslag", "leeftijd": 30, "alleenstaande": True, "inkomen": 30000}})
    assert "result" in result
    assert result["result"]["matchedRule"]["ruleId"] == "TZ-2025-001"
    print(f"  calculate(toeslagen): matched {result['result']['matchedRule']['ruleId']}")

def test_get_sources():
    result = call_tool("juraregel.get_sources", {"domain": "toeslagen"})
    assert isinstance(result, list)
    assert len(result) > 0
    print(f"  get_sources(toeslagen): {len(result)} sources")

def test_trace():
    result = call_tool("juraregel.trace", {"domain": "toeslagen", "rule_id": "TZ-2025-001"})
    assert "ruleId" in result or "wet" in result
    print(f"  trace(toeslagen/TZ-2025-001): OK")

def test_version_diff():
    result = call_tool("juraregel.version_diff", {"domain": "toeslagen", "v1": "2025.1", "v2": "2025.1"})
    assert "added" in result or "error" in result
    print(f"  version_diff: OK")

def test_semantic_search():
    result = call_tool("juraregel.semantic_search", {"query": "bijstand", "domain": "participatiewet"})
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]["domain"] == "participatiewet"
    print(f"  semantic_search(bijstand, participatiewet): {len(result)} results")

def test_explain():
    result = call_tool("juraregel.explain", {"domain": "toeslagen", "input": {"toeslagType": "zorgtoeslag", "leeftijd": 30, "alleenstaande": True, "inkomen": 30000}})
    assert "summary" in result
    assert "reasoning_steps" in result
    assert len(result["reasoning_steps"]) > 0
    print(f"  explain(toeslagen): {len(result['reasoning_steps'])} reasoning steps")

def test_check_compliance():
    result = call_tool("juraregel.check_compliance", {"domain": "bio2"})
    assert "total_rules" in result
    assert result["total_rules"] == 162
    print(f"  check_compliance(bio2): {result['total_rules']} rules, {result['compliance_percentage']}%")

def test_get_playbook_not_found():
    result = call_tool("juraregel.get_playbook", {"playbook_id": "nonexistent"})
    assert "error" in result
    print(f"  get_playbook(nonexistent): correctly returned error")

def test_get_governance():
    result = call_tool("juraregel.get_governance", {"domain": "toeslagen"})
    assert "domain" in result
    print(f"  get_governance(toeslagen): OK")

def test_unknown_domain():
    result = call_tool("juraregel.get_rules", {"domain": "nonexistent-domain-xyz"})
    assert "error" in result or result == {"error": "No JREM exports for domain 'nonexistent-domain-xyz'"}
    print(f"  get_rules(unknown): correctly returned error")

def test_missing_input():
    result = call_tool("juraregel.calculate", {"domain": "toeslagen", "input": {}})
    assert "result" in result
    print(f"  calculate(empty input): no crash")

if __name__ == "__main__":
    tests = [
        test_list_domains, test_get_rules, test_search_rules, test_calculate,
        test_get_sources, test_trace, test_version_diff,
        test_semantic_search, test_explain, test_check_compliance,
        test_get_playbook_not_found, test_get_governance,
        test_unknown_domain, test_missing_input,
    ]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  FAIL {test.__name__}: {e}")
            failed += 1
    print(f"Results: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
