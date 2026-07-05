# Changelog

## [2.0.0] - 2025-07-05 — Agentic BV Nederland

### Toegevoegd

**Knowledge Base (Product 1)**
- JKB Index Builder: 655 regels, 3 representaties (JREM, NL tekst, embedding)
- Qdrant vector store (embedded mode, 1536-dim cosine)
- SQLite FTS5 keyword store (ponytail: geen Meilisearch server)
- JKB CI Gates: 5 validaties

**MCP Server Enhancement (Product 2)**
- 5 nieuwe tools: semantic_search, explain, check_compliance, get_playbook, get_governance
- Totaal: 12 MCP tools
- End-to-end test suite: 14 tests

**Government Source Connectors (Product 3)**
- BWB connector (wetten.overheid.nl)
- EUR-Lex connector (SPARQL)
- PLOOI connector (officiele publicaties)
- Rechtspraak connector (Open Data)
- Scheduler + health checks

**Rule Extraction Pipeline (Product 4)**
- Pattern-based extraction engine
- Confidence scoring (0-100)
- FastAPI review queue
- Extraction CI gates

**Governance Registry (Product 5)**
- JSON-LD registry: 32 domeinen
- Hierarchy resolver (EU>Rijk>Provincie>Gemeente>Waterschap)
- Registry validator CI gate

**Agent Playbooks (Product 6)**
- 12 playbooks voor veelvoorkomende scenario's
- Playbook validator

**Documentatie & CI/CD (Product 7)**
- Architectuur documentatie
- CI integratie (JKB gates in run-all-gates.sh)

### Statistieken
- 28 use cases
- 655 JREM regels
- 438+ tests
- 12 MCP tools
- 12 agent playbooks
- 32 governance domeinen
