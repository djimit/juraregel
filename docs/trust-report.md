# JuraRegel Trust Report

**Datum:** 2026-07-05
**Versie:** 2.1.1
**Commit:** 4fd21b7

## Maturity Overview

| Level | Count | Description |
|-------|-------|-------------|
| L0-demo | 26 | Regelmatige exports, geen externe review | Example rules, no external review |
| L1-poc | 3 | Griffierecht, Publicatie, Toeslagen | Schema validates, tests pass, self-approved |
| L2-pilot | 0 | Independent legal review required |
| L3-production | 0 | Full assurance pipeline required |

## Flagship Use Case: Griffierecht

**Status:** L1-poc (closest to L2)
- Deterministic rule engine
- 36 rules with source references
- Regression tests between 2025/2026 versions
- Explainability + audit hashes
- **Blocker for L2:** No independent legal review

## CI Status

| Check | Status | Notes |
|-------|--------|-------|
| Schema validation | ✅ Pass | jrem-core.json + v1.1.0 |
| JREM validation | ✅ Pass | 0 errors, 0 warnings |
| BDD tests | ✅ Pass | 7/7 scenarios |
| CLI | ✅ Pass | All commands work |
| Legal review | ⚠️ Warn (PoC) / Fail (Pilot) | 29 self-approved, maturity-aware gating |

## Security Status

| Control | Status | Notes |
|---------|--------|-------|
| Auth | ✅ API key | JURAREGEL_API_KEY env var |
| CORS | ✅ Restricted | JURAREGEL_CORS_ORIGINS env var |
| Audit logging | ⚠️ Basic | Hash chain, no persistence |
| Rate limiting | ⚠️ In-memory | Not for production |
| TLS | ❌ Not implemented | Reverse proxy needed |
| OAuth2/OIDC | ❌ Not implemented | Planned for L3 |

## Known Limitations

1. All exports are self-approved (no independent legal review)
2. BIO2 evidence store is SQLite (PoC only)
3. No persistent audit logging
4. No production-grade authentication
5. CI not yet verified via GitHub Actions runs
6. No SBOM or dependency scanning

## Next Steps to L2

1. Independent legal review for Griffierecht
2. Evidence persistence for BIO2
3. Production CI verification
4. Threat model documentation
5. Security baseline assessment
