# JuraRegel pilot deployment

JuraRegel is niet production-ready. De Compose-configuratie start alleen de
griffierecht-PoC en de publicatie/PII-pilot. TLS, OAuth/OIDC, persistent audit,
back-up, multi-instance rate limiting, SBOM en onafhankelijke juridische
accordering moeten buiten deze repository aantoonbaar zijn voordat productie
kan worden overwogen.

```bash
docker compose up --build
curl http://127.0.0.1:8490/v1/health
curl http://127.0.0.1:8493/v1/health
```

Zet `JURAREGEL_AUTH_ENABLED=true` alleen samen met een geheime
`JURAREGEL_API_KEY`. Dit is een PoC API-key-controle, geen OAuth2/OIDC.

Kubernetes/Helm is bewust verwijderd totdat de container-smoketest, identity,
persistent evidence store en operationele SLO's vaststaan.
