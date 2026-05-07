import json
from services_py.storage import get_conn, is_sqlite_enabled

MEMORY_STORE: dict[str, dict] = {}

def get_memory(employee_id: str) -> dict:
    if is_sqlite_enabled():
      with get_conn() as conn:
          row = conn.execute('SELECT payload FROM memory WHERE employee_id = ?', (employee_id,)).fetchone()
          if row:
              return json.loads(row[0])
    return MEMORY_STORE.get(employee_id, {
        "employeeId": employee_id,
        "roleContext": {},
        "behavioralMemory": {"recentDismissedCards": []},
    })

def seed_memory(employee_id: str, value: dict) -> None:
    if is_sqlite_enabled():
        with get_conn() as conn:
            conn.execute('REPLACE INTO memory (employee_id, payload) VALUES (?, ?)', (employee_id, json.dumps(value)))
    MEMORY_STORE[employee_id] = value

def update_memory_from_event(event: dict) -> dict:
    memory = get_memory(event["employeeId"])
    if event.get("eventType") == "dismiss" and event.get("candidateId"):
        memory.setdefault("behavioralMemory", {}).setdefault("recentDismissedCards", []).append(event["candidateId"])
    seed_memory(event["employeeId"], memory)
    return memory
