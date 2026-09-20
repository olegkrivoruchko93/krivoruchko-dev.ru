import sqlite3
from pathlib import Path

from platformdirs import user_data_dir

from config import DATA_APP_AUTHOR, DATA_APP_NAME

_data_dir = Path(user_data_dir(DATA_APP_NAME, DATA_APP_AUTHOR))
_data_dir.mkdir(parents=True, exist_ok=True)
_db_path = _data_dir / "data.db"


def _connect() -> sqlite3.Connection:
    return sqlite3.connect(_db_path, timeout=5)


def init_db() -> None:
    """Create tables if they don't exist. Call once at app startup."""
    conn = _connect()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS visitors (
                id INTEGER PRIMARY KEY,
                ip TEXT NOT NULL,
                visited_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def record_visit(user_ip, iso_utc) -> int:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO visitors (ip, visited_at) VALUES (?, ?)", 
            (user_ip, iso_utc)
        )
        conn.commit()
        row = conn.execute("SELECT COUNT(*) FROM visitors").fetchone()
    return int(row[0])
