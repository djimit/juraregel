"""Compliance Digital Twin — Digitale kopie van je compliance-postuur.

Creëert een real-time digitale representatie van:
- Verwerkingsactiviteiten
- Risico's en maatregelen
- Compliance-scores per domein
- Voorspellende scenario's
- "Wat als?" analyses

Academische foundation:
- Digital Twin Technology (Grieves, 2014)
- Compliance Monitoring (Bamberger & Mulligan, 2015)
- Predictive Governance (Kitchin, 2017)
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)

# ─── Data Models ──────────────────────────────────────────────


@dataclass
class TwinNode:
    """A node in the digital twin."""

    node_id: str
    node_type: str  # processing, risk, measure, framework, assessment
    name: str
    status: str  # compliant, non_compliant, at_risk, unknown
    score: float  # 0-100
    metadata: dict[str, Any]


@dataclass
class TwinEdge:
    """An edge in the digital twin."""

    source: str
    target: str
    relation: str  # has_risk, mitigated_by, requires, implements
    weight: float  # 0-1


@dataclass
class Scenario:
    """A "what-if" scenario."""

    scenario_id: str
    description: str
    changes: dict[str, Any]
    predicted_impact: dict[str, float]  # framework → score_delta
    predicted_risks: list[str]
    recommended_actions: list[str]


@dataclass
class DigitalTwinReport:
    """Complete digital twin report."""

    organisation_id: str
    generated_at: str
    nodes: list[TwinNode]
    edges: list[TwinEdge]
    overall_score: float
    framework_scores: dict[str, float]
    scenarios: list[Scenario]
    alerts: list[str]


# ─── Digital Twin Engine ──────────────────────────────────────


class DigitalTwinEngine:
    """Create and maintain a compliance digital twin."""

    def create_twin(self, organisation_id: str, state: dict) -> DigitalTwinReport:
        """Create a digital twin from current state."""
        start = time.time()

        # 1. Create nodes
        nodes = self._create_nodes(state)

        # 2. Create edges
        edges = self._create_edges(nodes)

        # 3. Calculate scores
        framework_scores = self._calculate_framework_scores(nodes)
        overall_score = sum(framework_scores.values()) / max(len(framework_scores), 1)

        # 4. Generate scenarios
        scenarios = self._generate_scenarios(state, framework_scores)

        # 5. Generate alerts
        alerts = self._generate_alerts(nodes, framework_scores)

        return DigitalTwinReport(
            organisation_id=organisation_id,
            generated_at=datetime.utcnow().isoformat(),
            nodes=nodes,
            edges=edges,
            overall_score=round(overall_score, 1),
            framework_scores=framework_scores,
            scenarios=scenarios,
            alerts=alerts,
        )

    def _create_nodes(self, state: dict) -> list[TwinNode]:
        """Create twin nodes from state."""
        nodes = []

        # Processing activity nodes
        for i, pa in enumerate(state.get("processing_activities", [])):
            nodes.append(
                TwinNode(
                    node_id=f"pa-{i}",
                    node_type="processing",
                    name=pa.get("name", f"Verwerking {i + 1}"),
                    status=pa.get("status", "unknown"),
                    score=pa.get("compliance_score", 50),
                    metadata=pa,
                )
            )

        # Risk nodes
        risk_factors = {
            "datalek": {"base": 0.15, "framework": "AVG"},
            "discriminatie": {"base": 0.10, "framework": "AVG"},
            "non_conformiteit_ai": {"base": 0.20, "framework": "AI Act"},
            "dpia_vergeten": {"base": 0.25, "framework": "AVG"},
        }
        for risk_id, info in risk_factors.items():
            nodes.append(
                TwinNode(
                    node_id=f"risk-{risk_id}",
                    node_type="risk",
                    name=risk_id.replace("_", " ").title(),
                    status="at_risk" if info["base"] > 0.15 else "monitored",
                    score=max(0, 100 - int(info["base"] * 100)),
                    metadata={
                        "framework": info["framework"],
                        "probability": info["base"],
                    },
                )
            )

        # Framework nodes
        frameworks = ["AVG", "AI Act", "NIS2", "ISO 27001"]
        for fw in frameworks:
            nodes.append(
                TwinNode(
                    node_id=f"fw-{fw.lower().replace(' ', '-')}",
                    node_type="framework",
                    name=fw,
                    status="active",
                    score=state.get(f"{fw.lower()}_score", 60),
                    metadata={},
                )
            )

        return nodes

    def _create_edges(self, nodes: list[TwinNode]) -> list[TwinEdge]:
        """Create edges between nodes."""
        edges = []

        # Link processing activities to risks
        pa_nodes = [n for n in nodes if n.node_type == "processing"]
        risk_nodes = [n for n in nodes if n.node_type == "risk"]

        for pa in pa_nodes:
            for risk in risk_nodes:
                edges.append(
                    TwinEdge(
                        source=pa.node_id,
                        target=risk.node_id,
                        relation="has_risk",
                        weight=0.5,
                    )
                )

        # Link frameworks to processing activities
        fw_nodes = [n for n in nodes if n.node_type == "framework"]
        for fw in fw_nodes:
            for pa in pa_nodes:
                edges.append(
                    TwinEdge(
                        source=fw.node_id,
                        target=pa.node_id,
                        relation="governs",
                        weight=0.8,
                    )
                )

        return edges

    def _calculate_framework_scores(self, nodes: list[TwinNode]) -> dict[str, float]:
        """Calculate scores per framework."""
        scores = {}
        fw_nodes = [n for n in nodes if n.node_type == "framework"]

        for fw in fw_nodes:
            scores[fw.name] = fw.score

        return scores

    def _generate_scenarios(
        self, state: dict, current_scores: dict[str, float]
    ) -> list[Scenario]:
        """Generate "what-if" scenarios."""
        scenarios = []

        # Scenario 1: Implement encryption
        scenarios.append(
            Scenario(
                scenario_id="scen-encryptie",
                description="Implementeer end-to-end encryptie voor alle verwerkingen",
                changes={"security_measures": ["encryptie", "toegangscontrole"]},
                predicted_impact={"AVG": +15, "NIS2": +20, "ISO 27001": +10},
                predicted_risks=["Verlaagd datalek-risico met 60%"],
                recommended_actions=["Implementeer AES-256", "Configureer TLS 1.3"],
            )
        )

        # Scenario 2: Conduct DPIA
        if current_scores.get("AVG", 0) < 80:
            scenarios.append(
                Scenario(
                    scenario_id="scen-dpia",
                    description="Voer DPIA uit voor alle hoog-risico verwerkingen",
                    changes={"dpia_conducted": True},
                    predicted_impact={"AVG": +20, "AI Act": +10},
                    predicted_risks=["Identificatie van onbekende risico's"],
                    recommended_actions=[
                        "Plan DPIA-sessie",
                        "Identificeer stakeholders",
                    ],
                )
            )

        # Scenario 3: Human Oversight
        if state.get("ai_systems"):
            scenarios.append(
                Scenario(
                    scenario_id="scen-oversight",
                    description="Implementeer human-in-the-loop voor alle AI-besluiten",
                    changes={"human_oversight": True},
                    predicted_impact={"AI Act": +25, "AVG": +5},
                    predicted_risks=["Verlaagd discriminatie-risico"],
                    recommended_actions=[
                        "Definieer oversight-procedure",
                        "Train medewerkers",
                    ],
                )
            )

        return scenarios

    def _generate_alerts(
        self, nodes: list[TwinNode], scores: dict[str, float]
    ) -> list[str]:
        """Generate alerts."""
        alerts = []

        # Low framework scores
        for fw, score in scores.items():
            if score < 50:
                alerts.append(f"CRITICAL: {fw} score is kritiek laag ({score}/100)")
            elif score < 70:
                alerts.append(f"WARNING: {fw} score is onder de norm ({score}/100)")

        # At-risk nodes
        at_risk = [n for n in nodes if n.status == "at_risk"]
        for node in at_risk:
            alerts.append(f"RISICO: {node.name} vereist aandacht")

        return alerts


# ─── Singleton ─────────────────────────────────────────────────

digital_twin_engine = DigitalTwinEngine()
