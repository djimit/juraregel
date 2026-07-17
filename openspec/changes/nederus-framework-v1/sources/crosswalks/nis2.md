# NIS2 → NEDERUS Crosswalk

Maps NIS2 Directive 2022/2555 articles to NEDERUS unified controls.

NIS2 is a cybersecurity directive. Coverage is limited to risk management and
incident reporting domains.

## Risk Management (Art. 21)

| NIS2 Article | Requirement | NEDERUS Control | Relation |
|--------------|-------------|-----------------|----------|
| Art. 21 | Risk management measures | NED-01 (AI Impact Assessment) | partial |
| Art. 21(2)(a) | Risk analysis and system security | NED-01 (AI Impact Assessment) | partial |
| Art. 21(2)(b) | Incident handling | NED-05 (Incident Response) | equivalent |
| Art. 21(2)(c) | Business continuity | — | gap (continuity management) |
| Art. 21(2)(d) | Supply chain security | — | gap (vendor management) |
| Art. 21(2)(e) | Security in network/system development | — | gap (SDLC) |

## Incident Reporting (Art. 23)

| NIS2 Article | Requirement | NEDERUS Control | Relation |
|--------------|-------------|-----------------|----------|
| Art. 23(1) | Early warning within 24h | NED-05 (Incident Response) | equivalent |
| ArtED-23(2) | Incident notification within 72h | NED-05 (Incident Response) | equivalent |
| Art. 23(3) | Final report within 1 month | NED-05 (Incident Response) | equivalent |

## Coverage Summary

**NIS2 coverage: 5/9 mapped articles (56%)**

NIS2 addresses cybersecurity broadly. NEDERUS covers the AI-specific governance
that NIS2 does not address (bias, human oversight, transparency). Organizations
should maintain full NIS2 compliance alongside NEDERUS.

## Known Conflict: Incident Reporting Timing

NIS2 Art. 23 requires 24h preliminary notification. EU AI Act Art. 72 allows 15 days
for initial serious incident report. See `crosswalks/conflicts.md` for resolution.
