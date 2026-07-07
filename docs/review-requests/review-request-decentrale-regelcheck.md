# Jurist Review Request: Decentrale Regelcheck

## Scope

- Ruleset: `decentrale-regelcheck`
- Version: `2026.1`
- Maturity target: L1 now; optional L2 only after acceptance.
- Source snapshot: CVDR/SRU public search, UPL, TOOI/ROO.

## Review Questions

1. Is postcode plus product/activity a legally acceptable scope filter for a preflight?
2. Are open norms and multiple authorities correctly forced to manual review?
3. Are the sourceRefs sufficient for a legal reviewer to trace the local regulation?
4. Is the limitation clear enough that this is not a final legal decision?

## L2 Decision Checklist

- Scope is limited to postcode/product/activity preflight.
- `manualReviewRequired=true` is required for open norms, multiple authorities and no-match cases.
- Source references must point to public CVDR/SRU, UPL and TOOI/ROO context.
- Output must not present a final legal decision or permit/benefit outcome.

## Source Snapshot

- CVDR/SRU public search snapshot: `2026-07-07`, `https://lokaleregelgeving.overheid.nl/ZoekResultaat?count=3&locatie=1011&tekst=evenement`, live smoke count `3`.
- UPL product context snapshot: to be confirmed in the filled acceptance template.
- TOOI/ROO organisation context snapshot: to be confirmed in the filled acceptance template.

## Scenario Acceptance

- Postcode plus product/activity returns candidate local regulation and competent authority.
- Open norm or multiple matches forces manual review.
- No match is routed to manual review and is not treated as a legal rejection.

## L2 Limitations

- L2 covers preflight traceability only.
- Full local regulation interpretation remains with the competent authority or reviewer.
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
- Public CVDR search result metadata is used; full regulation interpretation remains human review.
