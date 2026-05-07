import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.getenv('GENUI_DB_PATH', '')

def is_sqlite_enabled() -> bool:
    return bool(DB_PATH)

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db() -> None:
    if not is_sqlite_enabled():
        return
    with get_conn() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS memory (employee_id TEXT PRIMARY KEY, payload TEXT NOT NULL)')
        conn.execute('CREATE TABLE IF NOT EXISTS audit (decision_id TEXT, employee_id TEXT, payload TEXT NOT NULL)')
