# JuraRegel Live Harvesters And Production Readiness

Execute OpenSpec change `juraregel-live-harvesters-production-readiness`.

## Objective

Build the live read-only source layer for:

1. CVDR/SRU into `decentrale-regelcheck`.
2. Woo-index/DiWoo into `woo-publicatieplicht-preflight`.
3. STTR/IMTR/RTR into `sttr-preflight`.
4. Production-readiness last: jurist acceptance metadata, L2/L3 gates, L3 disclaimers and trust report.

## Constraints

- Public read-only sources first.
- No authenticated endpoints until final human gate.
- No private Woo document content ingestion.
- No new database, crawler framework or orchestration layer.
- L2/L3 production status requires explicit jurist acceptance metadata.
- All human interactions are deferred to final gates.

## Acceptance

- OpenSpec strict validation passes.
- Focused tests and repo-wide pytest pass.
- JKB check passes.
- JREM validation passes.
- Pilot legal-review gate passes.
- Scheduler/source health has actionable `ok` or `degraded` statuses.
- Trust report states real readiness and unresolved human gates.
