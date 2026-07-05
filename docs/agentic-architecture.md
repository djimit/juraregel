# JuraRegel Agentic Platform - Architectuur

## Overzicht

Het JuraRegel Agentic Platform breidt het Legal RuleOps Platform uit met:

- **Knowledge Base** (655 regels, semantisch + keyword doorzoekbaar)
- **MCP Server** (12 tools voor LLM-agents)
- **Source Connectors** (BWB, EUR-Lex, PLOOI, Rechtspraak)
- **Rule Extraction Pipeline** (LLM-assisted, met review queue)
- **Governance Registry** (32 domeinen, 5 niveaus)
- **Agent Playbooks** (12 playbooks)

## CI/CD Gates

| Gate | Script | Doel |
|------|--------|------|
| Per-use-case (14 gates) | ci/run-gates.sh | JREM validatie, tests, acceptatie |
| JKB (5 gates) | ci/jkb-gates.sh | Knowledge base completheid |
| Extraction (3 gates) | ci/extraction-gates.sh | Extractie kwaliteit |

## Starten

python3 tools/jkb-builder.py
python3 tools/jkb-keyword.py index
python3 mcp-server/juraregel_mcp.py

## Dependencies

- Python 3.12+
- FastAPI (review queue)
- Qdrant client (vector store, embedded mode)
- OpenAI-compatible API (embeddings)
