"""
EU AI Act Code Scanner — static analysis of Python/TS/JS codebases for AI compliance.

Ported from AIR Blackbox (airblackbox/airblackbox) — adapted for JuraRegel's JREM format.
14 checks across Articles 9, 10, 11, 12, 14, 15.

Each check returns a CodeFinding with JREM-compatible structure.
"""

import os
import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class CodeFinding:
    """A single compliance finding in JREM-compatible format."""

    ruleId: str
    article: str
    name: str
    status: str  # "pass", "warn", "fail"
    evidence: str
    detection: str = "auto"
    fix_hint: str = ""
    files: list = field(default_factory=list)
    severity: str = "info"  # info, warning, error, critical
    maturity: str = "L1"

    def to_jrem(self) -> dict:
        """Convert to JREM rule format."""
        article_clean = self.article.replace(" ", "_").replace("(", "").replace(")", "")
        return {
            "ruleId": self.ruleId,
            "name": self.name,
            "priority": 100 if self.status == "fail" else 50,
            "legalStatus": "wettelijk",
            "sourceRefs": [
                {
                    "type": "wetsartikel",
                    "title": f"EU AI Act \u2014 {self.article}",
                    "section": self.ruleId,
                    "url": "https://eur-lex.europa.eu/eli/reg/2024/1689",
                }
            ],
            "conditions": {
                "detection": self.detection,
                "pattern": self.name,
                "status": self.status,
            },
            "outcome": {
                "category": f"uc_eu-ai-act_code_{article_clean}",
                "confidence": "deterministic" if self.detection == "auto" else "hybrid",
                "manualReviewRequired": self.status == "fail",
                "severity": self.severity,
                "fix_hint": self.fix_hint,
            },
            "evidence": self.evidence,
            "files": self.files[:10],
            "maturity": self.maturity,
        }


def scan_codebase(scan_path: str) -> List[CodeFinding]:
    """Walk all source files and check for AI compliance patterns."""
    source_files = _find_source_files(scan_path)
    if not source_files:
        return [
            CodeFinding(
                ruleId="AIR-SCAN-000",
                article="Scan",
                name="Source files",
                status="warn",
                evidence=f"No source files found in {scan_path}",
                fix_hint="Point --scan at a directory containing Python, TypeScript, or JavaScript code",
            )
        ]

    file_contents = {}
    for fp in source_files:
        try:
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                file_contents[fp] = f.read()
        except Exception:
            continue

    findings = []
    findings.extend(_check_error_handling(file_contents, scan_path))
    findings.extend(_check_fallback_patterns(file_contents, scan_path))
    findings.extend(_check_input_validation(file_contents, scan_path))
    findings.extend(_check_pii_handling(file_contents, scan_path))
    findings.extend(_check_docstrings(file_contents, scan_path))
    findings.extend(_check_type_hints(file_contents, scan_path))
    findings.extend(_check_logging(file_contents, scan_path))
    findings.extend(_check_tracing(file_contents, scan_path))
    findings.extend(_check_human_in_loop(file_contents, scan_path))
    findings.extend(_check_rate_limiting(file_contents, scan_path))
    findings.extend(_check_retry_logic(file_contents, scan_path))
    findings.extend(_check_injection_defense(file_contents, scan_path))
    findings.extend(_check_output_validation(file_contents, scan_path))
    findings.extend(_check_unsafe_input(file_contents, scan_path))
    return findings


def _find_source_files(scan_path: str) -> List[str]:
    skip_dirs = {
        "node_modules",
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "env",
        ".env",
        ".tox",
        ".mypy_cache",
        ".pytest_cache",
        "dist",
        "build",
        "egg-info",
        ".eggs",
        "site-packages",
        ".swarm",
        ".opencode",
    }
    extensions = {".py", ".ts", ".tsx", ".js", ".jsx"}
    source_files = []
    for root, dirs, files in os.walk(scan_path):
        dirs[:] = [
            d for d in dirs if d not in skip_dirs and not d.endswith(".egg-info")
        ]
        for fname in files:
            if any(fname.endswith(ext) for ext in extensions):
                source_files.append(os.path.join(root, fname))
    return source_files


def _rel(filepath: str, scan_path: str) -> str:
    return os.path.relpath(filepath, scan_path)


def _summarize_files(files: list, scan_path: str, max_files: int = 5) -> tuple:
    rel_files = [_rel(f, scan_path) for f in files[:max_files]]
    suffix = ", ".join(rel_files)
    if len(files) > max_files:
        suffix += f" (+{len(files) - max_files} more)"
    return files[:max_files], suffix


def _check_error_handling(file_contents: dict, scan_path: str) -> List[CodeFinding]:
    llm_patterns = [
        r"\.chat\.completions\.create\(",
        r"\.completions\.create\(",
        r"\.invoke\(",
        r"\.run\(",
        r"\.generate\(",
        r"\.predict\(",
        r"\.agenerate\(",
        r"\.ainvoke\(",
        r"ChatOpenAI\(",
        r"OpenAI\(",
        r"Anthropic\(",
        r"generate\(",
        r"chat\(",
    ]
    combined = "|".join(llm_patterns)
    files_with_llm = []
    files_with_handling = []
    for fp, content in file_contents.items():
        if re.search(combined, content):
            files_with_llm.append(fp)
            if re.search(r"\btry\b.*?\bexcept\b", content, re.DOTALL):
                files_with_handling.append(fp)
    if not files_with_llm:
        return [
            CodeFinding(
                ruleId="AIR-09-01",
                article="Art 9(1)",
                name="LLM call error handling",
                status="pass",
                evidence="No direct LLM API calls detected",
                severity="info",
            )
        ]
    covered = len(files_with_handling)
    total = len(files_with_llm)
    uncovered = [f for f in files_with_llm if f not in files_with_handling]
    _, suffix = _summarize_files(uncovered, scan_path)
    if covered == total:
        return [
            CodeFinding(
                ruleId="AIR-09-01",
                article="Art 9(1)",
                name="LLM call error handling",
                status="pass",
                evidence=f"All {total} files with LLM calls have try/except",
                severity="info",
            )
        ]
    return [
        CodeFinding(
            ruleId="AIR-09-01",
            article="Art 9(1)",
            name="LLM call error handling",
            status="fail" if covered == 0 else "warn",
            evidence=f"{covered}/{total} files with LLM calls have error handling. Missing: {suffix}",
            fix_hint="Wrap LLM API calls in try/except",
            files=uncovered,
            severity="error" if covered == 0 else "warning",
        )
    ]


def _check_fallback_patterns(file_contents: dict, scan_path: str) -> List[CodeFinding]:
    patterns = [
        r"fallback",
        r"retry",
        r"backoff",
        r"with_fallbacks",
        r"with_retry",
        r"tenacity",
        r"max_retries",
        r"default_response",
    ]
    combined = "|".join(patterns)
    files_found = [
        fp for fp, c in file_contents.items() if re.search(combined, c, re.IGNORECASE)
    ]
    if files_found:
        _, suffix = _summarize_files(files_found, scan_path)
        return [
            CodeFinding(
                ruleId="AIR-09-02",
                article="Art 9(2)",
                name="Fallback/recovery patterns",
                status="pass",
                evidence=f"Found in {len(files_found)} file(s): {suffix}",
                severity="info",
            )
        ]
    return [
        CodeFinding(
            ruleId="AIR-09-02",
            article="Art 9(2)",
            name="Fallback/recovery patterns",
            status="warn",
            evidence="No fallback or retry patterns detected",
            fix_hint="Add fallback logic for LLM failures",
            severity="warning",
        )
    ]


def _check_input_validation(file_contents: dict, scan_path: str) -> List[CodeFinding]:
    patterns = [
        r"pydantic",
        r"BaseModel",
        r"validator",
        r"field_validator",
        r"validate_input",
        r"input_schema",
        r"json_schema",
        r"TypedDict",
        r"dataclass",
        r"InputGuard",
        r"sanitize",
        r"zod",
        r"z\.object",
        r"z\.string",
        r"z\.number",
        r"joi",
        r"yup",
        r"schema",
    ]
    combined = "|".join(patterns)
    files_found = [fp for fp, c in file_contents.items() if re.search(combined, c)]
    total = len(file_contents)
    if files_found:
        _, suffix = _summarize_files(files_found, scan_path)
        return [
            CodeFinding(
                ruleId="AIR-10-01",
                article="Art 10(2)",
                name="Input validation",
                status="pass",
                evidence=f"Found in {len(files_found)}/{total} files: {suffix}",
                severity="info",
            )
        ]
    return [
        CodeFinding(
            ruleId="AIR-10-01",
            article="Art 10(2)",
            name="Input validation",
            status="warn",
            evidence="No structured input validation detected",
            fix_hint="Use Pydantic/Zod/dataclasses to validate inputs",
            severity="warning",
        )
    ]


def _check_pii_handling(file_contents: dict, scan_path: str) -> List[CodeFinding]:
    patterns = [
        r"pii",
        r"redact",
        r"mask",
        r"anonymize",
        r"tokenize_pii",
        r"presidio",
        r"scrub",
        r"private",
        r"sensitive",
        r"data_protection",
        r"gdpr",
        r"personal_data",
    ]
    combined = "|".join(patterns)
    files_found = [
        fp for fp, c in file_contents.items() if re.search(combined, c, re.IGNORECASE)
    ]
    if files_found:
        _, suffix = _summarize_files(files_found, scan_path)
        return [
            CodeFinding(
                ruleId="AIR-10-02",
                article="Art 10(3)",
                name="PII handling in code",
                status="pass",
                evidence=f"Found in {len(files_found)} file(s): {suffix}",
                severity="info",
            )
        ]
    return [
        CodeFinding(
            ruleId="AIR-10-02",
            article="Art 10(3)",
            name="PII handling in code",
            status="warn",
            evidence="No PII detection/redaction patterns found",
            fix_hint="Add PII detection before sending data to LLM",
            severity="warning",
        )
    ]


def _check_docstrings(file_contents: dict, scan_path: str) -> List[CodeFinding]:
    total_defs = 0
    documented_defs = 0
    for fp, content in file_contents.items():
        lines = content.split("\n")
        for i, line in enumerate(lines):
            stripped = line.strip()
            if (
                stripped.startswith("def ")
                or stripped.startswith("class ")
                or stripped.startswith("function ")
                or stripped.startswith("export function ")
            ):
                if stripped.startswith("def _") or stripped.startswith("function _"):
                    continue
                total_defs += 1
                for j in range(i + 1, min(i + 4, len(lines))):
                    next_line = lines[j].strip()
                    if next_line == "":
                        continue
                    if (
                        next_line.startswith('"""')
                        or next_line.startswith("'''")
                        or next_line.startswith("/**")
                    ):
                        documented_defs += 1
                    break
    if total_defs == 0:
        return [
            CodeFinding(
                ruleId="AIR-11-01",
                article="Art 11(1)",
                name="Code documentation",
                status="pass",
                evidence="No public functions/classes found",
                severity="info",
            )
        ]
    pct = (documented_defs / total_defs * 100) if total_defs > 0 else 0
    status = "pass" if pct >= 60 else "warn" if pct >= 30 else "fail"
    return [
        CodeFinding(
            ruleId="AIR-11-01",
            article="Art 11(1)",
            name="Code documentation",
            status=status,
            evidence=f"{documented_defs}/{total_defs} documented ({pct:.0f}%)",
            fix_hint="Add docstrings to public functions",
            severity="info" if status == "pass" else "warning",
        )
    ]


def _check_type_hints(file_contents: dict, scan_path: str) -> List[CodeFinding]:
    TYPE_RE = re.compile(
        r":\s*(str|int|float|bool|bytes|None|list|dict|set|tuple|frozenset|List|Dict|Set|Tuple|FrozenSet|Optional|Union|Any|Type|Callable|Coroutine|Sequence|Iterable|Iterator|Generator|AsyncGenerator|Mapping|MutableMapping|Path|PurePath|UUID|Pattern|Match|date|datetime|time|timedelta|Decimal|[A-Z][a-zA-Z0-9_]*)"
    )
    total_defs = 0
    typed_defs = 0
    for fp, content in file_contents.items():
        lines = content.split("\n")
        i = 0
        while i < len(lines):
            stripped = lines[i].strip()
            if (stripped.startswith("def ") and not stripped.startswith("def _")) or (
                stripped.startswith("function ")
                and not stripped.startswith("function _")
            ):
                full_sig = stripped
                j = i + 1
                while j < len(lines) and (
                    full_sig.rstrip().endswith("\\")
                    or full_sig.count("(") > full_sig.count(")")
                ):
                    next_line = lines[j].strip()
                    if full_sig.rstrip().endswith("\\"):
                        full_sig = full_sig.rstrip()[:-1]
                    full_sig += " " + next_line
                    j += 1
                total_defs += 1
                if "->" in full_sig or TYPE_RE.search(full_sig):
                    typed_defs += 1
                i = j
            else:
                i += 1
    if total_defs == 0:
        return []
    pct = typed_defs / total_defs * 100
    status = "pass" if pct >= 50 else "warn" if pct >= 20 else "fail"
    return [
        CodeFinding(
            ruleId="AIR-11-02",
            article="Art 11(2)",
            name="Type annotations",
            status=status,
            evidence=f"{typed_defs}/{total_defs} functions have type hints ({pct:.0f}%)",
            fix_hint="Add type hints to function signatures",
            severity="info" if status == "pass" else "warning",
        )
    ]


def _check_logging(file_contents: dict, scan_path: str) -> List[CodeFinding]:
    patterns = [
        r"import logging",
        r"from logging",
        r"getLogger",
        r"structlog",
        r"loguru",
        r"logger\.",
        r"logging\.",
        r"console\.(log|error|warn|info)",
        r"pino",
        r"winston",
    ]
    combined = "|".join(patterns)
    files_found = [fp for fp, c in file_contents.items() if re.search(combined, c)]
    total = len(file_contents)
    if not files_found:
        return [
            CodeFinding(
                ruleId="AIR-12-01",
                article="Art 12(1)",
                name="Application logging",
                status="fail",
                evidence="No logging framework detected",
                fix_hint="Add import logging and log key decisions",
                severity="error",
            )
        ]
    pct = len(files_found) / total * 100 if total > 0 else 0
    _, suffix = _summarize_files(files_found, scan_path)
    return [
        CodeFinding(
            ruleId="AIR-12-01",
            article="Art 12(1)",
            name="Application logging",
            status="pass" if pct >= 20 else "warn",
            evidence=f"Found in {len(files_found)}/{total} files ({pct:.0f}%): {suffix}",
            severity="info" if pct >= 20 else "warning",
        )
    ]


def _check_tracing(file_contents: dict, scan_path: str) -> List[CodeFinding]:
    patterns = [
        r"opentelemetry",
        r"otel",
        r"trace_id",
        r"span_id",
        r"run_id",
        r"request_id",
        r"correlation_id",
        r"langsmith",
        r"langfuse",
        r"helicone",
        r"arize",
        r"wandb",
        r"mlflow",
        r"callbacks",
    ]
    combined = "|".join(patterns)
    files_found = [
        fp for fp, c in file_contents.items() if re.search(combined, c, re.IGNORECASE)
    ]
    if files_found:
        _, suffix = _summarize_files(files_found, scan_path)
        return [
            CodeFinding(
                ruleId="AIR-12-02",
                article="Art 12(2)",
                name="Tracing/observability",
                status="pass",
                evidence=f"Found in {len(files_found)} file(s): {suffix}",
                severity="info",
            )
        ]
    return [
        CodeFinding(
            ruleId="AIR-12-02",
            article="Art 12(2)",
            name="Tracing/observability",
            status="warn",
            evidence="No tracing/observability integration detected",
            fix_hint="Add OpenTelemetry or LangSmith to track AI decisions",
            severity="warning",
        )
    ]


def _check_human_in_loop(file_contents: dict, scan_path: str) -> List[CodeFinding]:
    patterns = [
        r"human_in_the_loop",
        r"human_approval",
        r"require_approval",
        r"approval_gate",
        r"confirm",
        r"ask_human",
        r"human_input",
        r"HumanApprovalCallbackHandler",
        r"input\(",
        r"human_feedback",
        r"manual_review",
        r"approval_required",
    ]
    combined = "|".join(patterns)
    files_found = [
        fp for fp, c in file_contents.items() if re.search(combined, c, re.IGNORECASE)
    ]
    if files_found:
        _, suffix = _summarize_files(files_found, scan_path)
        return [
            CodeFinding(
                ruleId="AIR-14-01",
                article="Art 14(1)",
                name="Human-in-the-loop",
                status="pass",
                evidence=f"Found in {len(files_found)} file(s): {suffix}",
                severity="info",
            )
        ]
    return [
        CodeFinding(
            ruleId="AIR-14-01",
            article="Art 14(1)",
            name="Human-in-the-loop",
            status="warn",
            evidence="No human approval gates detected",
            fix_hint="Add approval gates for high-risk actions",
            severity="warning",
        )
    ]


def _check_rate_limiting(file_contents: dict, scan_path: str) -> List[CodeFinding]:
    patterns = [
        r"rate_limit",
        r"max_tokens",
        r"max_iterations",
        r"max_steps",
        r"budget",
        r"token_limit",
        r"cost_limit",
        r"max_retries",
        r"max_calls",
        r"throttle",
        r"cooldown",
        r"max_rpm",
    ]
    combined = "|".join(patterns)
    files_found = [
        fp for fp, c in file_contents.items() if re.search(combined, c, re.IGNORECASE)
    ]
    if files_found:
        _, suffix = _summarize_files(files_found, scan_path)
        return [
            CodeFinding(
                ruleId="AIR-14-02",
                article="Art 14(3)",
                name="Usage limits/budget",
                status="pass",
                evidence=f"Found in {len(files_found)} file(s): {suffix}",
                severity="info",
            )
        ]
    return [
        CodeFinding(
            ruleId="AIR-14-02",
            article="Art 14(3)",
            name="Usage limits/budget",
            status="warn",
            evidence="No rate limiting or budget controls detected",
            fix_hint="Set max_tokens, max_iterations, or budget limits",
            severity="warning",
        )
    ]


def _check_retry_logic(file_contents: dict, scan_path: str) -> List[CodeFinding]:
    patterns = [
        r"retry",
        r"backoff",
        r"tenacity",
        r"max_retries",
        r"exponential_backoff",
        r"with_retry",
        r"Retry\(",
    ]
    combined = "|".join(patterns)
    files_found = [
        fp for fp, c in file_contents.items() if re.search(combined, c, re.IGNORECASE)
    ]
    if files_found:
        _, suffix = _summarize_files(files_found, scan_path)
        return [
            CodeFinding(
                ruleId="AIR-15-01",
                article="Art 15(1)",
                name="Retry/backoff logic",
                status="pass",
                evidence=f"Found in {len(files_found)} file(s): {suffix}",
                severity="info",
            )
        ]
    return [
        CodeFinding(
            ruleId="AIR-15-01",
            article="Art 15(1)",
            name="Retry/backoff logic",
            status="warn",
            evidence="No retry or backoff patterns detected",
            fix_hint="Add retry logic with exponential backoff for LLM API calls",
            severity="warning",
        )
    ]


def _check_injection_defense(file_contents: dict, scan_path: str) -> List[CodeFinding]:
    patterns = [
        r"injection",
        r"sanitize",
        r"escape",
        r"guardrail",
        r"content_filter",
        r"moderation",
        r"safety_check",
        r"prompt_guard",
        r"nemo_guardrails",
        r"rebuff",
        r"lakera",
    ]
    combined = "|".join(patterns)
    files_found = [
        fp for fp, c in file_contents.items() if re.search(combined, c, re.IGNORECASE)
    ]
    if files_found:
        _, suffix = _summarize_files(files_found, scan_path)
        return [
            CodeFinding(
                ruleId="AIR-15-02",
                article="Art 15(2)",
                name="Prompt injection defense",
                status="pass",
                evidence=f"Found in {len(files_found)} file(s): {suffix}",
                severity="info",
            )
        ]
    return [
        CodeFinding(
            ruleId="AIR-15-02",
            article="Art 15(2)",
            name="Prompt injection defense",
            status="warn",
            evidence="No prompt injection defense patterns detected",
            fix_hint="Add input sanitization or guardrails",
            severity="warning",
        )
    ]


def _check_output_validation(file_contents: dict, scan_path: str) -> List[CodeFinding]:
    patterns = [
        r"output_parser",
        r"OutputParser",
        r"PydanticOutputParser",
        r"JsonOutputParser",
        r"parse_output",
        r"validate_output",
        r"response_model",
        r"structured_output",
        r"output_schema",
        r"response_format",
        r"zod.*parse",
        r"schema\.parse",
        r"validate\(",
    ]
    combined = "|".join(patterns)
    files_found = [fp for fp, c in file_contents.items() if re.search(combined, c)]
    if files_found:
        _, suffix = _summarize_files(files_found, scan_path)
        return [
            CodeFinding(
                ruleId="AIR-15-03",
                article="Art 15(3)",
                name="LLM output validation",
                status="pass",
                evidence=f"Found in {len(files_found)} file(s): {suffix}",
                severity="info",
            )
        ]
    return [
        CodeFinding(
            ruleId="AIR-15-03",
            article="Art 15(3)",
            name="LLM output validation",
            status="warn",
            evidence="No structured output validation detected",
            fix_hint="Use output parsers (Pydantic, JSON schema) to validate LLM responses",
            severity="warning",
        )
    ]


def _check_unsafe_input(file_contents: dict, scan_path: str) -> List[CodeFinding]:
    patterns = [
        r"eval\s*\(",
        r"exec\s*\(",
        r"Function\s*\(",
        r"new\s+Function\s*\(",
        r"subprocess\.call\s*\(.*shell\s*=\s*True",
        r"os\.system\s*\(",
        r"child_process\.exec\s*\(",
    ]
    combined = "|".join(patterns)
    files_found = [fp for fp, c in file_contents.items() if re.search(combined, c)]
    if files_found:
        _, suffix = _summarize_files(files_found, scan_path)
        return [
            CodeFinding(
                ruleId="AIR-15-04",
                article="Art 15(4)",
                name="Unsafe code execution",
                status="fail",
                evidence=f"Dangerous patterns in {len(files_found)} file(s): {suffix}",
                fix_hint="Avoid eval/exec on user input or LLM content",
                files=files_found,
                severity="critical",
            )
        ]
    return [
        CodeFinding(
            ruleId="AIR-15-04",
            article="Art 15(4)",
            name="Unsafe code execution",
            status="pass",
            evidence="No dangerous code execution patterns detected",
            severity="info",
        )
    ]
