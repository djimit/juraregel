# JuraRegel Agentic Platform - Architectuur

## Overzicht

Het JuraRegel Agentic Platform breidt het Legal RuleOps Platform uit met:

- **Knowledge Base** (702 regels, semantisch + keyword doorzoekbaar)
- **MCP Server** (12 tools + 3 resources + 3 prompts voor LLM-agents)
- **Source Connectors** (BWB, EUR-Lex, PLOOI, Rechtspraak)
- **Rule Extraction Pipeline** (LLM-assisted, met review queue)
- **Governance Registry** (32 domeinen, 5 niveaus)
- **Agent Playbooks** (12 playbooks)
- **Gherkin BDD Tests** (7 scenarios, legal team acceptatie)
- **BWB Harvester** (automatische wetwijziging-detectie)
- **JREM Schema Versioning** (v1.0.0, v1.1.0)

## Architectuur

```
Agent (Claude/GPT/Lokaal)
  | MCP Protocol (stdio)
  v
JuraRegel MCP Server v2.1.0 (12 tools + 3 resources + 3 prompts)
  |
  +--> Knowledge Base
  |      +-- Qdrant (vector search, 768-dim, nomic-embed-text)
  |      +-- SQLite FTS5 (keyword search)
  |      +-- JKB Index Builder (702 regels, 3 representaties)
  |
  +--> Source Connectors
  |      +-- BWB (wetten.overheid.nl) + Harvester
  |      +-- EUR-Lex (SPARQL)
  |      +-- PLOOI (legacy/officiele publicaties)
  |      +-- Rechtspraak (Open Data)
  |      +-- UPL + TOOI/ROO (dienstverlening en organisatiecontext)
  |      +-- CVDR/SRU + Woo/DiWoo + STTR/RTR (preflight bronlagen)
  |
  +--> Rule Extraction Pipeline
  |      +-- Pattern-based extraction
  |      +-- Confidence scoring
  |      +-- FastAPI review queue
  |
  +--> Governance Registry (JSON-LD, 32 domeinen)
  |
  +--> Agent Playbooks (12 playbooks)
```

## MCP Interface

### Tools (12)

| Tool | Doel |
|------|------|
| juraregel.list_domains | Lijst van alle domeinen |
| juraregel.get_rules | Regels voor een domein |
| juraregel.search_rules | Zoek regels |
| juraregel.calculate | Bereken juridisch resultaat |
| juraregel.get_sources | Bronverwijzingen |
| juraregel.trace | Audit trail |
| juraregel.version_diff | Verschil tussen versies |
| juraregel.semantic_search | Semantisch zoeken (Qdrant/FTS5) |
| juraregel.explain | Berekening uitleggen |
| juraregel.check_compliance | Compliance check |
| juraregel.get_playbook | Agent playbook |
| juraregel.get_governance | Governance info |

### Resources (3+)

| Resource | Doel |
|----------|------|
| laws://list | Lijst van alle domeinen |
| laws://summary | KB samenvatting |
| laws://{domain}/spec | Volledige JREM specificatie |
| profile://{domain} | Input/output profiel |

### Prompts (3)

| Prompt | Doel |
|--------|------|
| check_all_benefits | Controleer alle uitkeringen |
| explain_calculation | Leg berekening uit |
| compare_scenarios | Vergelijk scenario s |

## CI/CD Gates

| Gate | Script | Doel |
|------|--------|------|
| Per-use-case (14 gates) | ci/run-gates.sh | JREM validatie, tests, acceptatie |
| JKB (5 gates) | ci/jkb-gates.sh | Knowledge base completheid |
| Extraction (3 gates) | ci/extraction-gates.sh | Extractie kwaliteit |
| Schema Versioning | ci/jrem-schema-version-check.sh | JREM schema versie validatie |
| BDD Tests | ci/run-bdd-tests.sh | Gherkin scenario s |
| Harvester Health | ci/harvester-health.sh | BWB endpoint bereikbaar |

## JREM Schema Versioning

Versie | Bestand | Wijzigingen
-------|---------|-------------
v1.0.0 | shared/jrem-schema-v1.0.0.json | Basis schema met $id
v1.1.0 | shared/jrem-schema-v1.1.0.json | + governanceLevel, bwbId, celexId, eli

Migratie: `python3 tools/jrem-migrate.py`

## BDD Tests

Feature files in `features/`:

- `toeslagen.feature` - 4 scenarios (zorgtoeslag berekening)
- `bio2.feature` - 3 scenarios (BIO2 compliance)
- `participatiewet.feature` - 1 scenario (bijstand)

Run: `bash ci/run-bdd-tests.sh`

## Starten

```bash
# Knowledge Base bouwen
python3 tools/jkb-builder.py

# Keyword store indexeren
python3 tools/jkb-keyword.py index

# Vector store indexeren (vereist embedding API)
python3 tools/jkb-builder.py
python3 tools/jkb_vectorstore.py index

# JREM exports migreren naar v1.1.0
python3 tools/jrem-migrate.py

# MCP Server starten (stdio)
python3 mcp-server/juraregel_mcp.py

# BDD tests draaien
bash ci/run-bdd-tests.sh

# Harvester health check
python3 sources/harvester.py --health
```

## Dependencies

- Python 3.12+
- FastAPI (review queue)
- Qdrant client (vector store, embedded mode)
- OpenAI-compatible API (embeddings, nomic-embed-text via LiteLLM)
- pytest-bdd (BDD test framework)
