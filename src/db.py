import os
import sqlite3
from typing import Optional, Sequence


SCHEMA_SQL = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS users (
    chat_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    language_code TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subscriptions (
    chat_id INTEGER PRIMARY KEY,
    category TEXT,
    max_price REAL,
    interval_min INTEGER,
    last_sent_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS delivered_deals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL,
    deal_id TEXT NOT NULL,
    delivered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(chat_id, deal_id)
);
"""


class Database:
    def __init__(self, db_path: str) -> None:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._initialize()

    def _initialize(self) -> None:
        with self._conn:
            self._conn.executescript(SCHEMA_SQL)

    def upsert_user(
        self,
        chat_id: int,
        username: Optional[str],
        first_name: Optional[str],
        last_name: Optional[str],
        language_code: Optional[str],
    ) -> None:
        with self._conn:
            self._conn.execute(
                """
                INSERT INTO users (chat_id, username, first_name, last_name, language_code)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(chat_id) DO UPDATE SET
                    username=excluded.username,
                    first_name=excluded.first_name,
                    last_name=excluded.last_name,
                    language_code=excluded.language_code
                """,
                (chat_id, username, first_name, last_name, language_code),
            )

    def upsert_subscription(
        self, chat_id: int, category: Optional[str], max_price: Optional[float], interval_min: int
    ) -> None:
        with self._conn:
            self._conn.execute(
                """
                INSERT INTO subscriptions (chat_id, category, max_price, interval_min)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(chat_id) DO UPDATE SET
                    category=excluded.category,
                    max_price=excluded.max_price,
                    interval_min=excluded.interval_min
                """,
                (chat_id, category, max_price, interval_min),
            )

    def delete_subscription(self, chat_id: int) -> None:
        with self._conn:
            self._conn.execute("DELETE FROM subscriptions WHERE chat_id = ?", (chat_id,))

    def get_subscription(self, chat_id: int) -> Optional[sqlite3.Row]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM subscriptions WHERE chat_id = ?", (chat_id,))
        return cur.fetchone()

    def list_subscriptions(self) -> Sequence[sqlite3.Row]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM subscriptions")
        return cur.fetchall()

    def mark_deal_delivered(self, chat_id: int, deal_id: str) -> None:
        with self._conn:
            self._conn.execute(
                "INSERT OR IGNORE INTO delivered_deals (chat_id, deal_id) VALUES (?, ?)",
                (chat_id, deal_id),
            )

    def was_deal_delivered(self, chat_id: int, deal_id: str) -> bool:
        cur = self._conn.cursor()
        cur.execute(
            "SELECT 1 FROM delivered_deals WHERE chat_id = ? AND deal_id = ?",
            (chat_id, deal_id),
        )
        return cur.fetchone() is not None