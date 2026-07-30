# ISO/IEC 27017:2026 Assurance

Non-scoring evidence pilot for the four explicit cloud-specific controls in
ISO/IEC 27017:2026. It does not reproduce licensed guidance and does not provide
an ISO conformity, certification or legal-compliance conclusion.

The profile records local, falsifiable evidence expectations. The crosswalk is
draft analysis: related BIO2, NIST, DORA and EU AI Act material is not treated
as equivalent.

```bash
python3 use-cases/acict-assurance/assess.py \
  use-cases/iso27017-assurance/profiles/iso27017-2026.json \
  use-cases/iso27017-assurance/assessments/juraregel-2026.json
```

The expected result is `evidence-incomplete` until licensed source review,
target-environment evidence and independent assessment exist. See the
[Level 3 plan](../../docs/iso27017-2026-level3-plan.md).
