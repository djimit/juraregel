# ISO/IEC 27017:2026 - Level 3 evidence implementation plan

## 1. Decision

JuraRegel models ISO/IEC 27017:2026 as a non-scoring assurance profile, not as
an executable legal rule set and not as evidence of certification. The first
release is limited to the four explicit cloud-specific controls:

- 5.38 - shared roles and responsibilities within a cloud computing environment;
- 5.39 - agreement on roles and responsibilities of the cloud service partner;
- 8.35 - segregation in virtual computing environments;
- 8.36 - detection and prevention of unauthorized use of cloud services.

This is the smallest implementation that can test the strategic claim without
fabricating access to licensed guidance or organization evidence.

## 2. Research question

Can JuraRegel represent, collect and falsify evidence for the four
cloud-specific controls while preserving the distinction between:

1. an ISO control title;
2. an implementation interpretation;
3. a cross-framework relationship;
4. observed evidence;
5. an independent assessment;
6. certification?

The pilot succeeds only if these six epistemic layers remain separable in data
and output.

## 3. Claim model

| Claim class | Permitted claim | Required evidence |
|---|---|---|
| `source_fact` | Edition, publication status and control identifier | Official ISO metadata or licensed standard |
| `interpretation` | A locally defined evidence expectation | Author, rationale and explicit non-normative label |
| `mapping` | Another control supports or overlaps an ISO 27017 objective | Typed relation, rationale and review status |
| `observation` | An artifact was supplied and inspected | Immutable artifact reference, hash and timestamp |
| `assessment` | Evidence satisfies, fails or is insufficient for a local criterion | Named reviewer, date, scope and recorded reasoning |
| `certification` | An organization is ISO-certified | Accredited certification evidence; outside this pilot |

No lower claim class may be promoted automatically to a higher class.

## 4. Source hierarchy and licence boundary

1. The ISO catalogue is authoritative for publication metadata and scope.
2. A legitimately acquired ISO/NEN copy is required before normative guidance
   can be quoted, paraphrased in detail or declared complete.
3. Public framework and legislation sources can support crosswalk hypotheses,
   but do not prove ISO equivalence.
4. Local source registers record retrieval date, version and limitations.
5. Drafts, search results and vendor articles are context only.

Until a licensed copy is registered, the profile contains public control titles
and local evidence criteria only. `licensedTextAvailable` remains `false`.

## 5. Evidence model

Each control defines:

- subject and scope;
- evidence types;
- minimum artifact metadata;
- falsification criteria;
- prohibited inference;
- applicable cloud roles;
- mapping references.

An assessment finding contains:

- `status`: `satisfied`, `not_satisfied`, `insufficient_evidence` or
  `not_applicable`;
- `evidenceRefs`;
- `owner`;
- `reviewedBy`;
- `reviewedAt`;
- risk, measure and residual risk;
- rationale when not applicable.

The evaluator reports only `review-ready` or `evidence-incomplete`. It does not
calculate percentages, maturity scores or compensating totals.

## 6. Control hypotheses

### 5.38 - shared roles and responsibilities

Hypothesis: each material cloud security activity has an accountable party and
the allocation is consistent across governance records and technical reality.

Minimum evidence:

- scoped responsibility matrix;
- named customer, provider and partner roles;
- ownership of IAM, patching, logging, backup, incident response and keys;
- technical sample showing that assigned permissions match the matrix;
- review and exception history.

Falsified by an unassigned activity, contradictory artifacts, an accountable
role without authority, or a technical configuration that contradicts the
matrix.

### 5.39 - agreement with cloud service partners

Hypothesis: allocated responsibilities are agreed with each relevant cloud
service partner and remain governable through the service lifecycle.

Minimum evidence:

- signed agreement and SLA;
- security and privacy terms where applicable;
- incident notification and cooperation terms;
- subprocessor or supply-chain visibility;
- audit and evidence-access rights;
- data return, deletion, portability and exit terms;
- ownership of cryptographic keys and material AI assets where applicable.

Falsified by missing agreement, conflict with the responsibility matrix,
unbounded subcontracting, absent audit access or an unexecutable exit.

### 8.35 - segregation in virtual computing environments

Hypothesis: tenants, trust zones and lifecycle environments are isolated
according to a documented threat model and tested boundaries.

Minimum evidence:

- architecture and trust-boundary model;
- identity and privilege separation;
- network and workload isolation policy;
- secrets and key separation;
- development/test/production separation;
- negative tests demonstrating blocked cross-boundary access;
- exception register and remediation evidence.

Falsified by unauthorized cross-tenant or cross-environment access, shared
privileged identity without compensating evidence, or an untested boundary.

### 8.36 - unauthorized use of cloud services

Hypothesis: the organization can identify material cloud use, distinguish
authorized from unauthorized use and respond proportionately.

Minimum evidence:

- cloud and SaaS service inventory;
- authorization policy and owner;
- discovery evidence from relevant identity, network, endpoint, expense or
  procurement sources;
- triage and exception workflow;
- response evidence and recurring coverage review;
- explicit coverage of AI services, agents, MCP servers and API credentials
  where these are in scope.

Falsified by a material discovered service absent from inventory, unknown
ownership, no response path or detection blind spots presented as full coverage.

No specific CASB, CSPM, SSPM or vendor product is mandatory in this model.

## 7. Crosswalk method

Mappings use only these relation types:

- `supports`: evidence for the target can support the source control;
- `overlaps`: objectives intersect but neither proves the other;
- `evidence_reusable`: a named artifact can be reused after scope validation;
- `no_equivalence`: the relationship must not be used as a substitution;
- `applicability_requires_review`: legal or sector scope needs human review.

Every mapping includes a rationale and remains `reviewStatus: draft` until an
independent domain reviewer accepts it. NIST CSF, BIO2, NIS2, DORA and the EU AI
Act are not represented as interchangeable requirements.

## 8. Implementation phases and proof gates

### Phase A - repair the foundation

- Correct BIO2 ISO 27002 references to the ISO 27002 source.
- Classify those references as standards, not legislation.
- Add source-version anchors to BIO2 and ISO 27002 references.
- Remove the unsupported 85% compliance inference from the ISO 27002 API.

Gate: focused tests pass and source-quality debt decreases by the exact number
of repaired references.

### Phase B - build the pilot profile

- Register official ISO metadata and the licence limitation.
- Encode four public control titles and local evidence hypotheses.
- Add the typed crosswalk.
- Add a JuraRegel self-assessment.
- Reuse the existing non-scoring evidence evaluator.

Gate: four unique controls, zero score fields, all mapping targets resolve and
the self-assessment fails closed.

### Phase C - validate

- Run focused ISO 27002, BIO2, AcICT and ISO 27017 tests.
- Run source-quality and schema validation.
- Run the canonical repository gate.
- Record unrelated pre-existing failures without weakening the new gate.

Gate: no new blocking debt and deterministic assessment output.

## 9. Deferred work and activation criteria

| Deferred item | Add only when |
|---|---|
| Licensed normative guidance | A valid ISO/NEN licence and controlled source copy exist |
| Kubernetes/OpenShift adapter | A real target cluster, permission boundary and expected evidence contract are approved |
| Azure/AWS adapter | A read-only tenant scope and data-handling approval exist |
| Contract NLP | A labelled contract corpus and legal reviewer acceptance criteria exist |
| Shadow-cloud discovery adapter | An authorized telemetry source and coverage statement exist |
| Dashboard | At least one independently reviewed assessment needs recurring comparison |
| Certification claim | Accredited certification evidence is supplied |

## 10. Residual validity threats

- Public metadata cannot establish completeness of licensed guidance.
- Crosswalks are analytical hypotheses until independently reviewed.
- Repository evidence describes JuraRegel development, not IVO Rechtspraak's
  operational hybrid-cloud environment.
- Absence of detected unauthorized cloud use is not evidence of absence.
- Tool output cannot replace management acceptance of residual risk.

The correct pilot outcome is therefore expected to be
`evidence-incomplete`, not compliant.
