# Jurist Review Request: Woo Publicatieplicht Preflight

## Scope

- Ruleset: `woo-publicatieplicht-preflight`
- Version: `2026.1`
- Maturity target: L1 now; optional L2 only after acceptance.
- Source snapshot: Woo-index public search and organisation detail pages, DiWoo metadata expectations, TOOI/ROO.

## Review Questions

1. Are Woo information categories and publication locations sufficient for a metadata preflight?
2. Which metadata fields are legally mandatory before publication?
3. Is it correct that missing `tooiCode`, `publishedAt` or `sourceUrl` triggers manual review?
4. Does the implementation correctly avoid ingesting document bodies or private content?

## Required Acceptance Metadata

- `geaccondeerdDoor`
- `rol`
- `organisatie`
- `datum`
- `geldigTot`
- `versie`
- `scope`
- `bronSnapshot`
- `verklaring`
- `beperkingen`

## Current Blockers

- No independent jurist acceptance.
- Public Woo-index pages do not always expose `tooiCode` or `publishedAt`; missing fields stay blockers/manual review.
