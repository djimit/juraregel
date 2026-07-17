# NEDERUS Framework Governance

## Ownership

**Framework Owner**: DjimIT B.V.
**Lead Maintainer**: Dennis Landman
**License**: CC-BY 4.0

## Scope

NEDERUS v2.0 provides unified AI governance controls mapped to 8 frameworks:

### Functional Backbone
- **NIST AI RMF 1.0** — Risk management methodology (GOVERN, MAP, MEASURE, MANAGE)

### Legal Frameworks (EU)
- **EU AI Act 2024/1689** — AI-specific regulation (primary legal framework)
- **Cyber Resilience Act 2024/2847** — Product security for digital elements
- **Digital Services Act 2022/2065** — Platform transparency and content governance
- **AI Liability Directive 2024/2853** — Burden of proof for AI damage claims

### Legal Frameworks (National)
- **BIO2 v2.2** — Information security baseline for Dutch government
- **NIS2 2022/2555** — Cybersecurity directive
- **NORA 2024** — Dutch government reference architecture principles

## Control Selection Criteria

### Tier System

| Tier | Criteria | Value |
|------|----------|-------|
| **Priority** | Control appears in >=3 frameworks | Highest reusability |
| **Standard** | Control appears in >=2 frameworks | Proven overlap |
| **Minimum** | >=2 frameworks required for inclusion | Quality floor |

### v2.0 Controls

| ID | Title | Tier | Frameworks |
|----|-------|------|------------|
| NED-01 | AI Impact Assessment | Priority | 7/8 |
| NED-02 | Bias & Fairness Testing | Priority | 5/8 |
| NED-03 | Human Oversight | Priority | 4/8 |
| NED-04 | Transparency & Explainability | Priority | 5/8 |
| NED-05 | Incident Response & Reporting | Priority | 7/8 |
| NED-06 | Secure Development & Vulnerability Management | Standard | 5/8 |
| NED-07 | Platform Transparency & Content Governance | Standard | 4/8 |
| NED-08 | AI Liability & Evidence Preservation | Standard | 8/8 |

## Out of Scope

- **DMA** (Digital Markets Act) — Platform economics, not AI governance
- **Arbo/AI** — Workplace safety, not AI governance
- **ISO 42001** — Certification framework (future consideration)
- **eIDAS 2.0** — Identity management, not AI governance (covered via Forum Standaardisatie)
- **Wdo** — Accessibility implementation detail, not AI governance framework

## Release Cadence

- **Patch releases** (v2.0.x): As needed for corrections
- **Minor releases** (v2.x.0): Quarterly, adding new controls or framework updates
- **Major releases** (v3.0.0): Annually, structural changes

## Decision Making

### Adding a New Control
1. Open issue with proposed control definition
2. Demonstrate it maps to >=2 frameworks (>=3 for priority tier)
3. Show it is actionable and auditable
4. Maintainer reviews and approves/rejects

### Modifying a Mapping
1. Open issue with current mapping, proposed mapping, and rationale
2. Cite specific source framework article/section
3. v1.0-v2.0: Maintainer approves (self-review, disclosed limitation)
4. v2.1+: Requires 1 independent reviewer

### Deprecating a Control
1. Mark as `status: deprecated` in controls.yaml (never remove)
2. Document reason in CHANGELOG.md
3. Provide migration guidance if applicable

## Reviewer Model

### v2.0 (Current)
All mappings authored and self-reviewed by DjimIT. Limitation disclosed.

### v2.1+ (Planned)
| Reviewer | Role | Status |
|----------|------|--------|
| DjimIT | Lead author, maintainer | Active |
| VNG AI program | Public sector reviewer | TBD |
| ISO 17021 auditor | Accreditation reviewer | TBD |

## Contribution Process

1. Fork repository
2. Create feature branch
3. Edit `controls.yaml` (never edit `mapping-matrix.csv` directly)
4. Run `python scripts/generate_matrix.py`
5. Run `python scripts/validate.py`
6. Update crosswalks and CHANGELOG
7. Submit PR

## Quality Standards

- Every mapping must cite a specific article/section number
- No mapping may reference a draft or superseded framework version
- All evidence requirements must be producible by a real organization
- Controls must be testable (an auditor can verify compliance)
- Tier classification must be accurate (>=3 for priority, >=2 for standard)
