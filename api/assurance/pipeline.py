"""JLAIF Pipeline — End-to-end assurance orchestration.

Composes individual assurance modules into a unified pipeline with:
- Automatic module ordering by priority
- Error recovery (non-critical modules don't crash the pipeline)
- Shared state between modules
- Metrics collection per module
- Plugin-based extensibility
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Protocol

logger = logging.getLogger(__name__)


class ModuleCategory(str, Enum):
    """Module categories determine execution order."""

    PREPROCESSING = "preprocessing"
    ANALYSIS = "analysis"
    SCORING = "scoring"
    POSTPROCESSING = "postprocessing"
    REPORTING = "reporting"


@dataclass
class ModuleResult:
    """Result from a single module execution."""

    module_name: str
    category: ModuleCategory
    success: bool
    findings: list[dict[str, Any]] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    execution_time_ms: int = 0


@dataclass
class PipelineState:
    """Shared state across pipeline modules."""

    input_text: str
    context: dict[str, Any]
    intermediate_results: dict[str, Any] = field(default_factory=dict)
    findings: list[dict[str, Any]] = field(default_factory=list)
    errors: list[dict[str, str]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_result(self, key: str, value: Any) -> None:
        self.intermediate_results[key] = value

    def add_finding(self, finding: dict[str, Any]) -> None:
        self.findings.append(finding)

    def add_error(self, module: str, error: str) -> None:
        self.errors.append({"module": module, "error": error})

    def get(self, key: str, default: Any = None) -> Any:
        return self.intermediate_results.get(key, default)


class JLAIFModule(Protocol):
    """Protocol for assurance modules."""

    name: str
    priority: int
    category: ModuleCategory
    critical: bool

    def execute(self, state: PipelineState) -> ModuleResult: ...


@dataclass
class PipelineReport:
    """Complete pipeline execution report."""

    pipeline_id: str
    timestamp: str
    input_summary: str
    modules_executed: int
    modules_failed: int
    total_findings: int
    findings_by_category: dict[str, int]
    severity_distribution: dict[str, int]
    module_results: list[ModuleResult]
    total_execution_time_ms: int
    release_decision: str
    errors: list[dict[str, str]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "pipeline_id": self.pipeline_id,
            "timestamp": self.timestamp,
            "modules_executed": self.modules_executed,
            "modules_failed": self.modules_failed,
            "total_findings": self.total_findings,
            "findings_by_category": self.findings_by_category,
            "severity_distribution": self.severity_distribution,
            "total_execution_time_ms": self.total_execution_time_ms,
            "release_decision": self.release_decision,
            "errors": self.errors,
        }


class JLAIFPipeline:
    """End-to-end assurance pipeline."""

    def __init__(self, name: str = "jlaif-pipeline"):
        self.name = name
        self._modules: list[JLAIFModule] = []
        self._pre_hooks: list[Callable[[PipelineState], None]] = []
        self._post_hooks: list[Callable[[PipelineState, PipelineReport], None]] = []

    def register(self, module: JLAIFModule) -> "JLAIFPipeline":
        """Register an assurance module."""
        self._modules.append(module)
        self._modules.sort(key=lambda m: m.priority)
        logger.debug(f"Registered module: {module.name} (priority={module.priority})")
        return self

    def register_bulk(self, *modules: JLAIFModule) -> "JLAIFPipeline":
        """Register multiple modules at once."""
        for module in modules:
            self.register(module)
        return self

    def add_pre_hook(self, hook: Callable[[PipelineState], None]) -> "JLAIFPipeline":
        """Add a pre-execution hook."""
        self._pre_hooks.append(hook)
        return self

    def add_post_hook(
        self, hook: Callable[[PipelineState, PipelineReport], None]
    ) -> "JLAIFPipeline":
        """Add a post-execution hook."""
        self._post_hooks.append(hook)
        return self

    def execute(
        self, input_text: str, context: dict[str, Any] | None = None
    ) -> PipelineReport:
        """Execute the full pipeline."""
        start = time.time()
        context = context or {}

        state = PipelineState(input_text=input_text, context=context)

        # Pre-hooks
        for hook in self._pre_hooks:
            hook(state)

        # Execute modules
        module_results = []
        modules_executed = 0
        modules_failed = 0
        findings_by_category: dict[str, int] = {}

        for module in self._modules:
            module_start = time.time()
            try:
                if not self._validate_module(module):
                    raise ValueError(f"Module {module.name} failed self-validation")

                result = module.execute(state)
                result.execution_time_ms = int((time.time() - module_start) * 1000)
                module_results.append(result)
                modules_executed += 1

                # Aggregate findings
                cat = module.category.value
                findings_by_category[cat] = findings_by_category.get(cat, 0) + len(
                    result.findings
                )

                for finding in result.findings:
                    state.add_finding(finding)

            except Exception as e:
                modules_failed += 1
                error_msg = str(e)
                state.add_error(module.name, error_msg)
                module_results.append(
                    ModuleResult(
                        module_name=module.name,
                        category=module.category,
                        success=False,
                        error=error_msg,
                        execution_time_ms=int((time.time() - module_start) * 1000),
                    )
                )
                logger.error(f"Module {module.name} failed: {error_msg}")

                if module.critical:
                    logger.warning(
                        f"Critical module {module.name} failed — stopping pipeline"
                    )
                    break

        # Aggregate severity distribution
        severity_dist: dict[str, int] = {}
        for finding in state.findings:
            sev = finding.get("severity", "unknown")
            severity_dist[sev] = severity_dist.get(sev, 0) + 1

        # Determine release decision
        release = self._determine_release(state.findings)

        total_time = int((time.time() - start) * 1000)

        report = PipelineReport(
            pipeline_id=f"pipe-{int(start)}",
            timestamp=datetime.now().isoformat(),
            input_summary=input_text[:100],
            modules_executed=modules_executed,
            modules_failed=modules_failed,
            total_findings=len(state.findings),
            findings_by_category=findings_by_category,
            severity_distribution=severity_dist,
            module_results=module_results,
            total_execution_time_ms=total_time,
            release_decision=release,
            errors=state.errors,
        )

        # Post-hooks
        for hook in self._post_hooks:
            hook(state, report)

        return report

    def _validate_module(self, module: JLAIFModule) -> bool:
        """Validate a module before execution."""
        return hasattr(module, "execute") and callable(module.execute)

    def _determine_release(self, findings: list[dict]) -> str:
        """Determine release decision from findings."""
        for finding in findings:
            sev = finding.get("severity", "")
            if sev in ("S4", "S5"):
                return "NO-GO"

        material_count = sum(1 for f in findings if f.get("severity") == "S3")
        if material_count > 3:
            return "NO-GO"
        elif material_count > 0:
            return "CONDITIONAL"

        return "GO"

    def get_registered_modules(self) -> list[dict[str, Any]]:
        """Get list of registered modules."""
        return [
            {
                "name": m.name,
                "priority": m.priority,
                "category": m.category.value,
                "critical": m.critical,
            }
            for m in self._modules
        ]


# ─── Convenience builder ───────────────────────────────────────


def create_default_pipeline() -> JLAIFPipeline:
    """Create a default pipeline with all standard modules."""
    from .pipeline_modules import (
        PIIRedactionModule,
        JurisdictionModule,
        CitationModule,
        TemporalModule,
        SeverityScoringModule,
        ReleaseGateModule,
    )

    pipeline = JLAIFPipeline("jlaif-default")
    pipeline.register_bulk(
        PIIRedactionModule(),
        JurisdictionModule(),
        CitationModule(),
        TemporalModule(),
        SeverityScoringModule(),
        ReleaseGateModule(),
    )
    return pipeline
