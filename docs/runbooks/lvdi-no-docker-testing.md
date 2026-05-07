# LVDI / No-Docker Testing Guide

Use this when Docker is unavailable.

## 1) Start API locally
```bash
GENUI_API_TOKEN=dev-token GENUI_SIGNING_KEY=dev-signing-key GENUI_DB_PATH=/tmp/genui-local.db ./scripts/run_local_lvdi.sh
```

## 2) In another terminal run realtime smoke
```bash
GENUI_API_TOKEN=dev-token ./scripts/realtime_smoke_test.sh http://127.0.0.1:8080
```

## 3) Run automated tests
```bash
python -m unittest discover -s tests_py -p 'test_*.py' -v
npm test
```

## Optional signed-request test (no bearer token)
```bash
python - <<'PY'
import json, hmac, urllib.request
from hashlib import sha256
body = json.dumps({"appId":"employee-portal","channel":"web","surface":"employee-dashboard","slot":"dashboard-hero","employeeId":"E-SIGNED","context":{}}).encode()
sig = hmac.new(b'dev-signing-key', body, sha256).hexdigest()
req = urllib.request.Request('http://127.0.0.1:8080/v1/decisions/evaluate', data=body, headers={'Content-Type':'application/json','X-GenUI-Signature':sig}, method='POST')
print(urllib.request.urlopen(req).read().decode())
PY
```
