# JuraRegel Productie Deployment

## Environment Variables

| Variable | Default | Effect |
|---|---|---|
| `JURAREGEL_TLS_KEY` | (none) | Path to TLS private key. Enables HTTPS. |
| `JURAREGEL_TLS_CERT` | (none) | Path to TLS certificate. Enables HTTPS. |
| `JURAREGEL_AUTH_ENABLED` | (none) | Set to `true` to enable OAuth 2.0 token validation. |
| `JURAREGEL_RATE_LIMIT` | (none) | Format: `100/minute`. Enables rate limiting per IP. |
| `JURAREGEL_METRICS_ENABLED` | (none) | Set to `true` to expose `/metrics` endpoint (Prometheus). |
| `JURAREGEL_LOG_FORMAT` | `plain` | Set to `json` for structured JSON logging. |

## Docker Productie

```bash
# With TLS + auth + rate limiting + metrics
JURAREGEL_TLS_KEY=/certs/key.pem \
JURAREGEL_TLS_CERT=/certs/cert.pem \
JURAREGEL_AUTH_ENABLED=true \
JURAREGEL_RATE_LIMIT=100/minute \
JURAREGEL_METRICS_ENABLED=true \
JURAREGEL_LOG_FORMAT=json \
docker compose up
```

## Kubernetes (Helm)

```bash
helm install juraregel ./helm/juraregel \
  --set tls.enabled=true \
  --set tls.key=/certs/key.pem \
  --set tls.cert=/certs/cert.pem \
  --set auth.enabled=true \
  --set rateLimit=100/minute \
  --set metrics.enabled=true
```

## Prometheus + Grafana

```bash
# Start Prometheus + Grafana alongside JuraRegel
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up
```

## Security Checklist

- [ ] TLS 1.2+ (NCSC-TLS-001) — JURAREGEL_TLS_KEY + JURAREGEL_TLS_CERT
- [ ] OAuth 2.0 (NL GOV Assurance Profile) — JURAREGEL_AUTH_ENABLED=true
- [ ] Rate limiting (NCSC-WEB-010) — JURAREGEL_RATE_LIMIT=100/minute
- [ ] Metrics (NCSC-BAS-008) — JURAREGEL_METRICS_ENABLED=true
- [ ] Structured logging — JURAREGEL_LOG_FORMAT=json
- [ ] CORS configured — already in api_base.py
- [ ] Health checks — GET /v1/health per API
- [ ] Audit trail — inputHash + rulesetHash + timestamp per request
