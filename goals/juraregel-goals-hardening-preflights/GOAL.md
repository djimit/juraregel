# JuraRegel Goals Hardening And Preflights

## Objective

Execute OpenSpec change `juraregel-goals-hardening-preflights` autonomously.

## Scope

- Gate 4 jurist-acceptatie readiness.
- Source health cleanup for BWB, PLOOI and Rechtspraak.
- BWB sourceRef traceability cleanup.
- `decentrale-regelcheck`.
- `woo-publicatieplicht-preflight`.
- `sttr-preflight`.

## Non-Goals

- No production-ready claim without real jurist-acceptatie metadata.
- No new vector database, orchestration layer, UI or DSO clone.
- No private document ingestion.
- No human prompts until final gates.

## Acceptance

- Focused tests pass.
- Full pytest passes.
- All JREM exports validate against `shared/jrem-schema.json`.
- JKB check passes.
- CI JREM validator passes.
- Scheduler health has actionable statuses.
- OpenSpec strict validation passes.
