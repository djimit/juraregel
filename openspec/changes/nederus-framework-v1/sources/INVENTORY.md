# Framework Source Inventory — NEDERUS v2.0

This document records the exact versions and sources of all framework documents
used to build NEDERUS v2.0 controls and mappings.

| Framework | Version | Source URL | Status | Last Verified |
|-----------|---------|------------|--------|---------------|
| NIST AI RMF 1.0 | 1.0 (Jan 2023) | https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf | Referenced | 2026-07-17 |
| NIST AI RMF Playbook | 1.0 | https://airc.nist.gov/airmf-resources/playbook/ | Referenced | 2026-07-17 |
| EU AI Act | 2024/1689 | https://eur-lex.europa.eu/eli/reg/2024/1689 | Referenced | 2026-07-17 |
| BIO2 | 2.2 | https://www.digitaleoverheid.nl/overzicht-van-alle-onderwerpen/bio-baseline-informatiebeveiliging-overheid/ | Referenced | 2026-07-17 |
| NIS2 | 2022/2555 | https://eur-lex.europa.eu/eli/dir/2022/2555 | Referenced | 2026-07-17 |
| NORA | 2024 (current) | https://www.noraonline.nl/ | Referenced | 2026-07-17 |
| Cyber Resilience Act | 2024/2847 | https://eur-lex.europa.eu/eli/reg/2024/2847 | Referenced | 2026-07-17 |
| Digital Services Act | 2022/2065 | https://eur-lex.europa.eu/eli/reg/2022/2065 | Referenced | 2026-07-17 |
| AI Liability Directive | 2024/2853 | https://eur-lex.europa.eu/eli/dir/2024/2853 | Referenced | 2026-07-17 |

## Version Lock Rationale

NEDERUS v1.0 is locked to these specific versions. When frameworks update:

1. A new NEDERUS minor/patch version is released
2. The CHANGELOG.md documents which mappings changed
3. Deprecated mappings are marked `status: deprecated` (never removed)
4. This inventory is updated with the new version numbers

## Known Upcoming Changes

| Framework | Expected Update | Impact |
|-----------|----------------|--------|
| BIO2 | BIO3 (2025-2026) | Security control numbering may change |
| EU AI Act | Implementing acts (2025-2027) | Article references stable, guidance documents may add detail |
| NORA | Annual updates | Grondslagen numbering stable |

## Verification Method

Each crosswalk document (`crosswalks/*.md`) contains article-level citations
that can be verified against the source URLs above. If a citation cannot be
verified against the locked version, it is a bug — file an issue.
