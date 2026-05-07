#!/usr/bin/env bash
set -euo pipefail
export GENUI_API_TOKEN=${GENUI_API_TOKEN:-dev-token}
export GENUI_SIGNING_KEY=${GENUI_SIGNING_KEY:-dev-signing-key}
export GENUI_DB_PATH=${GENUI_DB_PATH:-/tmp/genui-local.db}
python -m services_py.run_server
