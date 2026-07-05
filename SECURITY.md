# Security Policy

## Supported Versions

JuraRegel is een project in ontwikkeling. Alleen de laatste main branch wordt ondersteund.

## Reporting a Vulnerability

Security issues kunnen worden gemeld via GitHub Issues met het label `security`.

## Security Model

### MCP Server

- **Protocol:** stdio (stdin/stdout)
- **Authenticatie:** API key via `AUTH_API_KEY` environment variable
- **Autorisatie:** geen (single-tenant)
- **Audit logging:** geen (gepland voor v3.0)

### API Servers (use cases)

- **Auth:** Bearer token validation
- **CORS:** restricted to configured origins
- **Rate limiting:** in-memory per IP
- **TLS:** via reverse proxy (nginx/traefik)

## Known Limitations

- Geen OAuth2/OIDC integratie
- Geen audit logging in productie
- Geen rate limiting achter load balancer
- In-memory storage (geen persistentie)

## Dependencies

- Python 3.12+
- FastAPI
- Qdrant client
- pytest-bdd

## Recommendations for Production

1. Implementeer echte OAuth2/OIDC via JWKS
2. Voeg audit logging toe (append-only storage)
3. Gebruik Redis voor rate limiting
4. Implementeer tenant isolation
5. Voeg SBOM generation toe
