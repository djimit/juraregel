# NEDERUS Framework v1.0 — Multi-Jurisdictional AI Compliance Mapping

## Why

Dutch public organizations simultaneously comply with EU AI Act, BIO2, NIS2, and
NORA. Each framework has its own taxonomy, its own impact assessment, its own
incident reporting. Organizations duplicate work: the same risk assessment is
written three times in three formats for three different auditors.

SCITUS (Canada, arXiv:2607.15051) proves this is solvable: 127 federal+provincial
requirements mapped to 57 unified controls with versioned governance. No
equivalent exists for the Dutch/EU context. This gap is DjimIT's market
opportunity — we already combine EU AI Act + BIO2 + NIS2 + NORA in client
engagements. NEDERUS systematizes this into an open, versioned framework.

**Problem metrics:**
- 4 frameworks × ~25-40 requirements each = ~100-160 individual compliance items
- Estimated 60% thematic overlap (risk assessment, human oversight, transparency,
  incident response, accountability)
- Organizations currently map these manually: 2-4 weeks per framework per audit cycle
- No open-source mapping exists for the Dutch context

**Strategic value:**
- Positions DjimIT as thought leader in multi-jurisdictional AI compliance
- Creates inbound lead flow (free tool → paid advisory)
- Provides structured data for Djimitflo compliance workflows
- First-mover window closes August 2026 (EU AI Act fully in force)

## What Changes

- Create `nederus-framework` as public GitHub repository (CC-BY 4.0)
- Define 5 v1.0 unified controls using NIST AI RMF as functional backbone,
  mapped to EU AI Act, BIO2, NIS2, and NORA (4 legal frameworks + 1 functional framework)
- Publish machine-readable `controls.yaml` with JSON Schema validation
- Publish `mapping-matrix.csv` with bidirectional traceability
- Publish per-framework crosswalk documentation with article-level citations
- Publish `GOVERNANCE.md` with maintainer model, release cadence, contribution process
- Publish blogpost on djimit.nl positioning NEDERUS and linking to SCITUS precedent
- Integrate `controls.yaml` as data source in Djimitflo (~120 lines TS loader + task generator)

## Impact

- **DjimIT advisory**: NEDERUS becomes standardized starting point for engagements
- **Djimitflo**: Compliance-as-code capability via YAML consumption
- **Market position**: First open multi-jurisdictional AI compliance framework for NL
- **Risk**: Incorrect mappings could mislead organizations — mitigated by three-layer
  validation (structural, semantic, operational) with human approval gate
- **Timing**: Phase 0-3 (public framework, week 1-6) delivers the first-mover asset
  before EU AI Act full enforcement (August 2026). Phase 4-6 (integration, pilot,
  adoption) extend value post-launch.
- **Scope boundary**: v1.0 covers high-risk AI systems and governance controls only.
  Technical security controls (cryptography, network segmentation) remain in BIO2/NIS2.
  Sector-specific frameworks (AVG, Wpg) excluded from initial scope.
- **Known limitation**: v1.0 mappings are self-reviewed by DjimIT (single maintainer).
  Independent review commitment begins with v1.1. This is disclosed in README.md
  and GOVERNANCE.md.
