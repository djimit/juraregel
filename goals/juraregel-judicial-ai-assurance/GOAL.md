# JuraRegel Judicial AI Assurance Goal

## Objective

Build the first bounded JuraRegel addition for judicial AI assurance:

- a source-ranked, catalog-only JREM profile for AI used in or around adjudication;
- non-compensable constitutional control points;
- explicit composition with existing JuraRegel domains instead of duplicated AI Act, privacy, DPIA or traceability rules;
- verifiable source lineage and focused contract tests;
- all human interaction deferred to the end of the build.

## Real Problem

The profile must answer which evidence is required before a judicial AI use case may proceed. It must not calculate a legal approval score, automate a judicial decision or present CEPEJ country examples as binding norms.

## Build Slice

1. Register `judicial-ai-assurance` as a JREM domain and procedure type.
2. Add a versioned source register with five authority classes:
   `binding-law`, `treaty-framework`, `authoritative-soft-law`,
   `implementation-method`, and `context-only`.
3. Add twelve assurance controls covering subsidiarity, legal openness, judicial authority, non-binding output, procedural fairness, source lineage, impact assessment, public control, evaluation, security, formal action authority and professional competence.
4. Mark constitutional controls as `hard-stop`; they may never be averaged into a passing score.
5. Expose the profile through the existing catalog-only API and MCP registry.
6. Prove schema validity, source quality, source-class use, hard-stop behavior and the absence of calculate capability.

## Architecture Boundary

```text
JuraRegel                    OpenMythos                 Djimitflo
normative controls          behavioural evidence      execution evidence
source authority            adversarial scenarios     traces/checkpoints
legal/manual gates          failure observations      capability enforcement
```

This slice only builds the JuraRegel column and the evidence contract expected from the other two systems. It does not add either system as a runtime dependency.

## Boundaries

- Catalog-only: no calculation engine, aggregate score or automated approval.
- No AI-generated legal interpretation is stored as accepted law.
- No direct write, send, filing or decision authority for an AI system.
- Existing domains remain the source of AI Act, privacy, DPIA, registry and traceability controls.
- Country presentations remain `context-only` and cannot justify a control by themselves.
- No production status, publication, commit or push without an end-gate decision.

## Success Criteria

- The JREM export validates against the shared schema.
- Every control has dated, section-level official source references.
- Every referenced source is classified in the source register.
- All hard-stop controls require human legal review and use `block-until-evidence`.
- The API reports `calculate=false` and returns `409 catalog_only` for calculation.
- Focused and canonical repository gates pass.
- Remaining human decisions are listed only after autonomous validation.

## Human Gates At End

1. Jurist review of source interpretation and hard-stop wording.
2. Judicial-governance approval of the profile boundary.
3. Decide whether to commit and push.
4. Decide whether a later integration with OpenMythos and Djimitflo may proceed.
