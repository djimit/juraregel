# JuraRegel Source Expansion Preflights Goal

## Objective

Execute the autonomous part of OpenSpec change `juraregel-source-expansion-preflights`:

- add public source connectors for UPL and TOOI/ROO;
- add a minimal `dienstverlening-check` use case;
- capture follow-up source preflights as design notes;
- leave human gates for the end.

## Boundaries

- No git commit or push without explicit approval.
- No authenticated API keys.
- No production publication.
- No generic AI extractor.
- No new vector database, orchestration layer or UI.
- L4/open discretionary norms return `manualReviewRequired=true`.

## Success Criteria

- `UPLConnector` returns fixture-backed product records with sourceRefs.
- `TOOIROOConnector` returns fixture-backed organisation records with sourceRefs.
- `dienstverlening-check` has 8-12 L1 rules, valid JREM and focused tests.
- OpenSpec tasks reflect completed autonomous work and remaining human gates.
- `openspec validate juraregel-source-expansion-preflights --strict` passes.

## Human Gates At End

1. Decide whether to commit and push.
2. Decide whether to use authenticated API endpoints.
3. Jurist-acceptatie before production-ready status.
4. Publication approval for external machine-readable reports.
