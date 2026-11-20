import sqlite3
from pathlib import Path

SCHEMA = Path(__file__).with_name("schema.sql")

def connect(db_path="data/monte_carlo.sqlite"):
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))
    return conn
