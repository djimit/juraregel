## [3.1.0] - 2026-07-17 — ISO 27701 Privacy Information Management

### Added
- ISO 27701 use case: 24 regels, port 8531
- PII Controller vs Processor rol-bepaling
- AVG → ISO 27701 mapping (9 koppelingen)
- Certificering-pad (9-18 maanden, €15K-€75K)
- Cross-links: DPIA Generator, ISO 27001/27002, ISO 25010, NIS2
- 13 tests passed

### PIMS Categorien
- Privacy governance: 6 regels (policy, by design, minimalisatie, consent, rights, PIA)
- Privacy operations: 5 regels (sharing, breach, retention, accuracy, transparency)
- Controller obligations: 1 rol-specifiek
- Processor obligations: 3 rol-specifieke
- PIMS improvement: 4 regels (documentation, audit, review, continual improvement)

---

## [3.0.0] - 2026-07-17 — ISO 27002 + BIO2 Mapping

### Added
- ISO 27002 use case: 34 regels, port 8530
- 4 categorieën: Organizational, People, Physical, Technological
- BIO2 → ISO 27002 mapping (16 BIO2-maatregelen → 34 ISO controls)
- API: /bio2-mapping, /controls-by-category, /compliance-gap/{orgId}
- 11 tests passed

### Mapping
- BIO2 A.5-6 → ISO A.5.1, A.5.7, A.5.9, A.5.12
- BIO2 B.5 → ISO A.8.1, A.8.2, A.8.3, A.8.5
- BIO2 C.4 → ISO A.8.15, A.8.16

---

## [2.9.0] - 2026-07-17 — ISO 25010 Software Quality Model

### Added
- ISO 25010 use case: 35 regels, port 8529
- 9 product quality characteristics (ISO/IEC 25010:2023)
- 31 sub-characteristics met testbare regels
- API: /quality-model, /evaluate (weighted scoring), /quality-model detail
- Cross-links: inclusivity→Wdo, security→ISO 27001, recoverability→BIA-BIV-DPIA
- 19 tests passed

---

## [2.8.0] - 2026-07-17 — Wet Digitale Overheid + Gemeente Pilot

### Added
- Wet Digitale Overheid use case: 16 regels, port 8528
- Wdo Art. 1-7 + Wmebv toegankelijkheidseisen
- 7 gekoppelde frameworks (Forum Standaardisatie, BIO2, eIDAS, NORA, etc.)
- Gemeente Pilot Onboarding Flow: 8-stap workflow
  - BIA (kritieke processen) → BIV (classificatie) → Risico → DPIA → Actieplan → Rapport
  - Compliance score berekening
  - Automatische actie-generatie
- 12 pilot tests passed

---

## [2.7.0] - 2026-07-17 — ISO 27001 ISMS + SoA Generator

### Added
- ISO 27001 ISMS use case: 28 regels, port 8526
- ISMS clausules 4-10: 8 regels (scope, beleid, risicoanalyse, SoA, doelstellingen)
- Statement of Applicability generator: 14 Annex A controls + BIO2 mapping
- Asset register: 2 regels (inventaris + eigenaar)
- Risicobehandeling: 4 strategieën (accepteeren, verminderen, vermijden, overdragen)
- API: /soa/generate, /soa/template, /risico/behandeling, /isms/documenten
- 20 tests passed

### BIO2 → ISO 27001 Mapping
- BIO2 A.5-6 → A.5.1.1, A.6.1.1, A.6.1.2
- BIO2 A.8 → A.8.1, A.8.2, A.8.3
- BIO2 A.10 → A.8.24, A.8.11
- BIO2 B.3 → A.8.28, A.8.9

---

## [2.6.0] - 2026-07-17 — BIA-BIV-DPIA Integrated Risk Assessment

### Added
- BIA-BIV-DPIA use case: 32 regels, port 8524
- Business Impact Analyse: 5 regels (proces, hersteltijd, impact)
- BIV classificatie: 6 regels (beschikbaarheid, integriteit, vertrouwelijkheid)
- Risico-analyse: 6 regels (kritiek, hoog, acceptabel, residuaal)
- DPIA: 12 regels (AVG Art. 35, AP-lijst, boete, FRIA)
- Combinatie: 3 regels (integrale BIA+BIV+DPIA)
- 15 tests passed

### Wetelijke Basis
- AVG Art. 35(1)(3a)(7)(7a-f)(11): DPIA verplichting + inhoud + herziening
- AVG Art. 36(2): Voorafgaand overleg AP
- AVG Art. 25: Privacy by design
- BIO2 A.5-6: Risicoanalyse + BIA
- BIO2 A.8: Classificatie (BIV)
- NEN-ISO/IEC 27001:2017 A.8.2: BIA
- EU AI Act Art. 27: FRIA voor AI

---

## [2.5.0] - 2026-07-17 — NEDERUS v2.0 + eIDAS 2.0 Combined Release

### NEDERUS v2.0
- 8 unified controls (was 5): +NED-06 (CRA), +NED-07 (DSA), +NED-08 (AI Liability)
- 8 frameworks (was 5): +CRA, DSA, AI Liability Directive
- Tier system: priority (>=3 frameworks) + standard (>=2)
- Per-framework crosswalks (8 files: NIST, EU AI Act, BIO2, NIS2, NORA, CRA, DSA, AI Liability)
- Validation pipeline with tier classification
- Djimitflo integration artifacts (~120 lines TS)
- OpenSpec change: openspec/changes/nederus-framework-v1/

### eIDAS 2.0
- 32 rules, 21 categories, port 8523
- Full eIDAS 1.0 + 2.0 coverage
- API: wallet-status, deadlines, rapport, categorieen
- 52 tests passed

### MCP Server
- 16 tools (was 12): +nederus.list/get/crosswalk/lookup
- NEDERUS_CONTROLS v2.0 data
- eidas domain registered

---

## [2.4.1] - 2026-07-17 — eIDAS 2.0 Full Implementation

### Added
- eIDAS use case: 32 regels, 21 categorieen, port 8523
- API endpoints: wallet-status, deadlines, rapport/{orgId}, categorieen
- Agent playbook: docs/agent-playbooks/eidas.md
- Tests: 30+ test cases (JREM validation + compliance scenarios + deadline checks)
- RegelSpraak: eidas-2026.rspraak (32 regels)
- JREM schema: eidas domain + eidas-compliance procedureType toegevoegd
- Documentatie: docs/eidas-use-case.md (volledig met voorbeelden)

### eIDAS Coverage
- eIDAS 1.0: 5 vertrouwensdiensten (handtekening, zegel, tijdsstempel, ERD, website-auth)
- eIDAS 2.0: QAA, Electronic Archival, EUDI-wallet (7 regels), PID, certificering
- Grensoverschrijdende erkenning (3 regels)
- TSP-kwalificatie, trust lists, kwaliteitskeurmerken
- DPIA, security levels, private sector, implementing acts

### Correcties
- Deadline gecorrigeerd: September 2026 → December 2026
- NL wallet status: niet beschikbaar, verwacht 2027-Q1

---

## [2.4.0] - 2026-07-17 — eIDAS 2.0 Use Case v1
- RegelSpraak specificatie (eidas-2026.rspraak)
- JREM export (eidas-2026.1.json) met 20 regels, 8 categorieen
- API app met wallet-status en deadline endpoints
- 11 test cases (JREM validation + compliance scenarios)
- MCP server: eidas domain geregistreerd
- Documentatie: docs/eidas-use-case.md

### eIDAS Coverage
- eIDAS 1.0: 5 vertrouwensdiensten (handtekening, zegel, tijdsstempel, ERD, website-auth)
- eIDAS 2.0: EUDI-wallet (4 statussen), attributenuitwisseling, kwaliteitskeurmerken
- Grensoverschrijdende erkenning (eIDAS Node + wallet interoperabiliteit)
- TSP-kwalificatie en trust list publicatie

---

## [2.3.0] - 2026-07-17 — NEDERUS v2.0 Expansion

### Added
- NEDERUS v2.0: 8 controls (was 5), 8 frameworks (was 5)
- 3 new controls: NED-06 (Secure Development/CRA), NED-07 (Platform Transparency/DSA), NED-08 (AI Liability)
- 3 new frameworks: Cyber Resilience Act, Digital Services Act, AI Liability Directive
- Tier system: Priority (≥3 frameworks) + Standard (≥2 frameworks)
- NEDERUS framework matrix in README.md (8×8 visual matrix)
- MCP server: `nederus.lookup` tool (search by ID, framework, or keyword)
- MCP server: NEDERUS_CONTROLS updated to v2.0 with 8 frameworks
- Crosswalks: cra.md, dsa.md, ai-liability.md

### Changed
- Selection criteria: ≥3 → tier-based (priority/standard)
- Generator: auto-determines tier from framework count
- Validator: tier classification check + minimum framework check
- MCP server: `nederus_list_controls` uses normalized framework names

---

## [2.2.0] - 2026-07-17 — NEDERUS Multi-Jurisdictional Mapping

### Added
- NEDERUS use case in README.md met 5 unified controls (NED-01 t/m NED-05)
- Use Case Maturity tabel: NEDERUS als extern framework toegevoegd
- NEDERUS-koppeling in BIO2 use case documentatie
- NEDERUS-koppeling in EU AI Act use case documentatie
- NEDERUS-koppeling in NIS2 agent playbook
- NORA compliance matrix: NEDERUS mapping sectie
- Architectuur diagram: NEDERUS Framework als bron toegevoegd
- Validatie sectie: NEDERUS controls metriek
- Compliance Officer rol: NEDERUS Framework link

### Changed
- README.md: NEDERUS use case sectie (na AVG/GDPR, voor NCSC)
- docs/nora-compliance-matrix.md: NEDERUS mapping tabel toegevoegd
- docs/bio2-use-case.md: NEDERUS koppeling + mapping tabel
- docs/eu-ai-act-use-case.md: NEDERUS koppeling + mapping tabel
- docs/agent-playbooks/nis2.md: NEDERUS koppeling + conflict documentatie
- docs/nora-use-case.md: NEDERUS koppeling + principe mapping
- docs/judicial-ai-admission-demo.md: NEDERUS koppeling
- docs/agent-playbooks/_template.md: NEDERUS sectie template
- CONTRIBUTING.md: NEDERUS contributie richtlijnen
- mcp-server/juraregel_mcp.py: 3 NEDERUS tools (list_controls, get_control, crosswalk)

### Added
- docs/nederus-use-case.md: Dedicated NEDERUS use case documentatie
- docs/nederus-mcp-tools.md: MCP tools documentatie

---

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
