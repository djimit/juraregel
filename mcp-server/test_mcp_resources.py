#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
MCP_SERVER = REPO_ROOT / "mcp-server" / "juraregel_mcp.py"
PYTHON = sys.executable

def call_mcp(method, params=None):
    req = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
    proc = subprocess.run([PYTHON, str(MCP_SERVER)], input=json.dumps(req), capture_output=True, text=True, cwd=str(REPO_ROOT))
    if proc.returncode != 0:
        return {"error": proc.stderr}
    return json.loads(proc.stdout.strip())

def test_resources_list():
    result = call_mcp("resources/list")
    assert "result" in result
    resources = result["result"]["resources"]
    assert len(resources) >= 3
    uris = [r["uri"] for r in resources]
    assert "laws://list" in uris
    assert "laws://summary" in uris
    print("  resources/list: OK")

def test_resource_read_laws_list():
    result = call_mcp("resources/read", {"uri": "laws://list"})
    assert "result" in result
    data = json.loads(result["result"]["contents"][0]["text"])
    assert len(data) >= 20
    print("  resources/read(laws://list): OK")

def test_resource_read_summary():
    result = call_mcp("resources/read", {"uri": "laws://summary"})
    assert "result" in result
    data = json.loads(result["result"]["contents"][0]["text"])
    assert data["total_rules"] == data["total_versioned_rules"] == 702
    assert data["total_current_rules"] <= data["total_versioned_rules"]
    assert data["total_rule_sets"] == 34
    assert data["total_repository_domains"] == 33
    print("  resources/read(laws://summary): OK")

def test_resource_read_spec():
    result = call_mcp("resources/read", {"uri": "laws://toeslagen/spec"})
    assert "result" in result
    data = json.loads(result["result"]["contents"][0]["text"])
    assert data["domain"] == "toeslagen"
    print("  resources/read(laws://toeslagen/spec): OK")

def test_resource_read_profile():
    result = call_mcp("resources/read", {"uri": "profile://toeslagen"})
    assert "result" in result
    data = json.loads(result["result"]["contents"][0]["text"])
    assert "input_profile" in data
    assert "output_profile" in data
    print("  resources/read(profile://toeslagen): OK")

def test_prompts_list():
    result = call_mcp("prompts/list")
    assert "result" in result
    prompts = result["result"]["prompts"]
    assert len(prompts) >= 3
    names = [p["name"] for p in prompts]
    assert "check_all_benefits" in names
    print("  prompts/list: OK")

def test_prompt_get():
    result = call_mcp("prompts/get", {"name": "check_all_benefits", "arguments": {"leeftijd": 30, "inkomen": 30000, "huishouden": "alleenstaande"}})
    assert "result" in result
    assert "messages" in result["result"]
    print("  prompts/get: OK")

def test_unknown_resource():
    result = call_mcp("resources/read", {"uri": "unknown://test"})
    assert "error" in result
    print("  resources/read(unknown): OK")

def test_unknown_prompt():
    result = call_mcp("prompts/get", {"name": "unknown_prompt", "arguments": {}})
    assert "error" in result
    print("  prompts/get(unknown): OK")

if __name__ == "__main__":
    tests = [test_resources_list, test_resource_read_laws_list, test_resource_read_summary,
             test_resource_read_spec, test_resource_read_profile, test_prompts_list,
             test_prompt_get, test_unknown_resource, test_unknown_prompt]
    passed = 0; failed = 0
    for test in tests:
        try:
            test(); passed += 1
        except Exception as e:
            print(f"  FAIL {test.__name__}: {e}"); failed += 1
    print(f"Results: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
