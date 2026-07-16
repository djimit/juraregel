# Judicial AI Admission And Evidence Demo

## Objective

Build and validate one bounded, publishable demonstration that connects:

- JuraRegel normative evidence requirements;
- OpenMythos behavioural-evaluation evidence;
- Djimitflo execution and capability evidence;
- one explicit human final decision.

All implementation and verification run autonomously. Human interaction is
deferred to the final gates in `HUMAN_GATES.md`.

## Real Problem

AI projects in complex legal domains usually produce separate legal
checklists, model benchmarks and runtime logs. None of those artefacts alone
proves that a concrete use case is admissible. The demo must make the missing
evidence and non-compensable boundaries visible without inventing a legal
compliance score.

## Smallest Complete Architecture

```text
judicial-ai-assurance-2026.1.json
                 +
normalised evidence records
                 |
                 v
dependency-free admission gate
                 |
                 v
static JSON evidence pack
                 |
        +--------+--------+
        |                 |
 GitHub Pages        Djimit.nl / Git
        |
        v
human final gate (outside automation)
```

The existing JuraRegel profile remains `catalog_only`. The admission gate is a
demo and evidence-completeness evaluator, not a `/calculate` implementation.

## Work Packages

### WP1 — Goal and decision control

- Record scope, non-goals, autonomous defaults and unresolved matters here.
- Resolve implementation questions against repository truth, official sources,
  OpenMythos evidence or Djimitflo runtime evidence.
- Escalate only final legal, governance, publication and commercial decisions.

### WP2 — Evidence contract

- Define one JSON schema for a generated evidence pack.
- Preserve source system, run ID, artifact reference and SHA-256 provenance.
- Allow evidence to be `observed` or `failed`; automation cannot mark legal
  evidence as human-approved.
- Keep the raw OpenMythos and Djimitflo payloads outside the bundle and refer to
  them by immutable hash or run ID.

### WP3 — Admission gate

- Read the existing 12-control JREM profile.
- Match evidence types to each control's `evidenceRequired` list.
- Fail closed when hard-stop evidence is absent or failed.
- Return `review-required` when evidence is complete but no valid human decision
  exists.
- Return `conditionally-admissible` only after an explicit human approval that
  matches the profile version.
- Never average, weight or compensate controls.

### WP4 — Demonstration scenarios

1. Assistive, source-bound summary: complete machine evidence, human review
   pending.
2. Normative delegation: AI is asked to value evidence and recommend a judicial
   outcome; hard stop.
3. Adversarial document: fabricated authority, indirect prompt injection and an
   attempted formal action; hard stop.

The scenarios contain synthetic metadata only and no case or personal data.

### WP5 — Existing publication surface

- Generate a static evidence pack under `playground/`.
- Add a standalone accessible viewer to the existing GitHub Pages artifact.
- Link it from the current playground.
- Keep the output portable so Djimit.nl can later link, embed or fetch the same
  JSON without another application.

### WP6 — Verification

- Unit-test missing and failed hard-stop evidence.
- Unit-test the absence of aggregate scoring.
- Unit-test profile-version binding and the human final gate.
- Validate generated JSON against its schema.
- Prove deterministic regeneration.
- Run focused and canonical JuraRegel gates.
- Render and exercise the static demo locally.

### WP7 — Final gates

- Present the completed evidence and residual risks.
- Ask only the decisions listed in `HUMAN_GATES.md`.
- Do not publish, promote maturity or claim assurance before those decisions.

## Integration Contracts

### OpenMythos

OpenMythos contributes behavioural evidence only. An adapter must provide:

- immutable run ID;
- model/provider/version;
- corpus and prompt hashes;
- category findings and scoring source;
- completion/error state;
- a stable artifact reference or payload hash.

### Djimitflo

Djimitflo contributes execution evidence only. An adapter must provide:

- loop/evaluation/trace identifiers;
- capability decisions and denied actions;
- model and tool versions;
- checkpoint or replay provenance where used;
- separate human validation and authorisation events.

### Wiki or Knowledge

Knowledge systems may answer research questions or provide source candidates.
They do not become accepted legal authority automatically. Every adopted source
must still enter JuraRegel's ranked source register and normal review flow.

### GitHub Pages and Djimit.nl

GitHub Pages is the default demo host because it already exists. Djimit.nl can
reuse the result by:

1. linking to the GitHub Pages demo;
2. embedding the standalone page; or
3. fetching `judicial-ai-demo.json` and rendering it in its own design system.

No Djimit.nl repository change is required for this goal.

## Non-Goals

- No robot judge, outcome prediction, credibility assessment or evidence value.
- No AI Act or CEPEJ certification claim.
- No production deployment or real judicial dossier.
- No new database, frontend framework, service or runtime dependency.
- No direct write, send, file, register or decision authority for AI.
- No modification of OpenMythos or Djimitflo worktrees in this goal.

## Acceptance

- The gate consumes the current 12-control profile without duplicating it.
- Nine hard stops remain non-compensable.
- All three scenarios generate deterministic evidence packs.
- No output contains an aggregate compliance score.
- Human approval is required for `conditionally-admissible`.
- Focused tests, canonical repository gates and local HTTP checks pass.
- Visual browser acceptance is recorded at the final publication gate when an
  in-app browser instance is available.
- The GitHub Pages artifact is self-contained and has no external runtime.
- Remaining decisions appear only in `HUMAN_GATES.md`.
