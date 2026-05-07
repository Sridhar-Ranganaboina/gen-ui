import json
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from services_py.audit import append_audit, get_audit
from services_py.auth import is_authorized
from services_py.memory import get_memory, update_memory_from_event
from services_py.orchestrator import evaluate_decision
from services_py.storage import init_db

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
init_db()

class Handler(BaseHTTPRequestHandler):
    def _json(self, code: int, payload: dict | list):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _auth_or_401(self, body: bytes = b''):
        if not is_authorized(self.headers, body):
            self._json(401, {"error": "unauthorized"})
            return False
        return True

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length) if length > 0 else b"{}"
        if not self._auth_or_401(raw_body):
            return
        payload = json.loads(raw_body)
        if self.path == "/v1/decisions/evaluate":
            decision = evaluate_decision(payload)
            append_audit({"decisionId": decision["decisionId"], "employeeId": payload["employeeId"], "slot": payload["slot"], "reasonCodes": decision["reasonCodes"], "variant": decision.get("experiment", {}).get("variant")})
            logging.info('decision_id=%s employee_id=%s slot=%s', decision['decisionId'], payload['employeeId'], payload['slot'])
            return self._json(200, decision)
        if self.path == "/v1/events/interactions":
            memory = update_memory_from_event(payload)
            return self._json(202, {"status": "accepted", "memoryVersion": memory.get("memoryVersion", 0) + 1})
        return self._json(404, {"error": "not found"})

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/healthz":
            return self._json(200, {"status": "ok"})
        if parsed.path == "/readyz":
            return self._json(200, {"status": "ready"})

        if not self._auth_or_401():
            return

        if parsed.path == "/v1/audit":
            decision_id = parse_qs(parsed.query).get("decisionId", [None])[0]
            audits = get_audit()
            if decision_id:
                audits = [a for a in audits if a.get("decisionId") == decision_id]
            return self._json(200, audits)
        if parsed.path.startswith('/v1/memory/'):
            employee_id = parsed.path.split('/')[-1]
            return self._json(200, get_memory(employee_id))
        return self._json(404, {"error": "not found"})

    def log_message(self, format, *args):
        return

def create_server(port: int = 0):
    return ThreadingHTTPServer(("0.0.0.0", port), Handler)
