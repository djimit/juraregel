# JuraRegel repository and ecosystem evidence audit

**Date:** 2026-07-30
**Scope:** JuraRegel Git checkout, all repository Markdown, the local
OpenMythos benchmark checkout and the local Djimitflo checkout/database
**Conclusion:** implementation present; external integration
`evidence-incomplete`

## 1. Research question

Which claims in JuraRegel describe executable and reproducible behaviour, which
describe static mappings or prototypes, and which remain plans or unsupported
empirical claims?

The unit of analysis is a claim, not a file. A claim is accepted only when its
subject, version, observation method, evidence artifact, falsification
condition and validity boundary can be identified.

## 2. Method

The audit used three independent passes:

1. **Documentation pass:** 213 Markdown files and 26,405 lines were scanned for
   relative links, implementation language, status claims, counts and
   reproducibility instructions.
2. **Code and gate pass:** APIs, assurance modules, root tests, use-case tests,
   CI selection and the canonical gate were compared. Negative probes tested
   whether fail-closed and integration claims could be falsified.
3. **Ecosystem pass:** the actual OpenMythos corpus and validation scripts were
   executed; the actual Djimitflo Git checkout and SQLite schema/data were
   inspected read-only.

Historical documents, strategy documents and publication drafts were not
treated as current runtime evidence. Passing unit tests was treated as evidence
for the tested contract only, never as evidence of legal compliance or live
external integration.

## 3. Observations

### 3.1 OpenMythos

- Commit: `a3ed65a9dd24bb1a275d1213e65f625a6385e75c`.
- Corpus SHA-256:
  `71ca62e742f71c2830f198c01dbcacdcf75487b9ef96e661d3e297d6608d41b9`.
- `351/351` corpus cases validate.
- The corpus contains 11 categories.
- The skill-lifecycle gate validates 18 draft cases across six stages; none are
  promoted.

The prior JuraRegel validator used 18 locally declared categories. It omitted
two observed categories (`canary`, `overthinking`) and counted nine local
extensions as if they were observed OpenMythos categories. Its 100% coverage
was therefore internally tautological rather than an external validation.

### 3.2 Djimitflo

- Commit: `cb9944fffe47e07e648a302d1d520406125fe880`.
- The checkout is dirty and was not modified.
- The inspected local database contains the OpenMythos run/result schema but
  zero persisted OpenMythos evaluation runs and zero case results.
- No external NEDERUS control catalog was located in the inspected checkout.
- The JuraRegel `DjimitfloBridge` accumulates objects in process memory; it does
  not call the configured Djimitflo API or persist records.

Consequently, a static NEDERUS mapping and an in-memory adapter cannot support
a claim of live Djimitflo integration.

### 3.3 JuraRegel documentation and gates

- Eight broken internal Markdown links existed in imported `.opencode` skills.
- The canonical local gate omitted `api/test_*.py` and `tests/test_*.py`, even
  though those directories contain the JLAIF and ecosystem-integration tests.
- The separate GitHub `JLAIF Assurance Gates` workflow was red on recent
  dependency branches because its Ruff surface contained unresolved lint debt.
- The continuous-evaluation engine returned success from hardcoded lambdas for
  23 checks and tested configuration only for the remaining check. Its Grade A
  output was therefore self-reference, not observed performance.
- The ISO/AcICT evaluator could promote `insufficient_evidence` to
  `review-ready` when reviewer metadata was added.
- The ISO 27017 plan required structured subject, scope, artifact metadata,
  applicable roles and mapping references that were absent from the profile.
- Publication drafts used precise OpenMythos grades and audit totals without a
  versioned empirical result artifact.

## 4. Implemented corrections

1. `insufficient_evidence` is now intrinsically incomplete; risk, measure,
   residual risk, ownership and review metadata are validated.
2. The ISO 27017 profile now implements its documented evidence fields and
   resolves profile mapping references through unique mapping IDs.
3. The canonical local and GitHub gates execute root/API tests and a
   repository-wide Markdown-link gate.
4. Missing repository engineering instructions were added and optional
   unavailable skill links were made non-linking.
5. A versioned ecosystem evidence snapshot records the observed OpenMythos,
   Djimitflo and JuraRegel state.
6. The integration validator covers the 11 observed OpenMythos categories,
   distinguishes mapping coverage from operational evidence, and returns
   `evidence-incomplete` while Djimitflo has no persisted run and the bridge is
   in-memory only.
7. Current README claims were corrected; historical publications now carry
   explicit reproducibility warnings.
8. Hardcoded continuous-evaluation success was removed; all criteria now fail
   closed until independently reviewable runtime evidence is supplied.
9. The exact JLAIF Ruff and assurance workflow surfaces pass locally.
10. Production startup now rejects absent identity, persistence, vector-store,
    CORS and ingress-rate-limit boundaries; unsigned tokens and embedded test
    credentials were removed.
11. Readiness actively probes PostgreSQL and Qdrant; production startup no
    longer creates database tables, and the API image runs as a non-root user.
12. A non-scoring enterprise-readiness gate separates repository gaps from
    external legal, normative, ecosystem and operations evidence.

The detailed issue-to-proof model, promotion policy and remaining external
gates are specified in the
[enterprise-grade level-3 plan](../enterprise-grade-level3-plan.md).

## 5. Detailed implementation plan

### Phase 1 — epistemic repair

**Objective:** prevent metadata, mappings or self-checks from being promoted to
external assurance.

Proof gates:

- an `insufficient_evidence` negative probe never returns `review-ready`;
- observed categories come from a versioned evidence artifact;
- mapping coverage and operational integration status are separate outputs.

### Phase 2 — documentation as contract

**Objective:** make broken local references and omitted test surfaces blocking.

Proof gates:

- every relative link in every repository Markdown file resolves;
- root/API tests run in the canonical local and GitHub gates;
- the GitHub JLAIF lint, regression, challenge, drift and canary commands pass
  on the same source;
- current-status documents link to the evidence snapshot;
- historical/vision documents cannot be mistaken for current attestations.

### Phase 3 — operational integration

**Objective:** move from `evidence-incomplete` to observed integration without
fabricating production evidence.

Activation criteria:

1. approve a Djimitflo target instance and credential boundary;
2. implement one authenticated, idempotent task/audit-event transport;
3. persist an OpenMythos run and case-result lineage in Djimitflo;
4. record request/response hashes, source commit, corpus hash and timestamps;
5. run failure, replay and partial-write tests;
6. independently review NEDERUS applicability and identifiers.

This phase is deliberately not auto-activated against a dirty local checkout or
an unapproved runtime because it would create external state and convert an
audit into a deployment.

## 6. Validity threats and residual work

- The ecosystem snapshot is a dated observation, not continuous monitoring.
- OpenMythos corpus validity does not prove model quality.
- A populated Djimitflo table would prove persistence, not legal adequacy.
- Static code-pattern scanning has construct-validity limits and must not be
  reported as benchmark performance.
- Historical numerical claims require their original case-level datasets and
  analysis scripts before they can be reinstated as empirical results.
- Licensed ISO text and independent ISO review remain outside repository scope.

The correct current system-level conclusion is therefore:

> JuraRegel has executable assurance prototypes and reproducible repository
> gates. OpenMythos mapping coverage is complete for the observed corpus
> categories, but live OpenMythos-to-Djimitflo operational evidence is absent.
> The integration remains `evidence-incomplete`.
