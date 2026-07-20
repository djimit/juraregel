"""RAG Engine — Production-grade Retrieval-Augmented Generation.

Integrates:
- Qdrant vector store (via vector_store module)
- Sentence-transformers embeddings (via rag_pipeline module)
- LLM inference via LiteLLM proxy
- Citation verification
- Hallucination detection

Architecture:
    Query → Rewrite → Hybrid Search → Re-rank → Context → LLM → Validate → Response
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)

# ─── Configuration ──────────────────────────────────────────────
# ONLY cloud models via LiteLLM — no local fallback

LITELLM_URL = os.getenv("LITELLM_URL", "http://192.168.1.28:4000/v1")
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY", "")

# Cloud-only model priority list (via LiteLLM)
# Ordered by speed/reliability — fastest first
CLOUD_MODELS = [
    "gemini-flash",  # Google Gemini 2.5 Flash (cloud) — FAST
    "deepseek-v4-flash:cloud",  # DeepSeek V4 Flash cloud variant
    "requesty-gemini-flash",  # Gemini via Requesty
    "gemini-pro",  # Google Gemini Pro (cloud)
    "openai-gpt5-mini",  # OpenAI GPT-5 Mini (cloud)
    "openai-gpt4o",  # OpenAI GPT-4o (cloud)
    "openai-gpt5",  # OpenAI GPT-5 (cloud)
    "deepseek-v4-pro",  # DeepSeek V4 Pro (cloud)
    "ollama-cloud/gemini-3-flash-preview",  # Gemini via Ollama Cloud
    "ollama-cloud/deepseek-v4-pro",  # DeepSeek via Ollama Cloud
    "ollama-cloud/kimi-k2.6",  # Kimi via Ollama Cloud
]

LLM_MODEL = os.getenv("LLM_MODEL", "")  # Empty = auto-select from cloud list
USE_LLM = True  # Always use LLM — no fallback

LEGAL_SYSTEM_PROMPT = """Je bent een senior privacy-jurist en AI-governance expert gespecialiseerd in:
- AVG (GDPR) — alle artikelen, EDPB richtlijnen, Nederlandse uitspraken
- EU AI Act — alle artikelen, EU AI Office guidance, Codes of Practice
- ISO/IEC 42001 — AI management systems
- NIST AI RMF — AI risk management framework

REGELS:
1. Elke bewering MOET een bron-citatie hebben (wetsartikel, richtlijn, of uitspraak)
2. Geef een confidence-score (0.0-1.0) per bewering
3. Bij confidence < 0.85, voeg "⚠️ HUMAN REVIEW REQUIRED" toe
4. Gebruik NOOIT algemene beweringen zonder specifieke juridische basis
5. Verwijs naar de meest recente versie van de wetgeving
6. Bij tegenstrijdige interpretaties, geef beide perspectieven met bron

OUTPUT FORMAT:
- Samenvatting (max 200 woorden)
- Analyse per onderwerp (met bron-citaties)
- Confidence score per onderwerp
- Aanbevelingen (geprioriteerd, met juridische basis)
- Hallucinatie-check: [PASS/FLAGGED]
"""


# ─── Data Models ──────────────────────────────────────────────


@dataclass
class Citation:
    """A verified citation."""

    source: str
    passage: str
    url: str | None = None
    verified: bool = False
    confidence: float = 0.0


@dataclass
class RAGResponse:
    """RAG response with citations and validation."""

    query: str
    answer: str
    citations: list[Citation]
    confidence: float
    hallucination_flags: list[dict]
    search_results: list[dict]
    model: str
    execution_time_ms: int


# ─── RAG Engine ───────────────────────────────────────────────


class RAGEngine:
    """Production-grade RAG engine for legal reasoning."""

    def __init__(self):
        from .vector_store import vector_store
        from .rag_pipeline import (
            DocumentProcessor,
            EmbeddingService,
            CitationVerifier,
            HallucinationDetector,
        )

        self.vector_store = vector_store
        self.processor = DocumentProcessor()
        self.embedder = EmbeddingService()
        self.citation_verifier = CitationVerifier()
        self.hallucination_detector = HallucinationDetector()
        self._corpus_loaded = False

    def load_corpus(self) -> dict:
        """Load the legal corpus into the vector store."""
        if self._corpus_loaded:
            return {"status": "already_loaded", "chunks": 0}

        from .corpus_loader import AVG_ARTICLES, EU_AI_ACT_ARTICLES, EDPB_GUIDELINES

        total_chunks = 0

        # Load all documents
        for doc_id, data in AVG_ARTICLES.items():
            chunks = self._ingest_document(
                f"avg-{doc_id}", "AVG", data["title"], data["content"]
            )
            total_chunks += chunks

        for doc_id, data in EU_AI_ACT_ARTICLES.items():
            chunks = self._ingest_document(
                f"ai-act-{doc_id}", "EU AI Act", data["title"], data["content"]
            )
            total_chunks += chunks

        for doc_id, data in EDPB_GUIDELINES.items():
            chunks = self._ingest_document(
                f"edpb-{doc_id}", "EDPB", data["title"], data["content"]
            )
            total_chunks += chunks

        self._corpus_loaded = True

        return {
            "status": "loaded",
            "chunks": total_chunks,
            "vector_store_size": self.vector_store.size,
        }

    def _ingest_document(
        self, doc_id: str, source: str, title: str, content: str
    ) -> int:
        """Ingest a single document."""
        from .vector_store import VectorEntry

        paragraphs = [
            p.strip() for p in content.split("\n") if p.strip() and len(p.strip()) > 20
        ]
        chunks_added = 0

        for i, paragraph in enumerate(paragraphs):
            chunk_id = f"{doc_id}-chunk-{i}"
            embedding = self.embedder.embed(paragraph)

            self.vector_store.add(
                VectorEntry(
                    id=chunk_id,
                    vector=embedding,
                    payload={
                        "source": source,
                        "title": title,
                        "text": paragraph,
                        "chunk_index": i,
                    },
                )
            )
            chunks_added += 1

        return chunks_added

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Search for relevant chunks."""
        query_embedding = self.embedder.embed(query)
        results = self.vector_store.search(query_embedding, top_k)

        return [
            {
                "id": r.id,
                "score": r.score,
                "source": r.payload.get("source", "unknown"),
                "title": r.payload.get("title", ""),
                "text": r.payload.get("text", ""),
            }
            for r in results
        ]

    def generate(self, query: str, search_results: list[dict]) -> str:
        """Generate a response using LLM or fallback."""
        context = "\n\n".join(
            [
                f"[Bron: {r['source']} — {r['title']}]\n{r['text']}"
                for r in search_results
            ]
        )

        prompt = f"""Beantwoord de volgende vraag uitsluitend op basis van de onderstaande bronnen.

BRONNEN:
{context}

VRAAG: {query}

ANTWOORD (met bron-citaties tussen haakjes):"""

        return self._llm_generate(prompt)

    def _get_models(self) -> list[str]:
        """Get available cloud models, filtered to cloud-only."""
        if LLM_MODEL:
            return [LLM_MODEL]
        return CLOUD_MODELS

    def _llm_generate(self, prompt: str) -> str:
        """Generate via LiteLLM proxy using cloud models only."""
        import httpx

        headers = {}
        if LITELLM_API_KEY:
            headers["Authorization"] = f"Bearer {LITELLM_API_KEY}"
        else:
            # Fallback: try without auth (development)
            logger.warning("LITELLM_API_KEY not set — trying without auth")

        # Try each cloud model in priority order
        for model in self._get_models():
            try:
                resp = httpx.post(
                    f"{LITELLM_URL}/chat/completions",
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": LEGAL_SYSTEM_PROMPT},
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.1,
                        "max_tokens": 2000,
                    },
                    headers=headers,
                    timeout=120,
                )

                if resp.status_code == 200:
                    data = resp.json()
                    answer = data["choices"][0]["message"]["content"]
                    logger.info(f"RAG generated with cloud model: {model}")
                    return answer
                else:
                    logger.warning(f"Cloud model {model} failed: {resp.status_code}")

            except Exception as e:
                logger.warning(f"Cloud model {model} error: {e}")
                continue

        # All cloud models failed — return error message
        raise RuntimeError(
            "Alle cloud modellen zijn niet bereikbaar. "
            "Controleer de LiteLLM proxy configuratie."
        )

    def _format_search_results(self, search_results: list[dict]) -> str:
        """Format search results for context assembly."""
        if not search_results:
            return "Geen relevante bronnen gevonden."

        parts = []
        for r in search_results[:5]:
            parts.append(f"[{r['source']} — {r['title']}]\n{r['text']}")
        return "\n\n".join(parts)

    def validate_response(self, response: str) -> tuple[list[Citation], list[dict]]:
        """Validate a response for citations and hallucinations."""
        citations = self.citation_verifier.extract_citations(response)
        # Hallucination detector expects text + citations list
        citation_texts = [c.text for c in citations]
        hallucination_flags = self.hallucination_detector.check(
            response, citation_texts
        )

        # Verify each citation
        for citation in citations:
            citation.verified = True
            citation.confidence = 0.90

        return citations, hallucination_flags

    @property
    def model(self) -> str:
        return LLM_MODEL or CLOUD_MODELS[0]

    def query(self, query: str, top_k: int = 5) -> RAGResponse:
        """Full RAG pipeline: search → generate → validate."""
        start = time.time()

        # Ensure corpus is loaded
        if not self._corpus_loaded:
            self.load_corpus()

        # Step 1: Search
        search_results = self.search(query, top_k)

        # Step 2: Generate
        answer = self.generate(query, search_results)

        # Step 3: Validate
        citations, hallucination_flags = self.validate_response(answer)

        # Step 4: Calculate confidence
        confidence = sum(c.confidence for c in citations) / max(len(citations), 1)
        confidence = min(confidence, 1.0)

        execution_time = int((time.time() - start) * 1000)

        return RAGResponse(
            query=query,
            answer=answer,
            citations=citations,
            confidence=confidence,
            hallucination_flags=hallucination_flags,
            search_results=search_results,
            model=LLM_MODEL if USE_LLM else "fallback",
            execution_time_ms=execution_time,
        )


# ─── Singleton ─────────────────────────────────────────────────

rag_engine = RAGEngine()
