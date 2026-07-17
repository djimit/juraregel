## Phase 0: Foundation (Week 1-2)

- [x] 0.1 Collect and inventory all source framework documents
  - NIST AI RMF 1.0 + Playbook (download from airc.nist.gov)
  - EU AI Act Verordening 2024/1689 (download from eur-lex)
  - BIO2 v2.2 (download from digitaleoverheid.nl)
  - NIS2 richtlijn 2022/2555 + NL implementatie
  - NORA 2.0 grondslagen (download from noraonline.nl)
  - **Acceptance**: All 5 source documents stored in `sources/` with version metadata

- [x] 0.2 Define JSON Schema for controls.yaml
  - Schema validates: id format, required fields, framework refs, severity enum
  - Schema validates: date format, semver format, relation enum
  - **Acceptance**: `schemas/control-schema.json` passes jsonschemavalidator.net

- [x] 0.3 Set up GitHub repository structure
  - Create `nederus-framework` repo under github.com/djimit
  - Add LICENSE (CC-BY 4.0)
  - Add .github/ templates (CONTRIBUTING, ISSUE_TEMPLATE)
  - **Acceptance**: Repo is public, has license, has templates

## Phase 1: Core Data (Week 2-4)

- [x] 1.1 Write controls.yaml (5 controls)
  - NED-01 through NED-05 with full framework references
  - Each control has: id, title, description, severity, frameworks, evidence, guidance
  - **Acceptance**: Validates against JSON Schema, all 5 frameworks represented

- [x] 1.2 Generate mapping-matrix.csv from controls.yaml
  - Run `python scripts/generate_matrix.py` (built in Phase 2, task 2.3)
  - 5 rows × 8 columns (control_id, title, nist, eu, bio2, nis2, nora, coverage)
  - Every cell populated (use "N/A" for gaps, never empty)
  - CSV is NEVER hand-edited — always regenerated from YAML
  - **Acceptance**: CSV parses cleanly, no empty cells, coverage column accurate, `generate_matrix.py` output matches committed CSV exactly

- [x] 1.3 Write crosswalk documentation (5 files)
  - `crosswalks/nist-rmf.md` — NIST → NEDERUS mapping with subfunction detail
  - `crosswalks/eu-ai-act.md` — EU AI Act → NEDERUS with article numbers
  - `crosswalks/bio2.md` — BIO2 → NEDERUS with control references
  - `crosswalks/nis2.md` — NIS2 → NEDERUS with article numbers
  - `crosswalks/nora.md` — NORA → NEDERUS with grondslag references
  - **Acceptance**: Each crosswalk cites specific articles/sections, not generic references

- [x] 1.4 Write GOVERNANCE.md
  - Defines: maintainers (DjimIT), release cadence (quarterly), contribution process
  - Defines: approval process for new mappings (2 reviewers required for v1.1+)
  - Defines: v1.0 self-review limitation and disclosure requirement
  - Defines: deprecation policy, escalation process
  - **Acceptance**: Document answers "who decides?", "how to contribute?", "what if wrong?"

- [x] 1.5 Write crosswalks/conflicts.md
  - Document all known inter-framework conflicts and their resolutions
  - Minimum: NIS2 24h vs EU AI Act 15d incident reporting timing
  - **Acceptance**: Each conflict has: frameworks involved, description, resolution rule, impact on controls

## Phase 2: Validation Pipeline (Week 3-5)

- [x] 2.1 Build structural validation script (`scripts/validate.py`)
  - YAML schema validation
  - CSV completeness check
  - Referential integrity check (all refs exist)
  - Bidirectional completeness check
  - **Acceptance**: Script runs via `python scripts/validate.py`, exits 0 on valid data

- [x] 2.2 Build CI workflow (`.github/workflows/validate.yml`)
  - Runs on every push and PR
  - Executes structural validation
  - Blocks merge on failure
  - **Acceptance**: PR with invalid YAML is blocked, PR with valid YAML passes

- [x] 2.3 Build mapping-matrix generator (`scripts/generate_matrix.py`)
  - Reads controls.yaml
  - Outputs mapping-matrix.csv
  - Ensures CSV is always in sync with YAML
  - **Acceptance**: `python scripts/generate_matrix.py` produces identical CSV to committed version

- [x] 2.4 Semantic review gate (manual process)
  - Document review process in CONTRIBUTING.md (task 0.3)
  - Require 2 named reviewers per mapping change (GOVERNANCE.md task 1.4)
  - Require `approved_by` field for each mapping row (CSV has approved_by column, all rows populated)
  - **Acceptance**: No mapping row in CSV lacks `approved_by` field ✓

## Phase 3: Documentation + Publication (Week 4-6)

- [x] 3.1 Write README.md
  - Framework overview (what is NEDERUS, why it exists)
  - Quickstart (how to read the mapping, how to use controls)
  - SCITUS precedent reference (arXiv:2607.15051)
  - Contributing guide (link to CONTRIBUTING.md)
  - **Acceptance**: README understandable by compliance officer with no AI background

- [x] 3.2 Write CHANGELOG.md
  - v1.0.0 entry with full change description
  - Template for future versions
  - **Acceptance**: Follows Keep a Changelog format

- [ ] 3.3 Publish blogpost on djimit.nl
  - Title: "5 controls die EU AI Act, BIO2 en NIS2 simultaan dekken"
  - References SCITUS as precedent
  - Links to GitHub repo
  - **Acceptance**: Published, indexed, shareable URL
  - **BLOCKED**: Requires human action (WordPress login + publish). Draft ready in blogpost-draft.md

## Phase 4: Djimitflo Integration (Week 5-7)

- [x] 4.1 Implement controls-loader.ts (~30 lines)
  - Reads controls.yaml from git submodule or local path
  - Parses YAML into typed Control[]
  - **Acceptance**: Unit test passes with sample controls.yaml

- [x] 4.2 Implement task-generator.ts (~40 lines)
  - Converts Control[] into Djimitflo Task[]
  - Maps severity to priority
  - Generates evidence checklist per task
  - **Acceptance**: 5 controls → 5 tasks with correct priorities

- [x] 4.3 Implement approval-gate integration (~20 lines)
  - High-severity controls require 2 approvers
  - Medium-severity require 1 approver
  - Audit trail records approver identity
  - **Acceptance**: Cannot mark high-severity control as passed without 2 approvals

- [x] 4.4 Add compliance audit events (~30 lines)
  - New event type: `compliance-evaluated`
  - Records: control_id, result, evidence_refs, evaluator, timestamp
  - **Acceptance**: Events appear in Djimitflo audit log

## Phase 5: Pilot + Case Study (Week 12-24)

**Dependency**: Requires Phase 3 (publication) complete. Phase 6 (adoption) runs
in parallel starting Week 8 but VNG/webinar activities are independent of pilot results.

- [ ] 5.1 Identify pilot partner — BLOCKED: requires human outreach to VNG/gemeenten
  - Target: municipality (via VNG network) or province
  - Criteria: has AI in production, faces multi-framework compliance
  - Pre-approach 3 candidates before Week 12
  - **Acceptance**: Signed agreement (even informal) with pilot partner

- [ ] 5.2 Run NEDERUS mapping on pilot's AI systems
  - Apply all 5 controls to ≥1 AI system
  - Document gaps and overlaps
  - **Acceptance**: Completed mapping document for pilot organization

- [ ] 5.3 Publish anonymized case study
  - Write up findings (anonymized)
  - Publish on djimit.nl/proof
  - **Acceptance**: Case study is public, demonstrates value

- [ ] 5.4 Incorporate pilot feedback into v1.1
  - Add 3-5 new controls based on pilot findings
  - Fix any mapping errors discovered
  - **Acceptance**: v1.1 released with changelog

## Phase 6: Adoption (Week 6+, ongoing)

- [ ] 6.1 VNG outreach
  - Contact VNG AI/compliance program
  - Offer NEDERUS as gemeentelijke compliance starter
  - **Acceptance**: ≥1 VNG contact acknowledges framework

- [ ] 6.2 Webinar
  - "5 controls, 3 frameworks, 1 hour" format
  - Target: overheids CIOs, compliance officers
  - **Acceptance**: ≥20 attendees, recording published

- [ ] 6.3 ISO 42001 partnership exploration
  - Identify accredited auditor for assurance-grade validation
  - Explore partnership model (DjimIT mapping + auditor certification)
  - **Acceptance**: ≥1 conversation with potential partner

## JuraRegel Integration (Week 6+)

- [x] JuraRegel README.md: NEDERUS use case sectie toegevoegd
- [x] JuraRegel README.md: Use Case Maturity tabel bijgewerkt
- [x] JuraRegel README.md: Architectuur diagram + NEDERUS Framework bron
- [x] JuraRegel README.md: Validatie sectie + NEDERUS metriek
- [x] JuraRegel README.md: Compliance Officer rol + NEDERUS link
- [x] docs/nora-compliance-matrix.md: NEDERUS mapping sectie
- [x] docs/bio2-use-case.md: NEDERUS koppeling + mapping tabel
- [x] docs/eu-ai-act-use-case.md: NEDERUS koppeling + mapping tabel
- [x] docs/agent-playbooks/nis2.md: NEDERUS koppeling + conflict documentatie
- [x] CHANGELOG.md: v2.2.0 entry met NEDERUS wijzigingen

## Definition of Done

- [x] GitHub repo is public, has 5 valid controls, 5 crosswalks, CI pipeline
- [ ] Blogpost is published and indexed — BLOCKED: requires WordPress login
- [x] Djimitflo integration loads controls.yaml and generates tasks (artifacts ready)
- [ ] Pilot case study is published (anonymized) — BLOCKED: requires pilot partner
- [x] GOVERNANCE.md is complete with named maintainers
- [x] All validation scripts pass (Layer 1 structural)
- [x] All mappings have `approved_by` field (Layer 2 semantic)
- [x] JuraRegel README.md bijgewerkt met NEDERUS use case
- [x] Bestaande use case documentatie gelinkt aan NEDERUS
- [x] CHANGELOG.md bijgewerkt
