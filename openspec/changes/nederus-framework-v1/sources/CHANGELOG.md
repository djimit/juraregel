# Changelog

All notable changes to the NEDERUS Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- v2.1: Independent review by VNG and ISO 17021 auditor
- v2.1: Pilot feedback integration
- v3.0: ISO 42001 integration, community contributions

## [2.0.0] - 2026-07-17

### Added
- 3 new controls: NED-06 (Secure Development), NED-07 (Platform Transparency), NED-08 (AI Liability)
- 3 new frameworks: CRA, DSA, AI Liability Directive
- Tier system: Priority (≥3 frameworks) and Standard (≥2 frameworks)
- Per-framework crosswalks:
  - crosswalks/cra.md (75% CRA coverage)
  - crosswalks/dsa.md (75% DSA coverage)
  - crosswalks/ai-liability.md (100% AI Liability coverage)
- Updated GOVERNANCE.md with tier system and v2.0 scope
- Updated README.md with 8 controls, 8 frameworks, architecture diagram
- Updated INVENTORY.md with 3 new framework sources

### Changed
- Selection criteria: ≥3 ≥2 frameworks (tier-based)
- Version bump: 1.0.0 → 2.0.0 (new frameworks = minor version per semver)
- 5 v1.0 controls updated with 3 new framework references each

### Known Limitations
- v2.0 mappings are self-reviewed by DjimIT (single maintainer)
- Independent review commitment begins with v2.1

## [1.0.0] - 2026-07-17

### Added
- Initial 5 controls: NED-01 through NED-05
- 5 frameworks: NIST AI RMF, EU AI Act, BIO2, NIS2, NORA
- controls.yaml, mapping-matrix.csv, crosswalks
- Validation pipeline, CI workflow, GitHub templates

[Unreleased]: https://github.com/djimit/nederus-framework/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/djimit/nederus-framework/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/djimit/nederus-framework/releases/tag/v1.0.0
