# Design

## Architecture Overview

NEDERUS is a **data product**, not a software product. The core deliverable is a
versioned, machine-readable mapping between 5 AI governance frameworks. Downstream
consumers (Djimitflo, advisory teams, client organizations) parse this data.

```
┌─────────────────────────────────────────────────────┐
│                  NEDERUS Repository                   │
│                                                       │
│  controls.yaml  ←── JSON Schema ──→  Validation      │
│  mapping-matrix.csv                                  │
│  crosswalks/{eu-ai-act,bio2,nis2,nora,nist-rmf}.md │
│  GOVERNANCE.md                                       │
│  CHANGELOG.md                                        │
└──────────────┬──────────────────────────────────────┘
               │ consumed by
       ┌───────┼───────┐
       ▼       ▼       ▼
  Djimitflo  Blogpost  Advisory
  (TS loader) (human)  (human)
```

## Ownership

- **Framework owner**: DjimIT B.V. (Dennis Landman as initial maintainer)
- **License**: CC-BY 4.0 (open, attribution required)
- **Governance model**: Benevolent dictator with community contributions
- **Release cadence**: Quarterly (v1.0, v1.1, v1.2, v2.0 per year)

## The 5 v1.0 Controls

Selected because they appear in ≥3 of 5 frameworks (highest overlap, highest value)
AND are actionable + auditable. Controls covering all 5 frameworks (NED-01, NED-05)
are prioritized over controls covering 3 (NED-02, NED-03, NED-04). Gaps in BIO2/NIS2
for NED-02/03/04 are intentional — these frameworks address bias/oversight/transparency
at the organizational policy level, not per-AI-system.

| ID | Control | NIST RMF | EU AI Act | BIO2 | NIS2 | NORA |
|----|---------|----------|-----------|------|------|------|
| NED-01 | AI Impact Assessment | MAP | Art. 9(2), FRIA Art. 27 | A.5-6 | Art. 21 | Grondslag-toets |
| NED-02 | Bias & Fairness Testing | MAP + MEASURE | Art. 10 | — | — | Evenredigheid |
| NED-03 | Human Oversight | GOVERN + MANAGE | Art. 14 | — | — | Proportionaliteit |
| NED-04 | Transparency & Explainability | MEASURE | Art. 13, Art. 50 | — | — | Openbaarheid |
| NED-05 | Incident Response & Reporting | MANAGE | Art. 72 | C.6-7 | Art. 23 | — |

**Selection criteria:**
1. Appears in ≥3 of 5 frameworks (proven overlap)
2. Actionable (organization can implement it)
3. Auditable (evidence can be produced)
4. Non-trivial (not just "have a policy")

## Data Format: controls.yaml

```yaml
version: "1.0.0"
last_updated: "2026-07-17"
frameworks:
  nist_ai_rmf: "1.0"
  eu_ai_act: "2024/1689"
  bio2: "2.2"
  nis2: "2022/2555"
  nora: "2.0"

controls:
  - id: NED-01
    title: AI Impact Assessment
    description: Conduct and document impact assessments before deploying AI systems
    severity: high
    frameworks:
      nist_ai_rmf:
        function: MAP
        reference: "MAP-1.1: Identify and assess risks"
        relation: equivalent
      eu_ai_act:
        reference: "Art. 9(2), Art. 27"
        relation: equivalent
      bio2:
        reference: "A.5-6"
        relation: partial
      nis2:
        reference: "Art. 21"
        relation: partial
      nora:
        reference: "Grondslag-toets"
        relation: partial
    evidence_required:
      - Documented impact assessment
      - Risk classification per EU AI Act Art. 6
      - Stakeholder sign-off
    implementation_guidance: |
      Use the unified NEDERUS Impact Assessment template. Map results to each
      framework's specific reporting format using the crosswalk documentation.
```

## Data Format: mapping-matrix.csv

```csv
control_id,control_title,nist_function,nist_ref,eu_article,bio2_ref,nis2_article,nora_ref,coverage
NED-01,AI Impact Assessment,MAP,MAP-1.1,"Art. 9(2), Art. 27",A.5-6,Art. 21,Grondslag-toets,full
NED-02,Bias & Fairness Testing,MAP+MEASURE,MAP-2.3+MEASURE-1.2,Art. 10,,,Evenredigheid,partial
NED-03,Human Oversight,GOVERN+MANAGE,GOVERN-1.4+MANAGE-2.1,Art. 14,,,Proportionaliteit,partial
NED-04,Transparency & Explainability,MEASURE,MEASURE-1.3,"Art. 13, Art. 50",,,Openbaarheid,partial
NED-05,Incident Response & Reporting,MANAGE,MANAGE-2.3,Art. 72,C.6-7,Art. 23,,full
```

## Three-Layer Validation (OpenMythos Gate)

### Layer 1: Structural (automated, CI)

| Check | Tool | Gate |
|-------|------|------|
| YAML validity | json-schema-validator | Hard fail |
| CSV completeness (all cells populated) | csv-lint | Hard fail |
| Referential integrity (all refs exist in source docs) | custom script | Hard fail |
| Bidirectional completeness (every NIST function has ≥1 correlate) | custom script | Warning |
| No circular dependencies | custom script | Hard fail |

### Layer 2: Semantic (expert review)

| Check | Method | Gate |
|-------|--------|------|
| Mapping correctness (is this truly equivalent?) | SME review per mapping | Required |
| Granularity mismatch documented (1:N mappings) | SME annotation | Required |
| Conflict detection (framework X requires, Y forbids) | Cross-reference matrix | Required |
| Second reviewer for high-severity mappings | Peer review | Required |

### Layer 3: Operational (empirical)

| Check | Method | Gate |
|-------|--------|------|
| Scenario-based validation (apply to real AI system) | Pilot engagement | Required |
| Cross-framework consistency (no contradictions) | Automated + manual | Required |
| Freshness (all refs to current framework versions) | Version check script | Hard fail |

**Human approval gate**: Every mapping row in the CSV requires an `approved_by`
field with a named individual. Rows without approval are excluded from published
output. This is non-negotiable for compliance frameworks.

## Conflict Resolution

Known inter-framework conflicts are documented in `crosswalks/conflicts.md`:

| Conflict | Frameworks | Resolution |
|----------|-----------|------------|
| Incident reporting timing | NIS2 Art. 23 (24h) vs EU AI Act Art. 72 (15d initial) | Apply most stringent: 24h preliminary notification to national CSIRT, 15-day formal report to EU AI Office. NED-05 evidence template supports both timelines. |
| Risk classification | EU AI Act 4-tier (prohibited/high/limited/minimal) vs BIO2 4-tier (baseline→zeer ernstig) | No direct mapping — organizations maintain separate classifications. NED-01 maps EU AI Act classification; BIO2 classification remains organization-internal. |

## Djimitflo Integration

**Pattern**: External data-source + thin wrapper (not embedded engine).

```typescript
// src/compliance/controls-loader.ts (~30 lines)
// src/compliance/task-generator.ts (~40 lines)
// src/compliance/audit-events.ts (~30 lines)
// src/compliance/approval-gate.ts (~20 lines)
```

Djimitflo reads `controls.yaml` → generates compliance tasks → routes through
existing approval workflow → records in audit trail. NEDERUS CLI handles
risk classification and framework-specific logic; Djimitflo handles orchestration.

**Integration point**: Git submodule or periodic sync of `controls.yaml` into
Djimitflo's `src/compliance/data/` directory.

## Versioning Strategy

- `controls.yaml` uses semver (v1.0.0, v1.0.1, v1.1.0, v2.0.0)
- Each framework reference includes version: `eu_ai_act: "2024/1689"`
- CHANGELOG.md tracks every addition, modification, deprecation
- Deprecated controls marked with `status: deprecated` (never removed)
- Breaking changes require major version bump

## Reviewer Model

v1.0 is authored and reviewed by DjimIT (Dennis Landman). For v1.1+, the following
reviewers are pre-committed:

| Reviewer | Role | Affiliation |
|----------|------|-------------|
| Dennis Landman | Lead author, maintainer | DjimIT B.V. |
| [TBD — VNG AI program] | Public sector reviewer | VNG |
| [TBD — ISO 17021 auditor] | Accreditation reviewer | TBD |

For v1.0, all mappings are self-reviewed with documented rationale. The `approved_by`
field contains "DjimIT (self-reviewed)" with a link to the rationale document.
This limitation is disclosed in README.md and resolved before v1.1.

## Rollback

- Git revert for any published change
- Deprecated controls remain accessible via git tags
- No database migration or service restart needed (static data product)
- Djimitflo integration can pin to specific NEDERUS version via git submodule ref
