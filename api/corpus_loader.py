"""Document Corpus Loader — Load legal documents into the RAG pipeline.

Loads:
- AVG (GDPR) — Full regulation text
- EU AI Act — Full regulation text
- EDPB Guidelines — Key guidance documents
- AP Richtlijnen — Dutch guidance
- Model DPIA Rijksdutch — Official DPIA template

Documents are chunked, embedded, and stored in the vector store.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


# ─── Built-in Legal Corpus (Essential Articles) ──────────────

AVG_ARTICLES = {
    "art5": {
        "title": "Artikel 5 — Beginselen in verband met de verwerking van persoonsgegevens",
        "content": (
            "1. Persoonsgegevens worden:\n"
            "a) op een behoorlijke en transparante wijze verwerkt ten aanzien van de betrokkene ('rechtmatigheid, behoorlijkheid en transparantie');\n"
            "b) verzameld voor omschreven, uitdrukkelijk omschreven en legitieme doeleinden en niet verder verwerken op een wijze die onverenigbaar is met die doeleinden ('doelbinding');\n"
            "c) toereikend, relevant en beperkt tot het noodzakelijke voor de doeleinden waarvoor ze worden verwerkt ('gegevensminimisering');\n"
            "d) juist en zo nodig geactualiseerd; met inachtneming van redelijke maatregelen moet worden gewaarborgd dat persoonsgegevens die onjuist zijn, voor de doeleinden waarvoor ze worden verwerkt, onverwijderd of gecorrigeerd worden ('juistheid');\n"
            "e) opgeslagen in een vorm die de identificatie van betrokkenen slechts mogelijk zolang als noodzakelijk is voor de doeleinden waarvoor de persoonsgegevens worden verwerkt ('opslagbeperking');\n"
            "f) verwerkt op een wijze die een passende beveiliging van de persoonsgegevens waarborgt, waaronder bescherming tegen ongeautoriseerde of onwettige verwerking en tegen per ongeluk verlies, vernietiging of schade ('integriteit en vertrouwelijkheid').\n"
            "2. De verwerkingsverantwoordelijke is verantwoordelijk voor en moet kunnen aantonen dat aan lid 1 wordt voldaan ('verantwoordingsplicht')."
        ),
    },
    "art6": {
        "title": "Artikel 6 — Rechtmatigheid van de verwerking",
        "content": (
            "1. Verwerking is alleen rechtmatig indien en voor zover ten minste een van de volgende van toepassing is:\n"
            "a) de betrokkene heeft toestemming verleend voor de verwerking van zijn persoonsgegevens voor een of meer specifieke doeleinden ('toestemming');\n"
            "b) de verwerking is noodzakelijk voor de uitvoering van een overeenkomst waarbij de betrokkene partij is ('contract');\n"
            "c) de verwerking is noodzakelijk om te voldoen aan een wettelijke verplichting ('wettelijke verplichting');\n"
            "d) de verwerking is noodzakelijk voor de bescherming van de vitale belangen van de betrokkene of van een andere natuurlijke persoon ('vitale belangen');\n"
            "e) de verwerking is noodzakelijk voor de vervulling van een taak van algemeen belang ('openbaar belang');\n"
            "f) de verwerking is noodzakelijk voor de bescherming van de gerechtvaardigde belangen van de verwerkingsverantwoordelijke of van een derde ('gerechtvaardigd belang')."
        ),
    },
    "art25": {
        "title": "Artikel 25 — Gegevensbescherming door ontwerp en door standaardinstellingen",
        "content": (
            "1. De verwerkingsverantwoordelijke implementeert passende technische en organisatorische maatregelen om er zorg voor te dragen dat alleen persoonsgegevens worden verwerkt die noodzakelijk zijn voor elk specifiek doel van de verwerking.\n"
            "2. Deze verplichting geldt voor de hoeveelheid verzamelde persoonsgegevens, de omvang van de verwerking, de opslagduur en de toegankelijkheid."
        ),
    },
    "art32": {
        "title": "Artikel 32 — Beveiliging van de verwerking",
        "content": (
            "1. De verwerkingsverantwoordelijke en de verwerker passen passende technische en organisatorische maatregelen toe om een beveiligingsniveau te waarborgen dat past bij het risico, waaronder, waar van toepassing:\n"
            "a) pseudonimisering en encryptie van persoonsgegevens;\n"
            "b) het vermogen om de vertrouwelijkheid, integriteit, beschikbaarheid en de veerkracht van de verwerkingssystemen en -diensten te waarborgen;\n"
            "c) het vermogen om de toegang tot persoonsgegevens te beperken."
        ),
    },
    "art35": {
        "title": "Artikel 35 — Beoordeling van de gevolgen van de verwerking voor de bescherming van persoonsgegevens (DPIA)",
        "content": (
            "1. Wanneer een verwerking waarschijnlijk een hoog risico oplevert voor de rechten en vrijheden van natuurlijke personen, voert de verwerkingsverantwoordelijke voorafgaand aan de verwerking een beoordeling uit van de gevolgen van de voorgenomen verwerking voor de bescherming van persoonsgegevens.\n"
            "3. Een DPIA is in ieder geval verplicht in de volgende gevallen:\n"
            "a) systematische en grootschalige evaluatie van persoonlijke aspecten van natuurlijke personen op basis van geautomatiseerde verwerking, waaronder profiling;\n"
            "b) grootschalige verwerking van bijzondere categorieen persoonsgegevens of van persoonsgegevens betreffende strafrechtelijke veroordelingen;\n"
            "c) systematische monitoring van een voor het publiek toegankelijk ruimte op grote schaal."
        ),
    },
}

EU_AI_ACT_ARTICLES = {
    "art5": {
        "title": "Article 5 — Prohibited AI Practices",
        "content": (
            "AI systems which deploy subliminal techniques, exploit vulnerabilities of specific groups, "
            "use social scoring by public authorities, or use real-time remote biometric identification "
            "in publicly accessible spaces for the purpose of law enforcement shall be prohibited."
        ),
    },
    "art6": {
        "title": "Article 6 — Classification of High-Risk AI Systems",
        "content": (
            "AI systems shall be considered high-risk where they are intended to be used as safety "
            "components of products, or are themselves products, covered by existing Union harmonisation "
            "legislation listed in Annex I, or are intended to be used for the purposes listed in Annex III."
        ),
    },
    "art9": {
        "title": "Article 9 — Risk Management System",
        "content": (
            "High-risk AI systems shall be designed and developed with a risk management system "
            "that consists of a continuous iterative process run throughout the entire lifecycle, including:\n"
            "(a) identification and analysis of known and foreseeable risks;\n"
            "(b) estimation and evaluation of risks that may emerge when the system is used;\n"
            "(c) evaluation of risks arising from post-market monitoring data;\n"
            "(d) adoption of appropriate and targeted risk management measures."
        ),
    },
    "art10": {
        "title": "Article 10 — Data and Data Governance",
        "content": (
            "High-risk AI systems which make use of techniques involving the training of models with data "
            "shall be developed on the basis of training, validation and testing data sets that meet the "
            "quality criteria, are relevant, sufficiently representative and to the best extent possible "
            "free of errors and complete."
        ),
    },
    "art14": {
        "title": "Article 14 — Human Oversight",
        "content": (
            "High-risk AI systems shall be designed and developed in such a way that they can be "
            "effectively overseen by natural persons during the period in which the AI system is in use, "
            "including the ability to understand, intervene, overrule, or stop the system."
        ),
    },
    "art27": {
        "title": "Article 27 — Fundamental Rights Impact Assessment (FRIA)",
        "content": (
            "Deployers of high-risk AI systems shall carry out a fundamental rights impact assessment "
            "before putting the system into use. The assessment shall contain at least:\n"
            "(a) a description of the deployer's processes in which the system will be used;\n"
            "(b) the period and frequency of use;\n"
            "(c) the categories of natural persons likely to be affected;\n"
            "(d) the specific risks of harm likely to arise;\n"
            "(e) a description of how risks will be mitigated;\n"
            "(f) the human oversight measures that will be implemented."
        ),
    },
}

EDPB_GUIDELINES = {
    "wp29-dpia": {
        "title": "EDPB WP29 Guidelines on DPIA (2017)",
        "content": (
            "The WP29 identifies 9 criteria that indicate whether a processing operation is likely "
            "to result in a high risk:\n"
            "1. Evaluation or scoring, including profiling\n"
            "2. Automated decision-making with legal or significant effects\n"
            "3. Systematic monitoring of publicly accessible areas\n"
            "4. Sensitive data or data of a highly personal nature\n"
            "5. Data processed on a large scale\n"
            "6. Matching or combining datasets\n"
            "7. Data concerning vulnerable data subjects\n"
            "8. Innovative use or applying new technological solutions\n"
            "9. Where the processing prevents data subjects from exercising a right or using a service."
        ),
    },
    "wp29-art25": {
        "title": "EDPB Guidelines on Data Protection by Design and by Default",
        "content": (
            "Key principles:\n"
            "1. Proactive not reactive; preventive not remedial\n"
            "2. Privacy as the default setting\n"
            "3. Privacy embedded into design\n"
            "4. Full functionality (positive-sum, not zero-sum)\n"
            "5. End-to-end security (full lifecycle protection)\n"
            "6. Visibility and transparency\n"
            "7. Respect for user privacy (user-centric)."
        ),
    },
}


# ─── Corpus Loader ────────────────────────────────────────────


class CorpusLoader:
    """Load legal documents into the RAG pipeline."""

    def __init__(self, rag_pipeline=None, vector_store=None):
        self.pipeline = rag_pipeline
        self.vector_store = vector_store
        self._loaded = False

    def load_builtin_corpus(self) -> dict:
        """Load the built-in legal corpus."""
        if self._loaded:
            return {"status": "already_loaded", "chunks": 0}

        total_chunks = 0

        # Load AVG articles
        for art_id, data in AVG_ARTICLES.items():
            chunks = self._process_document(
                doc_id=f"avg-{art_id}",
                source="AVG",
                title=data["title"],
                content=data.get("content", ""),
                url="https://eur-lex.europa.eu/legal-content/NL/TXT/?uri=CELEX:32016R0679",
            )
            total_chunks += chunks

        # Load EU AI Act articles
        for art_id, data in EU_AI_ACT_ARTICLES.items():
            chunks = self._process_document(
                doc_id=f"ai-act-{art_id}",
                source="EU AI Act",
                title=data["title"],
                content=data.get("content", ""),
                url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng",
            )
            total_chunks += chunks

        # Load EDPB guidelines
        for guide_id, data in EDPB_GUIDELINES.items():
            chunks = self._process_document(
                doc_id=f"edpb-{guide_id}",
                source="EDPB",
                title=data["title"],
                content=data.get("content", ""),
                url="https://edpb.europa.eu/",
            )
            total_chunks += chunks

        self._loaded = True

        return {
            "status": "loaded",
            "chunks": total_chunks,
            "documents": len(AVG_ARTICLES)
            + len(EU_AI_ACT_ARTICLES)
            + len(EDPB_GUIDELINES),
            "sources": ["AVG", "EU AI Act", "EDPB"],
        }

    def _process_document(
        self, doc_id: str, source: str, title: str, content: str, url: str
    ) -> int:
        """Process a single document into the vector store."""
        if not content:
            return 0

        # Chunk by paragraph
        paragraphs = [
            p.strip() for p in content.split("\n") if p.strip() and len(p.strip()) > 20
        ]

        chunks_added = 0
        for i, paragraph in enumerate(paragraphs):
            chunk_id = f"{doc_id}-chunk-{i}"

            # Generate embedding
            if self.pipeline:
                embedding = self.pipeline.embedder.embed(paragraph)
            else:
                embedding = self._simple_embed(paragraph)

            # Store in vector store
            if self.vector_store:
                from .vector_store import VectorEntry

                self.vector_store.add(
                    VectorEntry(
                        id=chunk_id,
                        vector=embedding,
                        payload={
                            "source": source,
                            "title": title,
                            "url": url,
                            "chunk_index": i,
                            "text": paragraph,
                        },
                    )
                )
                chunks_added += 1

        return chunks_added

    def _simple_embed(self, text: str, dim: int = 384) -> list[float]:
        """Simple hash-based embedding fallback."""
        import hashlib
        import struct

        vec = [0.0] * dim
        words = text.lower().split()

        for word in words:
            hash_bytes = hashlib.sha256(word.encode()).digest()
            for i in range(0, min(len(hash_bytes), dim * 4), 4):
                idx = (i // 4) % dim
                val = struct.unpack("f", hash_bytes[i : i + 4])[0]
                vec[idx] += val

        magnitude = sum(v**2 for v in vec) ** 0.5
        if magnitude > 0:
            vec = [v / magnitude for v in vec]

        return vec


# ─── Convenience Function ─────────────────────────────────────


def load_corpus() -> dict:
    """Load the built-in legal corpus into the vector store."""
    from .vector_store import vector_store

    loader = CorpusLoader(vector_store=vector_store)
    return loader.load_builtin_corpus()
