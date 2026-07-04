# Contributing to JREM

## Schema Changes
- JREM schema uses semantic versioning (schemaVersion field)
- Breaking changes require a major version bump
- All changes must validate against JSON Schema draft 2020-12
- additionalProperties: false must be maintained on all object levels

## JREM Instance Contributions
- Every rule must have at least 1 sourceRef
- Every ruleset must have validFrom and validUntil
- Scenarios should cover ≥90% of rule combinations
- metadata.acceptatieType must be "draft" for unreviewed instances

## Review Process
1. Fork the repository
2. Add or modify schema/examples
3. Validate: `python3 validate.py --schema schema.json --instance examples/your-instance.json`
4. Submit pull request with description of changes
