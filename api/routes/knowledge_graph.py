"""Knowledge Graph API — Legal concept relationship mapping."""

from fastapi import APIRouter, Query

from ..knowledge_graph import knowledge_graph

router = APIRouter()


@router.get("/")
async def kg_status():
    """Get knowledge graph status."""
    return {
        "status": "active",
        **knowledge_graph.get_stats(),
    }


@router.post("/build")
async def build_graph():
    """Build the knowledge graph from the legal corpus."""
    result = knowledge_graph.build_from_corpus()
    return {"status": "built", **result}


@router.get("/search")
async def search_graph(query: str, limit: int = Query(10, ge=1, le=50)):
    """Search the knowledge graph."""
    results = knowledge_graph.search(query, limit)
    return {"query": query, "results": results}


@router.get("/node/{node_id}")
async def get_node(node_id: str):
    """Get node details with neighbors."""
    node = knowledge_graph.get_node(node_id)
    if not node:
        return {"error": "Node not found"}

    neighbors = knowledge_graph.get_neighbors(node_id)
    predecessors = knowledge_graph.get_predecessors(node_id)

    return {
        "node": {
            "id": node.id,
            "label": node.label,
            "properties": node.properties,
        },
        "neighbors": [
            {"id": n.id, "label": n.label, "title": n.properties.get("title", "")}
            for n in neighbors
        ],
        "predecessors": [
            {"id": p.id, "label": p.label, "title": p.properties.get("title", "")}
            for p in predecessors
        ],
    }


@router.get("/impact/{node_id}")
async def impact_query(node_id: str, max_depth: int = Query(3, ge=1, le=5)):
    """Find all nodes affected by a change to the given node."""
    result = knowledge_graph.impact_query(node_id, max_depth)
    return {
        "change_node": result.change_node,
        "affected_count": result.affected_count,
        "max_depth": result.max_depth,
        "affected_nodes": result.affected_nodes,
    }


@router.get("/path")
async def find_path(source: str, target: str, max_depth: int = Query(4, ge=1, le=6)):
    """Find path between two nodes."""
    path = knowledge_graph.find_path(source, target, max_depth)
    if path:
        return {
            "source": source,
            "target": target,
            "path": path,
            "length": len(path) - 1,
        }
    return {
        "source": source,
        "target": target,
        "path": None,
        "message": "No path found",
    }
