"""Causaliteitsnetwerk — modelleert oorzaak-gevolg relaties tussen fouttypes.

Gebaseerd op:
- Structural Causal Models (Pearl, 2009)
- Bayesian Networks voor probabilistische inferentie
- Failure Mode and Effects Analysis (FMEA)

Elk fouttype heeft:
- Oorzaken (andere fouttypes die het kunnen veroorzaken)
- Gevolgen (andere fouttypes die het kan veroorzaken)
- Probabiliteit van cascading impact
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CausalEdge:
    """Een causale relatie tussen twee fouttypes."""

    cause: str
    effect: str
    probability: float  # P(effect | cause)
    description: str


@dataclass
class CausalNode:
    """Een fouttype met zijn causale relaties."""

    error_type: str
    causes: list[str] = field(default_factory=list)
    effects: list[str] = field(default_factory=list)
    base_probability: float = 0.1
    description: str = ""


CAUSAL_NETWORK: dict[str, CausalNode] = {
    "feitelijke_fout": CausalNode(
        error_type="feitelijke_fout",
        causes=["bronfout", "interpretatiefout"],
        effects=["procedurefout", "rechtsverlies"],
        base_probability=0.15,
        description="Onjuiste feiten leiden tot onjuiste conclusies",
    ),
    "bronfout": CausalNode(
        error_type="bronfout",
        causes=["omissiefout"],
        effects=["feitelijke_fout", "interpretatiefout"],
        base_probability=0.20,
        description="Ontbrekende of verkeerde bronnen veroorzaken interpretatiefouten",
    ),
    "interpretatiefout": CausalNode(
        error_type="interpretatiefout",
        causes=["bronfout", "feitelijke_fout", "bias_ongelijke_behandeling"],
        effects=["procedurefout", "omissiefout"],
        base_probability=0.18,
        description="Verkeerde interpretatie van correcte bronnen",
    ),
    "jurisdictiefout": CausalNode(
        error_type="jurisdictiefout",
        causes=["omissiefout"],
        effects=["procedurefout", "feitelijke_fout"],
        base_probability=0.08,
        description="Verkeerd rechtsgebied leidt tot verkeerde regels",
    ),
    "temporaliteitsfout": CausalNode(
        error_type="temporaliteitsfout",
        causes=["omissiefout"],
        effects=["feitelijke_fout", "bronfout"],
        base_probability=0.10,
        description="Verouderde informatie leidt tot onjuiste feiten",
    ),
    "procedurefout": CausalNode(
        error_type="procedurefout",
        causes=["feitelijke_fout", "interpretatiefout", "jurisdictiefout"],
        effects=["rechtsverlies"],
        base_probability=0.05,
        description="Procedurele fouten leiden tot rechtsverlies",
    ),
    "omissiefout": CausalNode(
        error_type="omissiefout",
        causes=["bias_ongelijke_behandeling"],
        effects=[
            "bronfout",
            "interpretatiefout",
            "jurisdictiefout",
            "temporaliteitsfout",
        ],
        base_probability=0.25,
        description="Gemiste informatie heeft cascading effect",
    ),
    "bias_ongelijke_behandeling": CausalNode(
        error_type="bias_ongelijke_behandeling",
        causes=[],
        effects=["interpretatiefout", "omissiefout"],
        base_probability=0.12,
        description="Systematische voorkeur beïnvloedt alle analyses",
    ),
    "vertrouwelijkheidsincident": CausalNode(
        error_type="vertrouwelijkheidsincident",
        causes=["procedurefout"],
        effects=["rechtsverlies"],
        base_probability=0.03,
        description="PII-lek leidt tot AVG-schending en rechtsverlies",
    ),
}

CAUSAL_EDGES = [
    CausalEdge("bronfout", "feitelijke_fout", 0.7, "Verkeerde bron → verkeerde feiten"),
    CausalEdge(
        "bronfout", "interpretatiefout", 0.5, "Verkeerde bron → verkeerde interpretatie"
    ),
    CausalEdge(
        "feitelijke_fout", "procedurefout", 0.6, "Verkeerde feiten → procedurele fout"
    ),
    CausalEdge(
        "interpretatiefout",
        "procedurefout",
        0.5,
        "Verkeerde interpretatie → procedurele fout",
    ),
    CausalEdge(
        "interpretatiefout",
        "omissiefout",
        0.3,
        "Verkeerde interpretatie → gemiste info",
    ),
    CausalEdge(
        "jurisdictiefout",
        "procedurefout",
        0.8,
        "Verkeerd rechtsgebied → procedurele fout",
    ),
    CausalEdge(
        "jurisdictiefout",
        "feitelijke_fout",
        0.6,
        "Verkeerd rechtsgebied → verkeerde feiten",
    ),
    CausalEdge(
        "temporaliteitsfout",
        "feitelijke_fout",
        0.5,
        "Verouderde info → verkeerde feiten",
    ),
    CausalEdge(
        "temporaliteitsfout", "bronfout", 0.4, "Verouderde info → verkeerde bron"
    ),
    CausalEdge("omissiefout", "bronfout", 0.6, "Gemiste info → ontbrekende bron"),
    CausalEdge(
        "omissiefout",
        "interpretatiefout",
        0.4,
        "Gemiste info → verkeerde interpretatie",
    ),
    CausalEdge(
        "omissiefout", "jurisdictiefout", 0.3, "Gemiste info → verkeerd rechtsgebied"
    ),
    CausalEdge(
        "omissiefout", "temporaliteitsfout", 0.2, "Gemiste info → verouderde info"
    ),
    CausalEdge(
        "bias_ongelijke_behandeling",
        "interpretatiefout",
        0.7,
        "Bias → verkeerde interpretatie",
    ),
    CausalEdge("bias_ongelijke_behandeling", "omissiefout", 0.5, "Bias → gemiste info"),
    CausalEdge(
        "procedurefout", "vertrouwelijkheidsincident", 0.2, "Procedurefout → PII-lek"
    ),
]


class CausalityNetwork:
    """Causaal netwerk voor fouttype-analyse."""

    def __init__(self):
        self._nodes = CAUSAL_NETWORK
        self._edges = CAUSAL_EDGES

    def get_root_causes(self, error_type: str) -> list[str]:
        """Vind root causes (fouttypes zonder oorzaken die het kunnen veroorzaken)."""
        visited = set()
        roots = []
        self._trace_up(error_type, visited, roots)
        return roots

    def _trace_up(self, error_type: str, visited: set, roots: list) -> None:
        if error_type in visited:
            return
        visited.add(error_type)

        node = self._nodes.get(error_type)
        if not node:
            return

        if not node.causes:
            roots.append(error_type)
        else:
            for cause in node.causes:
                self._trace_up(cause, visited, roots)

    def get_cascade_effects(self, error_type: str) -> list[str]:
        """Vind alle mogelijke gevolgen van een fouttype (cascading)."""
        visited = set()
        effects = []
        self._trace_down(error_type, visited, effects)
        return effects

    def _trace_down(self, error_type: str, visited: set, effects: list) -> None:
        if error_type in visited:
            return
        visited.add(error_type)

        node = self._nodes.get(error_type)
        if not node:
            return

        for effect in node.effects:
            effects.append(effect)
            self._trace_down(effect, visited, effects)

    def compute_cascade_probability(self, cause: str, effect: str) -> float:
        """Bereken de probabiliteit dat een fouttype een ander veroorzaakt."""
        for edge in self._edges:
            if edge.cause == cause and edge.effect == effect:
                return edge.probability
        return 0.0

    def find_critical_path(self, start: str, end: str) -> list[dict[str, Any]]:
        """Vind het meest waarschijnlijke causale pad tussen twee fouttypes."""
        paths = []
        self._find_paths(start, end, [], 1.0, paths)

        if not paths:
            return []

        # Sort by probability (highest first)
        paths.sort(key=lambda p: p["probability"], reverse=True)
        return paths[:3]

    def _find_paths(
        self,
        current: str,
        target: str,
        path: list[str],
        prob: float,
        results: list[dict],
    ) -> None:
        path = path + [current]

        if current == target and len(path) > 1:
            results.append({"path": path, "probability": round(prob, 4)})
            return

        node = self._nodes.get(current)
        if not node:
            return

        for effect in node.effects:
            if effect not in path:  # Prevent cycles
                edge_prob = self.compute_cascade_probability(current, effect)
                self._find_paths(effect, target, path, prob * edge_prob, results)

    def get_risk_ranking(self) -> list[dict[str, Any]]:
        """Rangschik fouttypes op basis van hun cascading impact."""
        rankings = []

        for error_type, node in self._nodes.items():
            cascade = self.get_cascade_effects(error_type)
            risk_score = len(cascade) * node.base_probability

            rankings.append(
                {
                    "error_type": error_type,
                    "cascade_size": len(cascade),
                    "base_probability": node.base_probability,
                    "risk_score": round(risk_score, 3),
                    "cascade_effects": cascade,
                }
            )

        rankings.sort(key=lambda r: r["risk_score"], reverse=True)
        return rankings

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": len(self._nodes),
            "edges": len(self._edges),
            "root_causes": [n for n, node in self._nodes.items() if not node.causes],
            "risk_ranking": self.get_risk_ranking(),
        }


# ─── Singleton ─────────────────────────────────────────────────

causality_network = CausalityNetwork()
