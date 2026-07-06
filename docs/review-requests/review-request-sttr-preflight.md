# Jurist Review Request: STTR Preflight

## Scope

- Ruleset: `sttr-preflight`
- Version: `2026.1`
- Maturity target: L1 now; optional L2 only after acceptance.
- Source snapshot: IPLO STTR/IMTR public version page and local package metadata.

## Review Questions

1. Are supported STTR/IMTR versions interpreted correctly for a preflight?
2. Is missing RTR version a blocking delivery issue?
3. Is missing `jremMapping.mappedRuleIds` a valid blocker for JuraRegel traceability?
4. Are the limits clear that this is not a full DSO/RTR submission or XSD validation?

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
- Full STTR XSD validation, verificatiematrix execution and DSO/RTR submission are out of scope.
