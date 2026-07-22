# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅        |

## Reporting a Vulnerability

If you discover a security vulnerability in JuraRegel, please report it by:

1. **Email**: security@djimit.nl (preferred for sensitive issues)
2. **GitHub**: Create a private security advisory at https://github.com/djimit/juraregel/security/advisories

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We aim to respond within 48 hours and will keep you informed of our progress.

## Security Measures

JuraRegel implements the following security measures:

- **PII Redaction**: Automatic detection and redaction of personal data in AI output
- **Dependency Scanning**: Weekly automated dependency updates via Dependabot
- **Audit Trail**: Immutable evidence lineage for all AI-generated output
- **Approval Gates**: Multi-party approval for high-risk (L4/L5) AI outputs
- **Input Validation**: All API inputs validated against JSON Schema
- **Rate Limiting**: API rate limiting to prevent abuse

## Known Vulnerabilities

We track and remediate security vulnerabilities through:
- GitHub Dependabot alerts
- JLAIF Security Audit Framework
- Regular dependency updates
