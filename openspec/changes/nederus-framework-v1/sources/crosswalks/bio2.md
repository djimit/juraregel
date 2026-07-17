# BIO2 → NEDERUS Crosswalk

Maps BIO2 (Baseline Informatiebeveiliging Overheid) v2.2 controls to NEDERUS unified controls.

BIO2 is an information security baseline, not AI-specific. Coverage is limited to
security governance and incident management domains.

## Beheersmaatregelen (Management Measures)

| BIO2 Reference | Control Theme | NEDERUS Control | Relation |
|----------------|---------------|-----------------|----------|
| A.5 | Beveiligingsbeleid | NED-01 (AI Impact Assessment) | partial |
| A.6 | Risicoanalyse en -behandeling | NED-01 (AI Impact Assessment) | equivalent |
| A.7 | Human resources security | — | gap (organizational, not AI-specific) |
| A.8 | Asset management | — | gap (IT asset management) |

## Operationele Maatregelen (Operational Measures)

| BIO2 Reference | Control Theme | NEDERUS Control | Relation |
|----------------|---------------|-----------------|----------|
| B.5 | Access control | NED-03 (Human Oversight) | partial |
| B.6 | Cryptography | — | gap (technical security) |
| B.7 | Physical security | — | gap (physical security) |
| B.8 | Operations security | — | gap (IT operations) |
| B.9 | Communications security | — | gap (network security) |
| B.10 | System acquisition/development | — | gap (SDLC) |
| B.11 | Supplier relationships | — | gap (vendor management) |
| B.12 | Incident management | NED-05 (Incident Response) | equivalent |
| B.13 | Business continuity | — | gap (continuity management) |

## Coverage Summary

**BIO2 coverage: 4/12 relevant controls mapped (33%)**

BIO2 is fundamentally an IT security framework. NEDERUS addresses the AI-specific
governance layer that BIO2 does not cover. Organizations should maintain full BIO2
compliance alongside NEDERUS — the frameworks are complementary, not overlapping.
