# Runbook — JuraRegel Rule API
## Alert: Rule API down
1. Check: curl http://127.0.0.1:<port>/v1/health
2. Restart: python3 use-cases/<domein>/api/app.py
3. If JREM load fail: check exports/*.json exists and validates

## Alert: CI gate failed
1. Run: bash ci/run-gates.sh use-cases/<domein>
2. Identify failed gate (1-14)
3. Fix issue (schema/test/brontraceability/acceptatie)

## Health Check All APIs
```bash
for port in 8490 8491 8492 8493 8494 8495 8496 8497 8498 8499 8500; do
  echo -n "Port $port: "; curl -s http://127.0.0.1:$port/v1/health | python3 -c "import json,sys; print(json.load(sys.stdin).get('status','DOWN'))" 2>/dev/null || echo "DOWN"
done
```
