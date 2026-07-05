# Changelog

## v1.0.0 — 2026-07-04

### Added
- 10 use cases: griffierecht, procesreglement, classificatie, publicatie/PII, BIO2, Forum Standaardisatie, Overheidsstandaarden, NORA, EU AI Act, AVG/GDPR
- 291 JREM regels across 7 domeinen
- 207 tests (all passing)
- 14 CI gates per use case
- Pseudonimiseringsrichtlijn engine V4.2 (100% precision on 25.127 decisions)
- TypeScript SDK (@juraregel/sdk) with typed clients for all 10 APIs
- JuraRegel CLI (npx juraregel init/check/serve/validate)
- Docker compose (10 services, ports 8490-8499)
- GitHub Actions reusable workflow
- Interactive dashboard with live health checks
- JREM open standard (MIT, JSON Schema 2020-12)
- Whitepaper "Legal RuleOps: From PDFs to APIs"
- NORA compliance matrix (Mermaid diagram)
- CONTRIBUTING.md with use case template
- OpenAPI 3.0 specs for all 10 Rule APIs
- 8 use case documentation files with Agile user stories

### Validated
- Pseudonimisering: 100% on full 25.127 decision dataset (48.702 detections)
- BIO2: 162 maatregelen from MinBZK GitHub, ISO 27002 linked
- Forum Standaardisatie: 22 standaarden (16 verplicht + 6 streefbeeld)
- Open standaarden: 7 compliant (pseudonimiseringsrichtlijn, AVG/GDPR, JSON Schema, MIT, ECLI, BWBR)
- Djimitflo: 189 LROP entries, 13 learning cycles, 9 reflections

## v1.1.0 — 2026-07-05

### Changed
- 4 PoC use cases upgraded to Production:
  - Procesreglement: 4 → 20 regels
  - Classificatie: 3 → 15 regels
  - EU AI Act: 12 → 25 regels
  - AVG/GDPR: 10 → 25 regels

### Added
- 5 new use cases: NIS2 (15 regels), btw-tarieven (10), WW-uitkering (15), IND verblijfsregels (15), Wmo (10)
- Total: 16 use cases, 444 regels, 279 tests, 10 domeinen
- All use cases: Production status, accepted, CI gates PASS
