#!/usr/bin/env bash
set -euo pipefail
BASE_URL=${1:-http://127.0.0.1:8080}
TOKEN=${GENUI_API_TOKEN:-dev-token}

echo "[1] Health"
curl -s "$BASE_URL/healthz" | jq .

echo "[2] Decision"
DECISION=$(curl -s -X POST "$BASE_URL/v1/decisions/evaluate" \
  -H "Authorization: Bearer $TOKEN" -H 'content-type: application/json' \
  -d '{"appId":"employee-portal","channel":"web","surface":"employee-dashboard","slot":"dashboard-hero","employeeId":"E777","context":{"roleContext":{"isManager":true}}}')
echo "$DECISION" | jq .
DECISION_ID=$(echo "$DECISION" | jq -r '.decisionId')
CANDIDATE_ID=$(echo "$DECISION" | jq -r '.candidateId')

echo "[3] Event"
curl -s -X POST "$BASE_URL/v1/events/interactions" \
  -H "Authorization: Bearer $TOKEN" -H 'content-type: application/json' \
  -d "{\"eventType\":\"dismiss\",\"employeeId\":\"E777\",\"slot\":\"dashboard-hero\",\"timestamp\":\"2026-05-07T00:00:00Z\",\"candidateId\":\"$CANDIDATE_ID\"}" | jq .

echo "[4] Memory"
curl -s "$BASE_URL/v1/memory/E777" -H "Authorization: Bearer $TOKEN" | jq .

echo "[5] Audit"
curl -s "$BASE_URL/v1/audit?decisionId=$DECISION_ID" -H "Authorization: Bearer $TOKEN" | jq .

echo "Smoke test completed"
