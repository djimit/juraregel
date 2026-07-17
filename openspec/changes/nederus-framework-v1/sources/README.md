# NEDERUS Framework v2.0

**Nederlandse Unified AI Standards** — A unified mapping between AI governance frameworks
for Dutch public organizations.

## What is NEDERUS?

Dutch organizations deploying AI systems must comply with multiple frameworks
simultaneously. NEDERUS unifies them: **one control satisfies multiple frameworks**.

## The 8 v2.0 Controls

### Priority Controls (≥3 frameworks)

| ID | Control | Frameworks | Coverage |
|----|---------|------------|----------|
| NED-01 | AI Impact Assessment | NIST, EU AI Act, BIO2, NIS2, NORA, CRA, AI Liability | 7/8 |
| NED-02 | Bias & Fairness Testing | NIST, EU AI Act, NORA, DSA, AI Liability | 5/8 |
| NED-03 | Human Oversight | NIST, EU AI Act, NORA, AI Liability | 4/8 |
| NED-04 | Transparency & Explainability | NIST, EU AI Act, NORA, CRA, DSA, AI Liability | 6/8 |
| NED-05 | Incident Response & Reporting | NIST, EU AI Act, BIO2, NIS2, CRA, DSA, AI Liability | 7/8 |

### Standard Controls (≥2 frameworks)

| ID | Control | Frameworks | Coverage |
|----|---------|------------|----------|
| NED-06 | Secure Development & Vulnerability Management | NIST, EU AI Act, BIO2, NIS2, NORA, CRA, AI Liability | 6/8 |
| NED-07 | Platform Transparency & Content Governance | NIST, EU AI Act, NORA, DSA, AI Liability | 5/8 |
| NED-08 | AI Liability & Evidence Preservation | NIST, EU AI Act, BIO2, NIS2, NORA, CRA, DSA, AI Liability | 8/8 |

## The 8 Frameworks

### Functional Backbone
- **NIST AI RMF 1.0** — Risk management methodology

### EU Legal Frameworks
- **EU AI Act 2024/1689** — AI regulation (primary)
- **Cyber Resilience Act 2024/2847** — Product security
- **Digital Services Act 2022/2065** — Platform transparency
- **AI Liability Directive 2024/2853** — Burden of proof (deadline Dec 2026)

### National Frameworks
- **BIO2 v2.2** — Information security baseline
- **NIS2 2022/2555** — Cybersecurity directive
- **NORA 2024** — Reference architecture principles

## Quickstart

1. Start with [`mapping-matrix.csv`](mapping-matrix.csv) — the 8×8 overview
2. Read [`controls.yaml`](controls.yaml) for full control definitions
3. Dive into [`crosswalks/`](crosswalks/) for per-framework detail

## Architecture

NEDERUS is a **data product** (YAML + CSV), not a software product. It is consumed by:
- **JuraRegel MCP Server** — serves NEDERUS mappings to LLM agents
- **Djimitflo** — YAML-injects NEDERUS controls as compliance workflow context
- **Human compliance officers** — browse crosswalks and mapping matrix

## Precedent

NEDERUS is inspired by [SCITUS](https://arxiv.org/abs/2607.15051) (Canada), which maps
127 federal+provincial requirements to 57 unified controls.

## Known Limitations

- **v2.0 mappings are self-reviewed** by DjimIT (single maintainer). Independent review begins with v2.1.
- **Scope**: AI governance mapping only. Technical security controls remain in BIO2/NIS2.

## Roadmap

| Version | Timeline | Content |
|---------|----------|---------|
| v2.0 | Jul 2026 | 8 controls, 8 frameworks |
| v2.1 | Q4 2026 | Independent review, pilot feedback |
| v3.0 | Q2 2027 | ISO 42001 integration, community contributions |

## Contributing & License

[CC-BY 4.0](LICENSE) — DjimIT B.V., 2026
See [CONTRIBUTING.md](.github/CONTRIBUTING.md) and [GOVERNANCE.md](GOVERNANCE.md).
