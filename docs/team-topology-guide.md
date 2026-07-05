# JuraRegel in Scaled Agile — Team Topology Guide

## Team Topologies (Skelton & Pais) + JuraRegel

### Stream-aligned teams
**Wat ze doen**: Features bouwen voor een specifiek domein (bijv. zaakintake, belastingaangifte).

**Hoe ze JuraRegel gebruiken**:
- Consumeren Rule APIs via TypeScript SDK: `npm install @juraregel/sdk`
- Checken compliance in CI: `npx juraregel check <domein>`
- Genereren database constraints: `GET /v1/traceability/matrix` → DB CHECK constraints
- Tracken compliance debt: `GET /v1/debt/<team>`

### Platform teams
**Wat ze doen**: Beheren gedeelde platformen (bijv. zaaksysteem, API gateway).

**Hoe ze JuraRegel gebruiken**:
- Beheren JuraRegel Rule APIs (Docker, Helm, monitoring)
- Beheren JREM Registry (Git-versioned)
- Runnen CI gates voor alle use cases
- Beheren de traceability matrix

### Enabling teams
**Wat ze doen**: Helpen andere teams met adoptie en verbetering.

**Hoe ze JuraRegel gebruiken**:
- Onboarden nieuwe teams: `npx juraregel init <domein> <port>`
- Trainen jurists in RegelSpraak CNL
- Begeleiden Rule Extraction Sprints
- Verzamelen evidence voor audits: `GET /v1/traceability/matrix`

### Complicated subsystem teams
**Wat ze doen**: Bouwen en beheren complexe subsystemen.

**Hoe ze JuraRegel gebruiken**:
- Pseudonimiseringsrichtlijn engine V4.2 (use case publicatie)
- Algoritmeregister compliance engine
- RegelSpraak → JREM generatie (toekomstig: ALEF/MPS)

## Wet → Code → Database keten

```
Wet/Regelgeving (wetten.overheid.nl)
  ↓ Rule Extraction Sprint (1-4 weken)
RegelSpraak CNL (leesbaar door jurist)
  ↓ Vertaling
JREM (JSON Schema 2020-12, bronverwijzingen)
  ↓ API factory pattern
Rule API (FastAPI, stateless, auditable)
  ↓ Traceability engine
Database CHECK constraint (SQL)
  ↓ Pydantic validator (application level)
Data persistence (database)
  ↓ CI gates + tests
Verification (14 gates, 370+ tests)
  ↓ Audit trail (inputHash + rulesetHash)
Audit evidence (jaarlijkse audit, ENSIA, AP)
```

## Scaled Agile ceremonies + JuraRegel

| Ceremony | JuraRegel product | Waarde |
|---|---|---|
| PI Planning | Regulatory Impact Analyzer | Wet wijzigingen in komende PI |
| Sprint Planning | Compliance Debt Tracker | Onuitgevoerde regels in sprint |
| Daily Standup | Traceability Matrix | Welke regels werken we aan? |
| Sprint Review | Evidence Collector | Bewijs dat regels zijn geïmplementeerd |
| Sprint Retrospective | Compliance Debt burn-down | Verbetering in compliance dekking |
| System Demo | Playground + Dashboard | Live demonstratie van rule compliance |

## Functiehuis Rijksoverheid mapping

| Functiehuis rol | Team type | JuraRegel product |
|---|---|---|
| Software Ontwikkelaar | Stream-aligned | SDK, CLI, OpenAPI, code examples |
| Solution Architect | Enabling | NORA matrix, ADR template, traceability |
| Security Expert | Complicated subsystem | NCSC, BIO2, threat model |
| DevOps Engineer | Platform | Docker, Helm, GitHub Actions, SRE toolkit |
| Compliance Officer | Enabling | Compliance debt, evidence collector, ENSIA |
| CISO | Platform | Executive dashboard, multi-framework matrix |
| Jurist | Enabling | RegelSpraak CNL, acceptatie protocol |
| Product Owner | Stream-aligned | User story template, ROI calculator |
| Data Engineer | Stream-aligned | DB constraint generator, DCAT-AP-NL |
| AI Engineer | Complicated subsystem | EU AI Act, algoritmeregister |
