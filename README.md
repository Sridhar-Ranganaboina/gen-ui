# gen-ui

## Is it fully production ready?
Not fully. We have started final production hardening with auth improvements, persistent local storage option (SQLite), health/readiness probes, structured logging, and non-Docker runtime/testing paths.

## Production hardening started
- Auth: bearer token and HMAC signed-request mode.
- Persistence: optional SQLite backend via `GENUI_DB_PATH`.
- Operability: `/healthz`, `/readyz`, structured logs.
- Runtime options: Docker compose **or** local no-Docker (LVDI compatible).

## APIs
- `POST /v1/decisions/evaluate`
- `POST /v1/events/interactions`
- `GET /v1/audit?decisionId=...`
- `GET /v1/memory/{employeeId}`
- `GET /healthz`
- `GET /readyz`

## LVDI / no-Docker quick start
```bash
GENUI_API_TOKEN=dev-token GENUI_SIGNING_KEY=dev-signing-key GENUI_DB_PATH=/tmp/genui-local.db ./scripts/run_local_lvdi.sh
```
Then in another terminal:
```bash
GENUI_API_TOKEN=dev-token ./scripts/realtime_smoke_test.sh http://127.0.0.1:8080
```

## Tests
```bash
python -m unittest discover -s tests_py -p 'test_*.py' -v
npm test
```

See detailed runbooks:
- `docs/runbooks/sprint8-readiness.md`
- `docs/runbooks/lvdi-no-docker-testing.md`
