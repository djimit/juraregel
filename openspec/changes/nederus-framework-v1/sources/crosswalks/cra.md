# Cyber Resilience Act → NEDERUS Crosswalk

Maps CRA (EU 2024/2847) articles to NEDERUS unified controls.

**Important note**: CRA applies to "products with digital elements" placed on the EU market.
PoC platforms like JuraRegel may be exempt until commercial distribution begins.
This crosswalk is relevant for organizations deploying AI systems as products.

## Essential Requirements (Art. 10-13)

| CRA Article | Requirement | NEDERUS Control | Relation |
|-------------|-------------|-----------------|----------|
| Art. 10 | Risk assessment | NED-01 (AI Impact Assessment) | partial |
| Art. 11 | Vulnerability handling | NED-05 (Incident Response) + NED-06 (Secure Development) | equivalent |
| Art. 12 | Security by design | NED-06 (Secure Development) | equivalent |
| Art. 13 | Information and instructions | NED-04 (Transparency) | partial |
| Art. 14 | Incident reporting | NED-05 (Incident Response) | equivalent |
| Art. 15 | Cybersecurity certification | — | gap (certification body) |

## Conformity Assessment (Art. 16-20)

| CRA Article | Requirement | NEDERUS Control | Relation |
|-------------|-------------|-----------------|----------|
| Art. 16 | Self-assessment (Class I) | NED-01 + NED-06 | partial |
| Art. 17 | Third-party assessment (Class II) | — | gap (notified body) |
| Art. 20 | Open source software | NED-06 | partial |

## Vulnerability Reporting (Art. 11)

| CRA Requirement | NEDERUS Control | Timeline |
|-----------------|-----------------|----------|
| Vulnerability reporting process | NED-06 (Secure Development) | Ongoing |
| Incident reporting to ENISA | NED-05 (Incident Response) | 72h awareness, 14d detailed |

## Coverage Summary

**CRA coverage: 6/8 mapped articles (75%)**

Unmapped articles are conformity assessment procedures (notified body functions)
or open source exemptions — outside NEDERUS v2.0 scope.

## Relationship to Other Frameworks

| CRA Overlap | Shared Control |
|-------------|---------------|
| CRA Art. 11 + NIS2 Art. 21 | NED-05 (Incident Response) |
| CRA Art. 12 + BIO2 B.3 | NED-06 (Secure Development) |
| CRA Art. 13 + EU AI Act Art. 13 | NED-04 (Transparency) |
