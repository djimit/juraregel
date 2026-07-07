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

## L2 Decision Checklist

- Scope is limited to STTR/IMTR/RTR package metadata and JREM traceability preflight.
- Non-current STTR version, missing RTR version and missing JREM mapping remain blockers/manual review.
- Source references must point to the public IPLO STTR/IMTR context and local package metadata.
- Output must not claim full DSO/RTR submission, XSD validation or verificatiematrix execution.

## Source Snapshot

- IPLO STTR/IMTR public version page snapshot: `2026-07-07`, `https://iplo.nl/digitaal-stelsel/aansluiten/standaarden/sttr-imtr/`, live smoke supported versions `3.0`, `2.0`, `1.5`.
- Local package metadata snapshot: `__PACKAGE_METADATA_CHECKED_AT_YYYY-MM-DD__`.

## Scenario Acceptance

- Current STTR/IMTR version is accepted for preflight.
- Missing RTR version or JREM mapping blocks the preflight.
- Result remains a metadata preflight and not a formal DSO/RTR validation result.

## L2 Limitations

- L2 covers package metadata and mapping traceability only.
- Full STTR XSD validation, verificatiematrix execution and DSO/RTR submission remain out of scope.
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
- Full STTR XSD validation, verificatiematrix execution and DSO/RTR submission are out of scope.
