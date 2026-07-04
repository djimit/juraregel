# JREM — Judicial Rule Exchange Model

An open standard for exchanging legal rules as structured, validated, auditable JSON.

## What is JREM?

JREM is a JSON Schema (draft 2020-12) that structures administrative-legal rules with:
- Rules with conditions, outcomes, and source references
- Embedded test scenarios
- Version management with validity periods
- Metadata with legal context and jurist acceptance

## Why JREM?

Legal rules currently live in PDFs, spreadsheets, and legacy code. JREM makes them:
- **Digital** — structured JSON, not text
- **Testable** — embedded scenarios with expected outcomes
- **Auditable** — source references, version tracking, jurist acceptance
- **Explainable** — every rule has a legal source and reasoning steps
- **Vendor-neutral** — not bound to any rule engine, language, or platform

## Quick Start

```bash
# Validate a JREM instance
python3 validate.py --schema schema.json --instance examples/griffierecht-civiel-2026.1.json
```

## Schema

The JREM schema defines:
- `ruleSetId`, `version`, `validFrom`, `validUntil` — identity and validity
- `rules[]` — each with `ruleId`, `conditions`, `outcome`, `sourceRefs`
- `scenarios[]` — test cases with input and expected output
- `transitionRules[]` — rules for version transitions
- `metadata` — optional legal context and jurist acceptance

## License

MIT — use freely, contribute back, no warranty.

## Contributing

See CONTRIBUTING.md (to be added). The schema is versioned semantically.
