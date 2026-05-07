import json
from services_py.storage import get_conn, is_sqlite_enabled

AUDIT_LOG: list[dict] = []

def append_audit(entry: dict) -> None:
    AUDIT_LOG.append(entry)
    if is_sqlite_enabled():
        with get_conn() as conn:
            conn.execute('INSERT INTO audit (decision_id, employee_id, payload) VALUES (?, ?, ?)', (entry.get('decisionId'), entry.get('employeeId'), json.dumps(entry)))

def get_audit() -> list[dict]:
    if is_sqlite_enabled():
        with get_conn() as conn:
            rows = conn.execute('SELECT payload FROM audit').fetchall()
            return [json.loads(r[0]) for r in rows]
    return AUDIT_LOG
