# Threat Model — [Systeem naam]
## STRIDE Analyse
| Threat | Component | Scenario | Mitigatie | JuraRegel check |
|---|---|---|---|---|
| Spoofing | Auth | Stolen credentials | MFA + PKI | NCSC-WEB-005 |
| Tampering | API input | SQL injection | Parameterized queries | NCSC-WEB-004 |
| Info Disclosure | PII | Persoonsgegevens zichtbaar | Pseudonimisering | Publicatie V4.2 |
| DoS | API endpoints | Rate limit ontbreekt | Rate limiting | NCSC-WEB-010 |
| Elevation | Authorization | Te veel rechten | Least privilege | NCSC-BAS-006 |
## OWASP Top 10 → JuraRegel
| OWASP | JuraRegel check |
|---|---|
| A01 Broken Access Control | NCSC-BAS-006 |
| A02 Cryptographic Failures | NCSC-TLS-001 |
| A03 Injection | NCSC-WEB-004 |
| A04 Insecure Design | NORA-003 |
| A05 Security Misconfig | NCSC-BAS-005 |
