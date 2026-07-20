"""RAG API — Retrieval-Augmented Generation for legal reasoning."""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Any

router = APIRouter()


class RAGQuery(BaseModel):
    """RAG query request."""

    query: str = Field(..., min_length=1, description="De juridische vraag")
    top_k: int = Field(default=5, ge=1, le=20, description="Aantal zoekresultaten")


class RAGResponse(BaseModel):
    """RAG response."""

    query: str
    answer: str
    citations: list[dict]
    confidence: float
    hallucination_flags: list[dict]
    search_results: list[dict]
    model: str
    execution_time_ms: int


@router.get("/")
async def rag_info():
    """Get RAG engine status."""
    from ..rag_engine import rag_engine

    return {
        "status": "active",
        "corpus_loaded": rag_engine._corpus_loaded,
        "vector_store_size": rag_engine.vector_store.size,
        "model": rag_engine.model if hasattr(rag_engine, "model") else "fallback",
    }


@router.post("/query", response_model=RAGResponse)
async def rag_query(request: RAGQuery):
    """Execute a RAG query — search legal corpus + generate answer."""
    from ..rag_engine import rag_engine

    result = rag_engine.query(request.query, request.top_k)

    return RAGResponse(
        query=result.query,
        answer=result.answer,
        citations=[
            {
                "source": c.source,
                "passage": c.passage,
                "url": c.url,
                "verified": c.verified,
                "confidence": c.confidence,
            }
            for c in result.citations
        ],
        confidence=result.confidence,
        hallucination_flags=result.hallucination_flags,
        search_results=result.search_results,
        model=result.model,
        execution_time_ms=result.execution_time_ms,
    )


@router.post("/corpus/load")
async def load_corpus():
    """Load the legal corpus into the vector store."""
    from ..rag_engine import rag_engine

    result = rag_engine.load_corpus()
    return result


@router.get("/search")
async def search_corpus(query: str, top_k: int = 5):
    """Search the legal corpus without generating an answer."""
    from ..rag_engine import rag_engine

    results = rag_engine.search(query, top_k)
    return {"query": query, "results": results}
