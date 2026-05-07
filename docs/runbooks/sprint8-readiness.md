# Sprint 8 Readiness Runbook

## What's now included
- Auth gate (`Authorization: Bearer <token>`) for platform APIs.
- Health (`/healthz`) and readiness (`/readyz`) probes.
- Docker Compose stack with API + Redis + Postgres.
- Real-time smoke test script.

## Local real-time test
1. Start stack:
   ```bash
   cd infra
   docker compose up --build
   ```
2. In new terminal, run smoke test:
   ```bash
   GENUI_API_TOKEN=dev-token ../scripts/realtime_smoke_test.sh http://127.0.0.1:8080
   ```
3. Expected results:
   - health returns `{"status":"ok"}`
   - decision has `decisionId`, `candidateId`, `manifest`
   - event returns `accepted`
   - memory includes dismissed candidate
   - audit query returns one record for the decisionId

## Security/perf hardening pending
- Replace static bearer token with OAuth/JWT validation.
- Wire Redis/Postgres adapters instead of in-memory stores.
- Add OTel traces/metrics export and SLO alerts.
- Add load test targets and chaos scenarios.
