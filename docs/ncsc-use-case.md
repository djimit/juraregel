# NCSC Use Case — ICT-beveiligingsrichtlijnen

**Als** security engineer of CISO **wil ik** automatisch valideren of mijn systemen voldoen aan de NCSC ICT-beveiligingsrichtlijnen **zodat** ik niet handmatig 32 richtlijnen hoef te checken.

| Rol | Probleem | Oplossing |
|---|---|---|
| Security engineer | 32 NCSC richtlijnen handmatig checken | Rule API checkt per richtlijn: compliant ja/nee |
| CISO | Onbekend welke richtlijnen nog open staan | Compliance rapport per categorie (TLS, webapp, basisprincipes) |
| Web developer | NCSC webapp richtlijnen onduidelijk | Check input validatie, output encoding, CSRF, CSP, rate limiting |
| SRE-er | NCSC TLS richtlijnen niet systematisch | Check TLS 1.2+, cipher suites, HSTS, certificate pinning |
| DevSecOps | Basisprincipes niet in CI/CD | Check B1-B10 + Cybersecuritybeeld 2025 in pipeline |

32 richtlijnen in 3 categorieën:
- **TLS** (8): TLS 1.2 min, TLS 1.3 voorkeur, sterke cipher suites, ECDSA, RSA 2048+, HSTS, cert pinning, OCSP
- **Webapplicaties** (10): input validatie, output encoding, CSRF, SQL injection, auth, session, CSP, error handling, file upload, rate limiting
- **Basisprincipes** (14): risicoanalyse, behandelplan, DevSecOps, technische standaarden, least privilege, defense in depth, monitoring, patch management, incident response, MFA, backups, netwerksegmentatie, Cybersecuritybeeld 2025

Bron: [ncsc.nl/documenten](https://www.ncsc.nl/documenten/publicaties/2025/juni/01/ict-beveiligingsrichtlijnen-voor-transport-layer-security-2025-05) | [ncsc.nl/onderwerpen](https://www.ncsc.nl/onderwerpen/ict-beveiligingsrichtlijnen-voor-webapplicaties) | [ncsc.nl/basisprincipes](https://www.ncsc.nl/basisprincipes)

Rule API op `localhost:8500`. 17 tests. 14 CI gates.

## Functiehuis Rijksoverheid Rollen

| Rol | Probleem | Oplossing |
|---|---|---|
| Security engineer | 32 NCSC richtlijnen handmatig checken | Rule API checkt per richtlijn |
| CISO | Onbekend wat open staat | Compliance rapport per categorie (TLS, webapp, basisprincipes) |
| Web developer | Webapp richtlijnen onduidelijk | Check input validatie, XSS, CSRF, CSP, rate limiting |
| SRE-er | TLS richtlijnen niet systematisch | Check TLS 1.2+, cipher suites, HSTS, cert pinning |
| DevSecOps | Basisprincipes niet in CI/CD | Check B1-B10 + Cybersecuritybeeld 2025 in pipeline |

