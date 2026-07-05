## [2.1.2] - 2026-07-05 -- Maturity Model & Evidence

### Added
- Maturity model L0-L3 (demo, PoC, pilot, production)
- maturityLevel field in alle 29 JREM exports
- BIO2 evidence store (SQLite) + POST /v1/bio2/assessments
- BIO2 rapport miturityLevel + limitations in audit
- requirements.txt mit pinned dependencies
- docs/trust-report.md
- Health endpoint: maturityLevel + approvalStatus + limitations

### Changed
- validate-jrem.py: CI_MODE=poc|pilot|production
- Legal review gate: warn-only PoC, fail in pilot/production
- CI workflow: poc + pilot jobs
- HTTPBearer auto_error=False (auth disabled by default)

### Fixed
- HTTPBearer auto_error bug
- v1.1.0 schema: validUntil nullable
- 64/64 tests passed (57 griffierecht + 7 BDD)

---

## [2.1.1] - 2025-07-05 — Hardening

### Fixed
- CI/CD: alle `|| true` verwijderd — gates falen echt bij errors
- CLI: syntax errors gefixt (`bin/juraregel.mjs`)
- Dockerfile: expose poorten gecorrigeerd (8490-8515)
- JREM v1.1.0: `$id` en description gecorrigeerd
- JREM v1.1.0: outcome required fields veralgemeend (niet griffierecht-specifiek)
- API auth: "any token" vervangen door API key validatie
- CORS: restricted to configured origins

### Added
- `shared/jrem-core.json` — generiek JREM kernschema
- `tools/jrem-migrate.py` v2.0 — verbeterde migratie met validatie
- `ci/legal-review-gate.sh` — waarschuwt bij self-approved regels
- SECURITY.md met security model
- `approval` object ter vervanging van `juristAccordering`

### Changed
- `juristAccordering` vervangen door auditable `approval` object in alle exports
- Accuracy claim gesanitizeerd ("hoog" ipv "100%")
- Disclaimer toegevoegd aan README

---

# Changelog

## [2.1.0] - 2025-07-05 - MinBZK Improvements

### Toegevoegd

**MCP Resources + Prompts (van poc-machine-law)**
- 3 resources: `laws://list`, `laws://summary`, `laws://{domain}/spec`, `profile://{domain}`
- 3 prompts: `check_all_benefits`, `explain_calculation`, `compare_scenarios`
- MCP server versie 2.1.0 met resources + prompts capabilities
- Test suite: 9 resource/prompt tests

**JREM Schema Versioning (van regelrecht)**
- `shared/jrem-schema-v1.0.0.json` - versioned schema met `$id`
- `shared/jrem-schema-v1.1.0.json` - uitbreiding met governanceLevel, bwbId, celexId, eli
- `tools/jrem-migrate.py` - migratie tool (v1.0.0 -> v1.1.0)
- `ci/jrem-schema-version-check.sh` - CI gate
- Alle 29 JREM exports gemigreerd naar v1.1.0

**Gherkin BDD Tests (van regelrecht)**
- `features/toeslagen.feature` - 4 scenarios (zorgtoeslag)
- `features/bio2.feature` - 3 scenarios (BIO2 compliance)
- `features/participatiewet.feature` - 1 scenario (bijstand)
- `features/steps/juraregel_steps.py` - step definitions
- `ci/run-bdd-tests.sh` - CI gate
- 7/7 BDD tests pass

**BWB Harvester (van regelrecht)**
- `sources/harvester.py` - BWB API client met diff detection
- State tracking in `.data/harvester-state.json`
- Health check: `python3 sources/harvester.py --health`
- `ci/harvester-health.sh` - CI gate

### Gewijzigd
- JREM exports: schemaVersion bijgewerkt van 1.0.0 naar 1.1.0
- MCP server: capabilities uitgebreid met resources + prompts
- README badges bijgewerkt

### Statistieken
- 28 use cases
- 655 JREM regels (v1.1.0 schema)
- 445+ tests (438 bestaand + 7 BDD + 9 MCP resources)
- 12 MCP tools + 3 resources + 3 prompts
- 12 agent playbooks
- 32 governance domeinen
- 4 versioned schema versies (v1.0.0, v1.1.0)

---

## [2.0.0] - 2025-07-05 - Agentic BV Nederland

### Toegevoegd

**Knowledge Base (Product 1)**
- JKB Index Builder: 655 regels, 3 representaties (JREM, NL tekst, embedding)
- Qdrant vector store (embedded mode, 768-dim cosine, nomic-embed-text)
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
- 12 playbooks voor veelvoorkomende scenario s
- Playbook validator

**Documentatie & CI/CD (Product 7)**
- Architectuur documentatie
- CI integratie (JKB gates in run-all-gates.sh)
