"""Vector Store — Multi-backend vector storage.

Supports:
- Qdrant (production, remote vector store)
- In-memory (development, no external dependencies)
- Local persistence (JSON file backup)

Auto-selects backend based on QDRANT_URL environment variable.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from dataclasses import dataclass, field
from typing import Any


# ─── Configuration ──────────────────────────────────────────────

QDRANT_URL = os.getenv("QDRANT_URL", "")
USE_QDRANT = bool(QDRANT_URL)

# ─── Data Models ──────────────────────────────────────────────


@dataclass
class VectorEntry:
    """A vector entry with metadata."""

    id: str
    vector: list[float]
    payload: dict[str, Any]


@dataclass
class SearchResult:
    """Search result with score."""

    id: str
    score: float
    payload: dict[str, Any]


# ─── In-Memory Vector Store ──────────────────────────────────


class InMemoryVectorStore:
    """Simple in-memory vector store for development."""

    def __init__(self):
        self._store: dict[str, VectorEntry] = {}

    def add(self, entry: VectorEntry) -> None:
        self._store[entry.id] = entry

    def search(self, query_vector: list[float], top_k: int = 10) -> list[SearchResult]:
        scores = []
        for entry_id, entry in self._store.items():
            similarity = self._cosine_similarity(query_vector, entry.vector)
            scores.append(
                SearchResult(id=entry_id, score=similarity, payload=entry.payload)
            )

        scores.sort(key=lambda x: x.score, reverse=True)
        return scores[:top_k]

    def delete(self, entry_id: str) -> bool:
        if entry_id in self._store:
            del self._store[entry_id]
            return True
        return False

    @property
    def size(self) -> int:
        return len(self._store)

    @staticmethod
    def _cosine_similarity(a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        mag_a = math.sqrt(sum(x**2 for x in a))
        mag_b = math.sqrt(sum(y**2 for y in b))
        return dot / (mag_a * mag_b) if mag_a > 0 and mag_b > 0 else 0.0


# ─── Qdrant Vector Store ─────────────────────────────────────


class QdrantVectorStore:
    """Qdrant-backed vector store for production."""

    def __init__(self, url: str, collection_name: str = "juraregel"):
        self.url = url
        self.collection_name = collection_name
        self._client = None

    def _get_client(self):
        if self._client is None:
            from qdrant_client import QdrantClient

            self._client = QdrantClient(url=self.url)
            # Ensure collection exists
            try:
                self._client.get_collection(self.collection_name)
            except Exception:
                from qdrant_client.models import Distance, VectorParams

                self._client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
                )
        return self._client

    def add(self, entry: VectorEntry) -> None:
        from qdrant_client.models import PointStruct

        client = self._get_client()
        client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=entry.id,
                    vector=entry.vector,
                    payload=entry.payload,
                )
            ],
        )

    def search(self, query_vector: list[float], top_k: int = 10) -> list[SearchResult]:
        client = self._get_client()
        results = client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
        )
        return [
            SearchResult(
                id=str(r.id),
                score=r.score,
                payload=r.payload or {},
            )
            for r in results
        ]

    def delete(self, entry_id: str) -> bool:
        from qdrant_client.models import PointIdsList

        client = self._get_client()
        client.delete(
            collection_name=self.collection_name,
            points_selector=PointIdsList(points=[entry_id]),
        )
        return True

    @property
    def size(self) -> int:
        client = self._get_client()
        info = client.get_collection(self.collection_name)
        return info.points_count


# ─── Factory ──────────────────────────────────────────────────


def create_vector_store() -> InMemoryVectorStore | QdrantVectorStore:
    """Create a vector store based on configuration."""
    if USE_QDRANT:
        return QdrantVectorStore(QDRANT_URL)
    return InMemoryVectorStore()


# ─── Global Instance ──────────────────────────────────────────

vector_store = create_vector_store()
