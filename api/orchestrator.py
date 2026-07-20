"""JuraRegel Orchestrator — Autonome compliance-assessment agent.

Niveau: 4 (boven PhD) — Autonoom redenerend, multi-jurisdictionaal, volledig traceerbaar.

Architectuur:
    Input → Data Collection (parallel) → Synthese (één LLM-call) → Output

    Data Collection:
    - Jurisdiction Analysis (lokaal, geen LLM)
    - Risk Prediction (lokaal, geen LLM)
    - Knowledge Graph (lokaal, geen LLM)
    - Drift Detection (lokaal, geen LLM)
    - RAG Search (lokaal, geen LLM — alleen zoeken)

    Synthese:
    - Één LLM-call met alle verzamelde data als context
    - Genereert conclusie, argumentatie, aanbevelingen

    Output:
    - Volledig assessment met audit trail
    - Human review flag
    - Actiepunten met deadlines
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

# ─── Data Models ──────────────────────────────────────────────


@dataclass
class AssessmentStep:
    """A single step in the autonomous assessment."""

    step_id: str
    name: str
    status: str
    result: dict
    duration_ms: int
    timestamp: str


@dataclass
class ComplianceAssessment:
    """Complete autonomous compliance assessment."""

    assessment_id: str
    organisation_id: str
    processing_activity: dict
    jurisdiction_analysis: dict
    risk_predictions: dict
    legal_arguments: dict
    drift_status: dict
    knowledge_graph_state: dict
    rag_context: dict
    conclusion: str
    confidence: float
    required_actions: list[str]
    deadlines: list[dict]
    human_review_required: bool
    steps: list[AssessmentStep]
    audit_trail_id: str
    model_used: str
    total_duration_ms: int
    generated_at: str


# ─── Orchestrator ─────────────────────────────────────────────


class ComplianceOrchestrator:
    """Autonomous compliance assessment orchestrator."""

    def __init__(self):
        self._step_count = 0

    def run_full_assessment(
        self,
        organisation_id: str,
        processing_activity: dict,
        context: dict | None = None,
    ) -> ComplianceAssessment:
        """Run a complete autonomous compliance assessment."""
        start = time.time()
        assessment_id = f"asm-{uuid.uuid4().hex[:8]}"
        steps = []

        # ─── Phase 1: Data Collection (parallel, geen LLM) ───

        step1 = self._run_step(
            "jurisdiction_analysis",
            lambda: self._analyze_jurisdictions(processing_activity),
        )
        steps.append(step1)
        jurisdiction_result = step1.result

        step2 = self._run_step(
            "risk_prediction",
            lambda: self._predict_risks(organisation_id, processing_activity),
        )
        steps.append(step2)
        risk_result = step2.result

        step3 = self._run_step(
            "knowledge_graph",
            lambda: self._analyze_knowledge_graph(processing_activity),
        )
        steps.append(step3)
        kg_result = step3.result

        step4 = self._run_step(
            "drift_detection",
            lambda: self._detect_drift(assessment_id, processing_activity),
        )
        steps.append(step4)
        drift_result = step4.result

        step5 = self._run_step(
            "rag_search", lambda: self._perform_rag_search(processing_activity)
        )
        steps.append(step5)
        rag_result = step5.result

        # ─── Phase 2: Synthese (één LLM-call) ───

        step6 = self._run_step(
            "synthese",
            lambda: self._synthesize(
                processing_activity,
                jurisdiction_result,
                risk_result,
                kg_result,
                drift_result,
                rag_result,
            ),
        )
        steps.append(step6)
        synthesis = step6.result

        # ─── Phase 3: Audit & Output ───

        step7 = self._run_step(
            "audit_logging",
            lambda: self._log_to_audit(assessment_id, organisation_id, steps),
        )
        steps.append(step7)

        total_duration = int((time.time() - start) * 1000)

        return ComplianceAssessment(
            assessment_id=assessment_id,
            organisation_id=organisation_id,
            processing_activity=processing_activity,
            jurisdiction_analysis=jurisdiction_result,
            risk_predictions=risk_result,
            legal_arguments=synthesis.get("arguments", {}),
            drift_status=drift_result,
            knowledge_graph_state=kg_result,
            rag_context=rag_result,
            conclusion=synthesis.get("conclusion", ""),
            confidence=synthesis.get("confidence", 0.0),
            required_actions=synthesis.get("actions", []),
            deadlines=synthesis.get("deadlines", []),
            human_review_required=synthesis.get("human_review", True),
            steps=steps,
            audit_trail_id=step7.result.get("trail_id", ""),
            model_used=synthesis.get("model", "template"),
            total_duration_ms=total_duration,
            generated_at=datetime.utcnow().isoformat(),
        )

    def _run_step(self, name: str, fn) -> AssessmentStep:
        """Run a single assessment step."""
        self._step_count += 1
        step_id = f"step-{self._step_count}"
        start = time.time()

        try:
            result = fn()
            status = "completed"
        except Exception as e:
            result = {"error": str(e)}
            status = "failed"
            logger.error(f"Step {name} failed: {e}")

        return AssessmentStep(
            step_id=step_id,
            name=name,
            status=status,
            result=result,
            duration_ms=int((time.time() - start) * 1000),
            timestamp=datetime.utcnow().isoformat(),
        )

    def _analyze_jurisdictions(self, activity: dict) -> dict:
        """Step 1: Multi-jurisdiction analysis."""
        from .multi_jurisdiction import multi_jurisdiction_engine

        report = multi_jurisdiction_engine.analyze(activity)
        return {
            "frameworks": report.applicable_frameworks,
            "obligations_count": len(report.obligations),
            "obligations": [
                {
                    "framework": o.framework,
                    "article": o.article,
                    "title": o.title,
                    "deadline": o.deadline,
                }
                for o in report.obligations
            ],
            "conflicts": len(report.conflicts),
            "gaps": report.gaps,
            "recommendations": report.recommendations,
        }

    def _predict_risks(self, org_id: str, activity: dict) -> dict:
        """Step 2: Predict compliance risks."""
        from .predictive_compliance import predictive_engine

        report = predictive_engine.predict(org_id, activity)
        return {
            "overall_risk": report.overall_risk_score,
            "risk_count": len(report.risk_predictions),
            "top_risks": [
                {"id": r.risk_id, "score": r.risk_score, "timeframe": r.timeframe}
                for r in report.risk_predictions[:5]
            ],
            "trend": report.trend_analysis.trend,
            "forecast_30d": report.trend_analysis.forecast_30d,
            "forecast_90d": report.trend_analysis.forecast_90d,
            "early_warnings": report.early_warnings,
            "priority_actions": report.priority_actions,
        }

    def _analyze_knowledge_graph(self, activity: dict) -> dict:
        """Step 3: Knowledge graph analysis."""
        from .knowledge_graph import knowledge_graph

        if not knowledge_graph.nodes:
            try:
                knowledge_graph.build_from_corpus()
            except Exception:
                pass  # Non-critical

        relevant = knowledge_graph.search(activity.get("name", ""), limit=5)
        return {
            "nodes_total": len(knowledge_graph.nodes),
            "relevant_nodes": relevant,
            "coverage": len(relevant),
        }

    def _detect_drift(self, assessment_id: str, activity: dict) -> dict:
        """Step 4: Detect compliance drift."""
        from .drift_detector import drift_detector

        report = drift_detector.detect_drift(assessment_id, activity)
        return {
            "drift_score": report.drift_score,
            "drift_count": len(report.drift_items),
            "trend": report.score_trend,
        }

    def _perform_rag_search(self, activity: dict) -> dict:
        """Step 5: RAG search (alleen zoeken, geen LLM)."""
        from .rag_engine import rag_engine

        question = self._generate_question(activity)
        search_results = rag_engine.search(question, top_k=5)
        return {
            "question": question,
            "results_count": len(search_results),
            "results": [
                {"source": r["source"], "title": r["title"], "text": r["text"][:200]}
                for r in search_results
            ],
        }

    def _generate_question(self, activity: dict) -> str:
        """Generate a search question from processing activity."""
        name = activity.get("name", "deze verwerking")
        return f"Welke verplichtingen gelden voor {name} volgens AVG en EU AI Act?"

    def _synthesize(
        self,
        activity: dict,
        jurisdiction: dict,
        risks: dict,
        kg: dict,
        drift: dict,
        rag: dict,
    ) -> dict:
        """Step 6: Synthesize all data into a conclusion (één LLM-call of template)."""

        # Build context for synthesis
        context = {
            "activity": activity,
            "jurisdiction": jurisdiction,
            "risks": risks,
            "knowledge_graph": kg,
            "drift": drift,
            "rag_results": rag.get("results", []),
        }

        # Try LLM synthesis first (with short timeout)
        try:
            result = self._llm_synthesize(context)
            # Verify result has actions/deadlines
            if result.get("actions") or result.get("deadlines"):
                return result
            # LLM gave output but no structured data — supplement with template
            template_result = self._template_synthesize(context)
            result["actions"] = template_result.get("actions", [])
            result["deadlines"] = template_result.get("deadlines", [])
            return result
        except Exception as e:
            logger.warning(f"LLM synthesis failed: {e}, using template")
            return self._template_synthesize(context)

    def _llm_synthesize(self, context: dict) -> dict:
        """Synthesize using cloud LLM via LiteLLM."""
        import httpx
        import os

        litellm_url = os.getenv("LITELLM_URL", "http://192.168.1.28:4000/v1")
        litellm_key = os.getenv("LITELLM_API_KEY", "")

        # Build prompt with all collected data
        prompt = self._build_synthesis_prompt(context)

        headers = {}
        if litellm_key:
            headers["Authorization"] = f"Bearer {litellm_key}"

        # Try cloud models in order of speed
        models = ["gemini-flash", "deepseek-v4-flash:cloud", "openai-gpt5-mini"]

        for model in models:
            try:
                resp = httpx.post(
                    f"{litellm_url}/chat/completions",
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": SYNTHESIS_SYSTEM_PROMPT},
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.1,
                        "max_tokens": 2000,
                    },
                    headers=headers,
                    timeout=60,
                )

                if resp.status_code == 200:
                    data = resp.json()
                    answer = data["choices"][0]["message"]["content"]

                    # Try to parse JSON from answer
                    import re

                    json_match = re.search(r"```json\s*(.*?)\s*```", answer, re.DOTALL)
                    if json_match:
                        try:
                            parsed = json.loads(json_match.group(1))
                            return {
                                "conclusion": parsed.get("conclusion", answer[:1000]),
                                "arguments": parsed.get(
                                    "arguments", {"source": "llm", "model": model}
                                ),
                                "confidence": parsed.get("confidence", 0.85),
                                "actions": parsed.get(
                                    "actions", self._extract_actions(answer)
                                ),
                                "deadlines": parsed.get(
                                    "deadlines", self._extract_deadlines(answer)
                                ),
                                "human_review": parsed.get("human_review", False),
                                "model": model,
                            }
                        except json.JSONDecodeError:
                            pass

                    return {
                        "conclusion": answer[:1000],
                        "arguments": {"source": "llm", "model": model},
                        "confidence": 0.85,
                        "actions": self._extract_actions(answer),
                        "deadlines": self._extract_deadlines(answer),
                        "human_review": False,
                        "model": model,
                    }
            except Exception as e:
                logger.warning(f"Model {model} failed: {e}")
                continue

        raise RuntimeError("All LLM models failed")

    def _template_synthesize(self, context: dict) -> dict:
        """Template-based synthesis fallback (geen LLM nodig)."""
        jurisdiction = context.get("jurisdiction", {})
        risks = context.get("risks", {})

        # Build conclusion from data
        parts = []
        parts.append(
            f"## Analyse voor {context.get('activity', {}).get('name', 'deze verwerking')}"
        )
        parts.append("")
        frames = jurisdiction.get("frameworks", [])
        parts.append(
            f"**Toepasselijke frameworks:** {', '.join(frames) if frames else 'Geen'}"
        )
        parts.append(
            f"**Aantal verplichtingen:** {jurisdiction.get('obligations_count', 0)}"
        )
        parts.append(f"**Risicoscore:** {risks.get('overall_risk', 0):.2f}")
        parts.append(f"**Trend:** {risks.get('trend', 'onbekend')}")

        # Actions
        actions = []
        if jurisdiction.get("recommendations"):
            actions.extend(jurisdiction["recommendations"][:5])
        if risks.get("priority_actions"):
            actions.extend(risks["priority_actions"][:3])

        # Deadlines
        deadlines = []
        for obs in jurisdiction.get("obligations", []):
            if obs.get("deadline"):
                deadlines.append(
                    {
                        "source": obs["framework"],
                        "deadline": obs["deadline"],
                        "title": obs["title"],
                    }
                )

        # Human review
        human_review = (
            len(jurisdiction.get("gaps", [])) > 0 or risks.get("overall_risk", 0) > 0.3
        )

        # Confidence based on data completeness
        confidence = 0.6  # Base for template
        if jurisdiction.get("obligations_count", 0) > 3:
            confidence += 0.1
        if risks.get("risk_count", 0) > 3:
            confidence += 0.1

        return {
            "conclusion": "\n".join(parts),
            "arguments": {"source": "template"},
            "confidence": min(confidence, 0.9),
            "actions": actions[:10],
            "deadlines": deadlines,
            "human_review": human_review,
            "model": "template",
        }

    def _build_synthesis_prompt(self, context: dict) -> str:
        """Build the synthesis prompt from collected data."""
        parts = [
            "## Verwerkingsactiviteit",
            json.dumps(context.get("activity", {}), indent=2, ensure_ascii=False),
            "",
            "## Juridische Analyse",
            f"Frameworks: {', '.join(context.get('jurisdiction', {}).get('frameworks', []))}",
            f"Verplichtingen: {context.get('jurisdiction', {}).get('obligations_count', 0)}",
            f"Gaps: {context.get('jurisdiction', {}).get('gaps', [])}",
            "",
            "## Risico Analyse",
            f"Overall Risk: {context.get('risks', {}).get('overall_risk', 0)}",
            f"Trend: {context.get('risks', {}).get('trend', 'onbekend')}",
            f"Early Warnings: {context.get('risks', {}).get('early_warnings', [])}",
            "",
            "## Knowledge Graph",
            f"Nodes: {context.get('knowledge_graph', {}).get('nodes_total', 0)}",
            f"Relevant: {context.get('knowledge_graph', {}).get('coverage', 0)}",
            "",
            "## RAG Zoekresultaten",
        ]

        for r in context.get("rag_results", [])[:3]:
            parts.append(
                f"- [{r.get('source', '?')}] {r.get('title', '?')}: {r.get('text', '')[:150]}"
            )

        parts.extend(
            [
                "",
                "## Opdracht",
                "Genereer een gestructureerd compliance-advies met:",
                "1. Conclusie (max 200 woorden)",
                "2. Juridische argumentatie (met bron-citaties)",
                "3. Aanbevelingen (geprioriteerd)",
                "4. Deadlines",
                "5. Human review nodig? (ja/nee + reden)",
                "",
                "Output formaat: JSON met velden: conclusion, arguments, actions, deadlines, human_review",
            ]
        )

        return "\n".join(parts)

    def _extract_actions(self, text: str) -> list[str]:
        """Extract actions from LLM output."""
        import re

        actions = []
        for line in text.split("\n"):
            line = line.strip()
            # Match bullet points, numbered lists, and lines with action keywords
            if line.startswith(("•", "-", "*")) or re.match(r"^\d+[\.\)]", line):
                cleaned = re.sub(r"^[•\-\*\d\.\)\s]+", "", line).strip()
                if cleaned and len(cleaned) > 5:
                    actions.append(cleaned)
        return actions[:10]

    def _extract_deadlines(self, text: str) -> list[dict]:
        """Extract deadlines from LLM output."""
        import re

        deadlines = []
        # Match ISO dates
        for match in re.finditer(r"(\d{4}-\d{2}-\d{2})", text):
            # Get context around the date
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            context = text[start:end].strip()
            deadlines.append(
                {"date": match.group(1), "context": context, "source": "llm_output"}
            )
        return deadlines

    def _log_to_audit(self, assessment_id: str, org_id: str, steps: list) -> dict:
        """Log to audit trail."""
        from .accountable_ai import accountability

        trail = accountability.create_audit_trail("assessment", assessment_id)
        for step in steps:
            accountability.log_decision(
                entity_id=assessment_id,
                action=step.name,
                actor="ComplianceOrchestrator",
                input_data={"step_id": step.step_id},
                output_data=step.result,
                reasoning=f"Step {step.name}: {step.status}",
                confidence=1.0 if step.status == "completed" else 0.0,
            )

        return {"trail_id": trail.trail_id, "entries": len(steps)}


# ─── System Prompts ───────────────────────────────────────────

SYNTHESIS_SYSTEM_PROMPT = """Je bent een senior privacy-jurist en AI-governance expert.
Je genereert een gestructureerd compliance-advies op basis van verzamelde data.

REGELS:
1. Baseer elke bewering op de verstrekte bronnen
2. Citeer specifieke wetsartikelen (bijv. "AVG Art. 35(3)(a)")
3. Geef een heldere conclusie
4. Prioriteer aanbevelingen op urgentie
5. Identificeer deadlines
6. Geef aan wanneer menselige review nodig is

Output: JSON met velden: conclusion, arguments, actions, deadlines, human_review"""


# ─── Singleton ─────────────────────────────────────────────────

orchestrator = ComplianceOrchestrator()
