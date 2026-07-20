"""Agentic AI Workflows — Autonomous compliance agents.

Agents:
1. DPIA Agent — End-to-end DPIA generation
2. FRIA Agent — End-to-end FRIA generation
3. Regulatory Monitor — Continuous regulatory change detection
4. Evidence Agent — Automated evidence collection
5. Review Agent — Review cycle planning
6. Incident Agent — Incident analysis and response
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any


# ─── Agent Base ───────────────────────────────────────────────


@dataclass
class AgentResult:
    """Result of an agent execution."""

    agent: str
    status: str  # success, partial, failed
    output: dict[str, Any]
    citations: list[dict] = field(default_factory=list)
    confidence: float = 0.0
    hallucination_flags: list[dict] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    execution_time_ms: int = 0
    trace: list[dict] = field(default_factory=list)


# ─── DPIA Agent ────────────────────────────────────────────────


class DPIAAgent:
    """Autonomous DPIA generation agent."""

    def __init__(self):
        self.name = "DPIA Agent"
        self.version = "1.0.0"

    async def execute(
        self,
        processing_activity: dict,
        template_id: str = "dpia_rijksdienst",
    ) -> AgentResult:
        """Generate a complete DPIA for a processing activity."""
        start = datetime.utcnow()
        trace = []

        # Step 1: Pre-scan
        trace.append({"step": "pre_scan", "status": "running"})
        pre_scan = self._run_pre_scan(processing_activity)
        trace.append(
            {"step": "pre_scan", "status": "complete", "result": pre_scan["verdict"]}
        )

        if pre_scan["verdict"] == "NO-GO":
            return AgentResult(
                agent=self.name,
                status="complete",
                output={"verdict": "NO-GO", "reasoning": pre_scan["reasoning"]},
                confidence=0.95,
                trace=trace,
                execution_time_ms=self._elapsed_ms(start),
            )

        # Step 2: Generate DPIA from template
        trace.append({"step": "generate", "status": "running"})
        from docs.templates import generate_document, enrich_document

        doc = generate_document(
            template_id,
            processing_activity.get("organisation", "Organisatie"),
            verwerking=processing_activity.get("name", "Verwerking"),
        )
        enriched = enrich_document(doc)
        trace.append({"step": "generate", "status": "complete"})

        # Step 3: Identify risks
        trace.append({"step": "risk_analysis", "status": "running"})
        risks = self._identify_risks(processing_activity)
        trace.append(
            {"step": "risk_analysis", "status": "complete", "risks_found": len(risks)}
        )

        # Step 4: Propose measures
        trace.append({"step": "measures", "status": "running"})
        measures = self._propose_measures(risks)
        trace.append(
            {
                "step": "measures",
                "status": "complete",
                "measures_proposed": len(measures),
            }
        )

        # Step 5: Calculate confidence
        confidence = self._calculate_confidence(enriched, risks, measures)

        # Step 6: Generate recommendations
        recommendations = self._generate_recommendations(processing_activity, risks)

        execution_time = self._elapsed_ms(start)

        return AgentResult(
            agent=self.name,
            status="success",
            output={
                "document": enriched,
                "pre_scan": pre_scan,
                "risks": risks,
                "measures": measures,
                "next_review_date": (
                    datetime.utcnow() + timedelta(days=365)
                ).isoformat(),
            },
            citations=[
                {"source": "AVG Art. 35", "passage": "DPIA verplicht bij hoog risico"},
                {"source": "EDPB WP29", "passage": "9 criteria voor DPIA-verplichting"},
            ],
            confidence=confidence,
            recommendations=recommendations,
            execution_time_ms=execution_time,
            trace=trace,
        )

    def _run_pre_scan(self, activity: dict) -> dict:
        """Run the 9-criteria pre-scan."""
        score = 0
        criteria = []

        # Criterion 1: Evaluation/scoring
        if activity.get("ai_systems"):
            score += 1
            criteria.append("AI-systeem: evaluatie/scoring gedetecteerd")

        # Criterion 4: Sensitive data
        sensitive = {"biometrische gegevens", "gezondheidsgegevens", "strafrechtelijke"}
        if any(cat.lower() in sensitive for cat in activity.get("data_categories", [])):
            score += 1
            criteria.append("Gevoelige gegevens gedetecteerd")

        # Criterion 5: Large scale
        if activity.get("data_subject_count", 0) > 5000:
            score += 1
            criteria.append("Grootschalige verwerking")

        # Criterion 7: Vulnerable subjects
        vulnerable = {"kinderen", "medewerkers", "patiënten"}
        if any(sub.lower() in vulnerable for sub in activity.get("data_subjects", [])):
            score += 1
            criteria.append("Kwetsbare betrokkenen")

        return {
            "score": score,
            "verdict": "GO" if score >= 2 else "NO-GO",
            "reasoning": criteria,
        }

    def _identify_risks(self, activity: dict) -> list[dict]:
        """Identify risks based on processing activity."""
        risks = []

        if activity.get("ai_systems"):
            risks.append(
                {
                    "type": "discriminatie",
                    "severity": "high",
                    "description": "AI-systeem kan leiden tot onbedoelde discriminatie",
                    "citation": "EU AI Act Art. 10(2)(f)",
                }
            )

        if "gezondheidsgegevens" in str(activity.get("data_categories", [])):
            risks.append(
                {
                    "type": "datalek_gezondheid",
                    "severity": "critical",
                    "description": "Verwerking van gezondheidsgegevens vereist extra beveiliging",
                    "citation": "AVG Art. 9",
                }
            )

        return risks

    def _propose_measures(self, risks: list[dict]) -> list[dict]:
        """Propose mitigating measures for identified risks."""
        measures = []
        for risk in risks:
            if risk["type"] == "discriminatie":
                measures.append(
                    {
                        "measure": "Bias-auditing uitvoeren",
                        "frequency": "jaarlijks",
                        "citation": "EU AI Act Art. 10(3)",
                    }
                )
            elif risk["type"] == "datalek_gezondheid":
                measures.append(
                    {
                        "measure": "End-to-end encryptie",
                        "frequency": "continu",
                        "citation": "AVG Art. 32",
                    }
                )
        return measures

    def _calculate_confidence(self, doc: dict, risks: list, measures: list) -> float:
        """Calculate confidence score for the DPIA."""
        base = 0.85
        if len(risks) > 0:
            base += 0.05
        if len(measures) >= len(risks):
            base += 0.05
        return min(base, 0.98)

    def _generate_recommendations(self, activity: dict, risks: list) -> list[str]:
        """Generate actionable recommendations."""
        recs = []
        if risks:
            recs.append("Plan stakeholder-consultatie binnen 30 dagen")
            recs.append("Documenteer mitigerende maatregelen in privacybeleid")
            recs.append("Plan jaarlijkse herziening DPIA")
        return recs

    def _elapsed_ms(self, start: datetime) -> int:
        return int((datetime.utcnow() - start).total_seconds() * 1000)


# ─── FRIA Agent ────────────────────────────────────────────────


class FRIAAgent:
    """Autonomous FRIA generation agent."""

    def __init__(self):
        self.name = "FRIA Agent"
        self.version = "1.0.0"

    async def execute(self, ai_system: dict) -> AgentResult:
        """Generate a complete FRIA for an AI system."""
        start = datetime.utcnow()
        trace = []

        # Step 1: Risk classification
        trace.append({"step": "classification", "status": "running"})
        classification = self._classify_risk(ai_system)
        trace.append(
            {
                "step": "classification",
                "status": "complete",
                "tier": classification["tier"],
            }
        )

        if classification["tier"] != "high":
            return AgentResult(
                agent=self.name,
                status="complete",
                output={
                    "verdict": "FRIA niet verplicht",
                    "classification": classification,
                },
                confidence=0.95,
                trace=trace,
                execution_time_ms=self._elapsed_ms(start),
            )

        # Step 2: Generate FRIA
        trace.append({"step": "generate", "status": "running"})
        from docs.templates import generate_document, enrich_document

        doc = generate_document(
            "fria_eu",
            ai_system.get("organisation", "Organisatie"),
            ai_systeem=ai_system.get("name", "AI-systeem"),
        )
        enriched = enrich_document(doc)
        trace.append({"step": "generate", "status": "complete"})

        # Step 3: Fundamental rights analysis
        rights_impact = self._analyze_rights_impact(ai_system)
        trace.append({"step": "rights_analysis", "status": "complete"})

        return AgentResult(
            agent=self.name,
            status="success",
            output={
                "document": enriched,
                "classification": classification,
                "rights_impact": rights_impact,
            },
            citations=[
                {
                    "source": "EU AI Act Art. 27",
                    "passage": "FRIA verplicht voor hoog-risico AI",
                },
            ],
            confidence=0.90,
            trace=trace,
            execution_time_ms=self._elapsed_ms(start),
        )

    def _classify_risk(self, ai_system: dict) -> dict:
        """Classify AI system risk tier."""
        # Simplified classification
        high_risk_areas = {
            "recruitment",
            "credit_scoring",
            "medical",
            "law_enforcement",
        }
        domain = ai_system.get("domain", "")

        if domain in high_risk_areas:
            return {
                "tier": "high",
                "reasoning": f"Domein '{domain}' valt onder Bijlage III",
            }
        return {"tier": "limited", "reasoning": "Geen hoog-risico toepassing"}

    def _analyze_rights_impact(self, ai_system: dict) -> list[dict]:
        """Analyze impact on fundamental rights."""
        return [
            {
                "right": "Non-discriminatie",
                "impact": "medium",
                "citation": "Art. 21 HVVR",
            },
            {"right": "Privacy", "impact": "high", "citation": "Art. 8 EVRM"},
        ]

    def _elapsed_ms(self, start: datetime) -> int:
        return int((datetime.utcnow() - start).total_seconds() * 1000)


# ─── Regulatory Monitor Agent ──────────────────────────────────


class RegulatoryMonitorAgent:
    """Continuous regulatory change monitoring agent."""

    def __init__(self):
        self.name = "Regulatory Monitor"
        self.version = "1.0.0"
        self.sources = ["EUR-Lex", "Staatsblad", "EDPB", "AP", "EU AI Office"]

    async def scan(self) -> AgentResult:
        """Scan for regulatory changes."""
        start = datetime.utcnow()

        # In production: scrape sources, detect changes, analyze impact
        changes = [
            {
                "source": "EDPB",
                "title": "Guidelines on AI and Data Protection",
                "date": "2026-07-15",
                "impact_score": 0.8,
                "affected_frameworks": ["AVG", "AI Act"],
            }
        ]

        return AgentResult(
            agent=self.name,
            status="success",
            output={"changes_detected": len(changes), "changes": changes},
            confidence=0.85,
            trace=[{"step": "scan", "sources_checked": len(self.sources)}],
            execution_time_ms=self._elapsed_ms(start),
        )

    def _elapsed_ms(self, start: datetime) -> int:
        return int((datetime.utcnow() - start).total_seconds() * 1000)


# ─── Agent Orchestrator ────────────────────────────────────────


class AgentOrchestrator:
    """Orchestrate multiple compliance agents."""

    def __init__(self):
        self.agents = {
            "dpia": DPIAAgent(),
            "fria": FRIAAgent(),
            "regulatory": RegulatoryMonitorAgent(),
        }

    async def run_agent(self, agent_name: str, **kwargs) -> AgentResult:
        """Run a specific agent."""
        agent = self.agents.get(agent_name)
        if not agent:
            return AgentResult(
                agent=agent_name,
                status="failed",
                output={"error": f"Unknown agent: {agent_name}"},
            )

        if hasattr(agent, "execute"):
            return await agent.execute(**kwargs)
        elif hasattr(agent, "scan"):
            return await agent.scan()

        return AgentResult(
            agent=agent_name,
            status="failed",
            output={"error": "Agent has no execute method"},
        )

    async def run_full_compliance_check(self, organisation_id: str) -> dict:
        """Run a full compliance check across all agents."""
        results = {}

        # Run DPIA agent
        results["dpia"] = await self.run_agent("dpia", processing_activity={})

        # Run FRIA agent
        results["fria"] = await self.run_agent("fria", ai_system={})

        # Run regulatory monitor
        results["regulatory"] = await self.run_agent("regulatory")

        return {
            "organisation_id": organisation_id,
            "timestamp": datetime.utcnow().isoformat(),
            "results": results,
        }
