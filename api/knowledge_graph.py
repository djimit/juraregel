"""Knowledge Graph — Legal concept relationship mapping.

Models relationships between:
- Laws and articles
- Guidelines and interpretations
- Templates and criteria
- Risks and measures
- Processing activities and impacts

Uses in-memory graph (Neo4j/pg_graph ready for production).
"""

from __future__ import annotations

import json
import logging
import os
import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

# ─── Data Models ──────────────────────────────────────────────


@dataclass
class KGNode:
    """Knowledge graph node."""

    id: str
    label: str  # Wet, Artikel, Richtlijn, Template, Criterion, Risico, Maatregel
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class KGEdge:
    """Knowledge graph edge."""

    source: str
    target: str
    relation: (
        str  # has_article, references, requires, contradicts, supersedes, implements
    )
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class ImpactQueryResult:
    """Result of an impact query."""

    change_node: str
    affected_nodes: list[dict]
    affected_count: int
    max_depth: int
    paths: list[list[str]]


# ─── Knowledge Graph ──────────────────────────────────────────


class KnowledgeGraph:
    """In-memory knowledge graph for legal reasoning."""

    def __init__(self):
        self.nodes: dict[str, KGNode] = {}
        self.edges: list[KGEdge] = []
        self._adjacency: dict[str, list[tuple[str, str]]] = defaultdict(
            list
        )  # node -> [(target, relation)]
        self._reverse_adj: dict[str, list[tuple[str, str]]] = defaultdict(list)

    def add_node(
        self, node_id: str, label: str, properties: dict | None = None
    ) -> KGNode:
        """Add a node."""
        node = KGNode(id=node_id, label=label, properties=properties or {})
        self.nodes[node_id] = node
        return node

    def add_edge(
        self, source: str, target: str, relation: str, properties: dict | None = None
    ) -> KGEdge:
        """Add an edge."""
        edge = KGEdge(
            source=source, target=target, relation=relation, properties=properties or {}
        )
        self.edges.append(edge)
        self._adjacency[source].append((target, relation))
        self._reverse_adj[target].append((source, relation))
        return edge

    def get_node(self, node_id: str) -> KGNode | None:
        """Get node by ID."""
        return self.nodes.get(node_id)

    def get_neighbors(self, node_id: str, relation: str | None = None) -> list[KGNode]:
        """Get neighboring nodes."""
        neighbors = []
        for target, rel in self._adjacency.get(node_id, []):
            if relation is None or rel == relation:
                if target in self.nodes:
                    neighbors.append(self.nodes[target])
        return neighbors

    def get_predecessors(
        self, node_id: str, relation: str | None = None
    ) -> list[KGNode]:
        """Get predecessor nodes."""
        predecessors = []
        for source, rel in self._reverse_adj.get(node_id, []):
            if relation is None or rel == relation:
                if source in self.nodes:
                    predecessors.append(self.nodes[source])
        return predecessors

    def impact_query(self, node_id: str, max_depth: int = 3) -> ImpactQueryResult:
        """Find all nodes affected by a change to the given node (BFS)."""
        visited = set()
        queue = [(node_id, 0, [node_id])]
        affected = []
        paths = []

        while queue:
            current, depth, path = queue.pop(0)
            if current in visited or depth > max_depth:
                continue
            visited.add(current)

            if depth > 0 and current in self.nodes:
                affected.append(
                    {
                        "id": current,
                        "label": self.nodes[current].label,
                        "depth": depth,
                        "path": path,
                    }
                )
                paths.append(path)

            for target, rel in self._adjacency.get(current, []):
                if target not in visited:
                    queue.append((target, depth + 1, path + [target]))

        return ImpactQueryResult(
            change_node=node_id,
            affected_nodes=affected,
            affected_count=len(affected),
            max_depth=max_depth,
            paths=paths,
        )

    def find_path(
        self, source: str, target: str, max_depth: int = 4
    ) -> list[str] | None:
        """Find path between two nodes (BFS)."""
        visited = {source}
        queue = [(source, [source])]

        while queue:
            current, path = queue.pop(0)
            if len(path) > max_depth:
                continue

            for next_node, _ in self._adjacency.get(current, []):
                if next_node == target:
                    return path + [next_node]
                if next_node not in visited:
                    visited.add(next_node)
                    queue.append((next_node, path + [next_node]))

        return None

    def build_from_corpus(self) -> dict:
        """Build the knowledge graph from the legal corpus."""
        from .corpus_loader import AVG_ARTICLES, EU_AI_ACT_ARTICLES, EDPB_GUIDELINES

        # Add law nodes
        self.add_node(
            "avg",
            "Wet",
            {"title": "Algemene Verordening Gegevensbescherming", "jurisdiction": "EU"},
        )
        self.add_node("ai-act", "Wet", {"title": "EU AI Act", "jurisdiction": "EU"})
        self.add_node(
            "edpb", "Richtlijn", {"title": "EDPB Guidelines", "jurisdiction": "EU"}
        )

        # Add AVG articles
        for art_id, data in AVG_ARTICLES.items():
            node_id = f"avg-{art_id}"
            self.add_node(
                node_id,
                "Artikel",
                {
                    "title": data["title"],
                    "wet": "AVG",
                    "content": data["content"][:200],
                },
            )
            self.add_edge("avg", node_id, "has_article")

            # Extract criteria from content
            if "DPIA" in data["content"] or "beoordeling" in data["content"].lower():
                crit_id = f"crit-{art_id}-dpia"
                self.add_node(
                    crit_id,
                    "Criterion",
                    {"name": "DPIA-verplichting", "source": node_id},
                )
                self.add_edge(node_id, crit_id, "has_criterion")

        # Add AI Act articles
        for art_id, data in EU_AI_ACT_ARTICLES.items():
            node_id = f"ai-act-{art_id}"
            self.add_node(
                node_id,
                "Artikel",
                {
                    "title": data["title"],
                    "wet": "AI Act",
                    "content": data["content"][:200],
                },
            )
            self.add_edge("ai-act", node_id, "has_article")

            # FRIA connection
            if "27" in art_id:
                self.add_node(
                    "fria-template", "Template", {"name": "FRIA", "type": "assessment"}
                )
                self.add_edge(node_id, "fria-template", "requires")

        # Add EDPB guidelines
        for guide_id, data in EDPB_GUIDELINES.items():
            node_id = f"edpb-{guide_id}"
            self.add_node(
                node_id,
                "Richtlijn",
                {
                    "title": data["title"],
                    "source": "EDPB",
                },
            )
            self.add_edge("edpb", node_id, "has_guideline")

            # Link to AVG
            if "dpia" in guide_id:
                self.add_edge(node_id, "avg-art35", "references")
            if "design" in guide_id:
                self.add_edge(node_id, "avg-art25", "references")

        # Add template nodes
        templates = [
            ("dpia-template", "DPIA", "assessment"),
            ("fria-template", "FRIA", "assessment"),
            ("lia-template", "LIA", "assessment"),
            ("tia-template", "TIA", "assessment"),
            ("bias-audit-template", "Bias Audit", "assessment"),
        ]
        for tid, name, ttype in templates:
            self.add_node(tid, "Template", {"name": name, "type": ttype})

        # Link templates to criteria
        self.add_edge("dpia-template", "crit-art35-dpia", "evaluates")
        self.add_edge("fria-template", "ai-act-art27", "evaluates")

        # Add risk nodes
        risks = [
            ("risk-discriminatie", "Discriminatie", "high"),
            ("risk-datalek", "Datalek", "critical"),
            ("risk-bias", "AI Bias", "high"),
            ("risk-privacy", "Privacy-inbreuk", "high"),
            ("risk-transparantie", "Gebrek aan transparantie", "medium"),
        ]
        for rid, name, severity in risks:
            self.add_node(rid, "Risico", {"name": name, "severity": severity})

        # Add measure nodes
        measures = [
            ("measure-encryptie", "Encryptie", "technical"),
            ("measure-pseudonimisering", "Pseudonimisering", "technical"),
            ("measure-toegangscontrole", "Toegangscontrole", "technical"),
            ("measure-bias-audit", "Bias Auditing", "organizational"),
            ("measure-human-oversight", "Menselijke Oversight", "organizational"),
            ("measure-dpia", "DPIA uitvoeren", "organizational"),
        ]
        for mid, name, mtype in measures:
            self.add_node(mid, "Maatregel", {"name": name, "type": mtype})

        # Link risks to measures
        self.add_edge("risk-discriminatie", "measure-bias-audit", "mitigated_by")
        self.add_edge("risk-datalek", "measure-encryptie", "mitigated_by")
        self.add_edge("risk-datalek", "measure-toegangscontrole", "mitigated_by")
        self.add - edge("risk-bias", "measure-bias-audit", "mitigated_by")
        self.add_edge("risk-privacy", "measure-pseudonimisering", "mitigated_by")

        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
            "labels": list(set(n.label for n in self.nodes.values())),
        }

    def get_stats(self) -> dict:
        """Get graph statistics."""
        labels = defaultdict(int)
        for node in self.nodes.values():
            labels[node.label] += 1

        relations = defaultdict(int)
        for edge in self.edges:
            relations[edge.relation] += 1

        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "labels": dict(labels),
            "relations": dict(relations),
        }

    def search(self, query: str, limit: int = 10) -> list[dict]:
        """Search nodes by title/name."""
        query_lower = query.lower()
        results = []
        for node in self.nodes.values():
            title = node.properties.get("title", "") or node.properties.get("name", "")
            if query_lower in title.lower() or query_lower in node.id.lower():
                results.append(
                    {
                        "id": node.id,
                        "label": node.label,
                        "title": title,
                    }
                )
            if len(results) >= limit:
                break
        return results


# ─── Singleton ─────────────────────────────────────────────────

knowledge_graph = KnowledgeGraph()
