# Contributing to NEDERUS Framework

Thank you for your interest in contributing to NEDERUS (Nederlandse Unified AI Standards).

## How to Contribute

### Reporting Issues

Use GitHub Issues to:
- Report incorrect mappings (include specific article/section references)
- Suggest new controls
- Flag framework version changes that affect mappings
- Report documentation errors

### Proposing New Controls or Mapping Changes

1. Open an issue describing the proposed change
2. Include: source framework reference, target framework reference, rationale
3. Wait for maintainer review (DjimIT)
4. If approved, submit a PR with the change

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`feature/NED-XX-description`)
3. Make changes to `controls.yaml` (never edit `mapping-matrix.csv` directly)
4. Run `python scripts/generate_matrix.py` to regenerate the CSV
5. Run `python scripts/validate.py` — must pass
6. Update `crosswalks/*.md` if adding new framework mappings
7. Update `CHANGELOG.md` under "Unreleased"
8. Submit PR with description of what changed and why

## Review Process

### v1.0 (Current)
All mappings are authored and self-reviewed by DjimIT. This limitation is
disclosed in README.md and GOVERNANCE.md.

### v1.1+ (Future)
Each mapping change requires:
- Review by 1 independent domain expert (not the author)
- `approved_by` field in mapping-matrix.csv with reviewer name
- Documentation of review rationale in PR description

## Code of Conduct

- Be respectful and constructive
- Focus on factual accuracy of mappings
- Cite sources — every mapping must have a traceable reference
- Disclose conflicts of interest (e.g., if you work for a framework body)

## Questions?

Open an issue or contact: framework@djimit.nl
