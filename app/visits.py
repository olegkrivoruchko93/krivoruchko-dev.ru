import sqlite3
from pathlib import Path

from platformdirs import user_data_dir

from config import DATA_APP_AUTHOR, DATA_APP_NAME

_db_path: Path | None = None


def _database_path() -> Path:
    global _db_path
    if _db_path is not None:
        return _db_path

    data_dir = Path(user_data_dir(DATA_APP_NAME, DATA_APP_AUTHOR))
    data_dir.mkdir(parents=True, exist_ok=True)
    _db_path = data_dir / "visits.db"
    return _db_path


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_database_path(), timeout=5)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value INTEGER NOT NULL
        )
        """
    )
    conn.execute(
        "INSERT OR IGNORE INTO meta (key, value) VALUES ('visits', 0)"
    )
    return conn


def increment_visit_count() -> int:
    with _connect() as conn:
        conn.execute(
            "UPDATE meta SET value = value + 1 WHERE key = 'visits'"
        )
        row = conn.execute(
            "SELECT value FROM meta WHERE key = 'visits'"
        ).fetchone()
        conn.commit()
    return int(row[0]) if row else 0
