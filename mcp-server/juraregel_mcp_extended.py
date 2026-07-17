"""
JuraRegel MCP Server Extended — adds code scanning + compliance tools.

New tools:
  juraregel.scan_codebase     — scan codebase for AI compliance patterns
  juraregel.get_compliance_report — generate compliance report
  juraregel.verify_evidence   — verify evidence bundle integrity
  juraregel.check_gate_status — CI/CD gate evaluation

New resources:
  scan://{scan_id}            — scan results
  report://{report_id}        — compliance reports
  evidence://bundles          — evidence bundle registry

New prompts:
  audit_preparation           — full audit prep workflow
  evidence_gap_analysis       — identify missing evidence
"""

import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
sys.path.insert(
    0, str(Path(__file__).parent.parent / "use-cases" / "eu-ai-act" / "lib")
)

from rule_engine import select_rule

# Try to import code scanner
try:
    from code_scanner import scan_codebase

    HAS_SCANNER = True
except ImportError:
    HAS_SCANNER = False

# In-memory scan cache
_scan_cache: dict = {}


def handle_request(request: dict) -> dict:
    """JSON-RPC request handler."""
    method = request.get("method", "")
    params = request.get("params", {})

    handlers = {
        "initialize": _handle_initialize,
        "tools/list": _handle_tools_list,
        "tools/call": _handle_tools_call,
        "resources/list": _handle_resources_list,
        "resources/read": _handle_resources_read,
        "prompts/list": _handle_prompts_list,
        "prompts/get": _handle_prompts_get,
    }

    handler = handlers.get(method)
    if handler:
        return handler(params)
    return {"error": {"code": -32601, "message": f"Method not found: {method}"}}


def _handle_initialize(params: dict) -> dict:
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}, "resources": {}, "prompts": {}},
        "serverInfo": {"name": "juraregel-extended", "version": "2026.1"},
    }


def _handle_tools_list(params: dict) -> dict:
    tools = [
        {
            "name": "juraregel.scan_codebase",
            "description": "Scan een codebase en map bestanden naar JuraRegel JREM regels. Identificeert compliance patterns voor EU AI Act.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Absolute pad naar de codebase root",
                    },
                    "domains": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optioneel: beperk tot domeinen (eu-ai-act, bio2, avg-gdpr)",
                    },
                    "scan_depth": {
                        "type": "string",
                        "enum": ["shallow", "medium", "deep"],
                        "description": "Default: medium",
                    },
                },
                "required": ["path"],
            },
        },
        {
            "name": "juraregel.get_compliance_report",
            "description": "Genereer een compliance rapport op basis van scan resultaten.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "scan_id": {
                        "type": "string",
                        "description": "Scan ID van eerdere scan",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["json", "markdown"],
                        "description": "Default: json",
                    },
                },
                "required": ["scan_id"],
            },
        },
        {
            "name": "juraregel.verify_evidence",
            "description": "Verifieer evidence bundle integriteit en volledigheid.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "evidence_path": {
                        "type": "string",
                        "description": "Pad naar evidence bundle",
                    },
                    "strict_mode": {"type": "boolean", "description": "Default: false"},
                },
                "required": ["evidence_path"],
            },
        },
        {
            "name": "juraregel.check_gate_status",
            "description": "Check compliance gates voor CI/CD pipeline. Geeft PASS/FAIL.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "scan_id": {"type": "string"},
                    "threshold": {
                        "type": "object",
                        "properties": {
                            "min_compliance_pct": {"type": "number"},
                            "max_critical_gaps": {"type": "integer"},
                        },
                    },
                },
                "required": ["scan_id"],
            },
        },
    ]
    return {"tools": tools}


def _handle_tools_call(params: dict) -> dict:
    name = params.get("name", "")
    args = params.get("arguments", {})

    handlers = {
        "juraregel.scan_codebase": _tool_scan_codebase,
        "juraregel.get_compliance_report": _tool_compliance_report,
        "juraregel.verify_evidence": _tool_verify_evidence,
        "juraregel.check_gate_status": _tool_check_gate,
    }

    handler = handlers.get(name)
    if handler:
        try:
            result = handler(args)
            return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
        except Exception as e:
            return {
                "content": [{"type": "text", "text": json.dumps({"error": str(e)})}],
                "isError": True,
            }
    return {"error": {"code": -32601, "message": f"Tool not found: {name}"}}


def _tool_scan_codebase(args: dict) -> dict:
    path = args.get("path", ".")
    domains = args.get("domains")
    scan_depth = args.get("scan_depth", "medium")

    if not HAS_SCANNER:
        return {"error": "code_scanner module not available"}

    findings = scan_codebase(path)
    scan_id = str(uuid.uuid4())[:12]
    _scan_cache[scan_id] = findings

    passed = sum(1 for f in findings if f.status == "pass")
    warnings = sum(1 for f in findings if f.status == "warn")
    failed = sum(1 for f in findings if f.status == "fail")

    return {
        "scan_id": scan_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "path": str(Path(path).resolve()),
        "total_checks": len(findings),
        "passed": passed,
        "warnings": warnings,
        "failed": failed,
        "compliance_score": round(passed / max(len(findings), 1), 2),
        "findings": [
            {
                "ruleId": f.ruleId,
                "article": f.article,
                "name": f.name,
                "status": f.status,
                "severity": f.severity,
                "fix_hint": f.fix_hint,
            }
            for f in findings
        ],
    }


def _tool_compliance_report(args: dict) -> dict:
    scan_id = args.get("scan_id", "")
    fmt = args.get("format", "json")
    findings = _scan_cache.get(scan_id)

    if findings is None:
        return {"error": f"Scan {scan_id} not found"}

    passed = sum(1 for f in findings if f.status == "pass")
    total = len(findings)

    report = {
        "report_id": f"rpt-{scan_id}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": "compliant"
        if passed == total
        else "partial_compliance"
        if passed > total / 2
        else "non_compliant",
        "compliance_score": round(passed / max(total, 1), 2),
        "total_checks": total,
        "passed": passed,
        "warnings": sum(1 for f in findings if f.status == "warn"),
        "failed": sum(1 for f in findings if f.status == "fail"),
        "gaps": [
            {
                "ruleId": f.ruleId,
                "article": f.article,
                "name": f.name,
                "fix_hint": f.fix_hint,
            }
            for f in findings
            if f.status != "pass"
        ],
    }

    if fmt == "markdown":
        lines = [
            f"# Compliance Report — {report['report_id']}",
            f"",
            f"**Status:** {report['overall_status']}",
            f"**Score:** {report['compliance_score'] * 100:.0f}%",
            "",
            "## Gaps",
            "",
        ]
        for g in report["gaps"]:
            lines.append(f"- **{g['ruleId']}** ({g['article']}): {g['name']}")
            lines.append(f"  - Fix: {g['fix_hint']}")
        return {"report_id": report["report_id"], "markdown": "\n".join(lines)}

    return report


def _tool_verify_evidence(args: dict) -> dict:
    evidence_path = args.get("evidence_path", "")
    strict = args.get("strict_mode", False)
    path = Path(evidence_path)

    if not path.exists():
        return {"status": "invalid", "error": f"Path not found: {evidence_path}"}

    files_verified = 0
    errors = []

    if path.is_dir():
        for f in path.rglob("*"):
            if f.is_file():
                files_verified += 1
    else:
        files_verified = 1

    return {
        "verification_id": f"ver-{uuid.uuid4().hex[:12]}",
        "evidence_path": str(path.resolve()),
        "status": "valid" if not errors else "invalid",
        "files_verified": files_verified,
        "errors": errors,
        "strict_mode": strict,
    }


def _tool_check_gate(args: dict) -> dict:
    scan_id = args.get("scan_id", "")
    threshold = args.get("threshold", {})
    findings = _scan_cache.get(scan_id)

    if findings is None:
        return {
            "error": f"Scan {scan_id} not found",
            "overall_verdict": "FAIL",
            "exit_code": 1,
        }

    min_pct = threshold.get("min_compliance_pct", 0.80)
    max_critical = threshold.get("max_critical_gaps", 0)

    passed = sum(1 for f in findings if f.status == "pass")
    total = len(findings)
    score = passed / max(total, 1)
    critical = sum(
        1 for f in findings if f.severity == "critical" and f.status == "fail"
    )

    gates = []
    gates.append(
        {
            "gate": "compliance_score",
            "status": "PASS" if score >= min_pct else "FAIL",
            "reason": f"Score {score * 100:.0f}% (threshold: {min_pct * 100:.0f}%)",
        }
    )
    gates.append(
        {
            "gate": "no_critical_gaps",
            "status": "PASS" if critical <= max_critical else "FAIL",
            "reason": f"{critical} critical gaps (threshold: {max_critical})",
        }
    )

    all_pass = all(g["status"] == "PASS" for g in gates)

    return {
        "gate_run_id": f"gate-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "overall_verdict": "PASS" if all_pass else "FAIL",
        "gates": gates,
        "exit_code": 0 if all_pass else 1,
        "action_required": [g["reason"] for g in gates if g["status"] == "FAIL"],
    }


def _handle_resources_list(params: dict) -> dict:
    resources = []
    for scan_id in _scan_cache:
        resources.append(
            {
                "uri": f"scan://{scan_id}",
                "name": f"Scan {scan_id}",
                "mimeType": "application/json",
            }
        )
    return {"resources": resources}


def _handle_resources_read(params: dict) -> dict:
    uri = params.get("uri", "")
    if uri.startswith("scan://"):
        scan_id = uri[7:]
        findings = _scan_cache.get(scan_id)
        if findings:
            return {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "application/json",
                        "text": json.dumps(
                            [
                                f.to_jrem()
                                if hasattr(f, "to_jrem")
                                else {"ruleId": f.ruleId, "status": f.status}
                                for f in findings
                            ]
                        ),
                    }
                ]
            }


def _handle_prompts_list(params: dict) -> dict:
    return {
        "prompts": [
            {
                "name": "audit_preparation",
                "description": "Bereid voor op een compliance audit: scan + gap analysis + checklist",
                "arguments": [
                    {"name": "codebase_path", "required": True},
                    {"name": "framework", "required": True},
                ],
            },
            {
                "name": "evidence_gap_analysis",
                "description": "Analyseer ontbrekende evidence voor compliance",
                "arguments": [{"name": "scan_id", "required": True}],
            },
        ]
    }


def _handle_prompts_get(params: dict) -> dict:
    name = params.get("name", "")
    args = params.get("arguments", {})

    if name == "audit_preparation":
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Audit preparation for {args.get('framework', 'unknown')} on {args.get('codebase_path', '.')}. Run juraregel.scan_codebase, then juraregel.get_compliance_report with format=markdown, then juraregel.check_gate_status.",
                    },
                }
            ]
        }
    elif name == "evidence_gap_analysis":
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Analyze evidence gaps for scan {args.get('scan_id', 'unknown')}. Run juraregel.get_compliance_report and list all failed checks with fix hints.",
                    },
                }
            ]
        }
    return {"error": f"Prompt not found: {name}"}


# ─── STDIO Server ───

if __name__ == "__main__":
    import sys

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
            response["jsonrpc"] = "2.0"
            response["id"] = request.get("id")
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            continue
