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

## L2 Decision Checklist

- Scope is limited to Woo/DiWoo metadata preflight.
- Missing `tooiCode`, `publishedAt`, `sourceUrl`, organisation or documenttype remains blocking/manual review.
- Source references must point to public Woo-index, DiWoo and TOOI/ROO context.
- Implementation must not ingest document bodies, private content or non-public locations.

## Source Snapshot

- Woo-index public page snapshot: `2026-07-07`, `https://organisaties.overheid.nl/woo/zoeken?keyword=Amsterdam&maximumRecords=5&pageNumber=1&sortOrder=0`, live smoke count `5`.
- DiWoo metadata expectation snapshot: to be confirmed in the filled acceptance template.
- TOOI/ROO organisation context snapshot: to be confirmed in the filled acceptance template.

## Scenario Acceptance

- Organisation plus documenttype resolves to candidate publication location.
- Missing required metadata blocks the preflight.
- Preflight uses metadata only and does not process document bodies.

## L2 Limitations

- L2 covers publication metadata checks only.
- The preflight is not an information-law decision and does not approve document content.
- No L2 promotion is allowed until the acceptance template is filled with real jurist metadata.

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
