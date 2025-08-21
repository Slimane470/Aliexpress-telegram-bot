import os
import sqlite3
from typing import Any, Dict, List, Optional, Tuple


class Store:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._ensure_parent_dir()
        self._init_db()

    def _ensure_parent_dir(self) -> None:
        parent = os.path.dirname(self.db_path)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    chat_id INTEGER PRIMARY KEY,
                    categories TEXT DEFAULT '',
                    min_price REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def upsert_user(self, chat_id: int) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO users (chat_id) VALUES (?)
                ON CONFLICT(chat_id) DO NOTHING
                """,
                (chat_id,),
            )
            conn.commit()

    def set_categories(self, chat_id: int, categories: List[str]) -> None:
        normalized = ",".join(sorted({c.strip().lower() for c in categories if c.strip()}))
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO users (chat_id, categories) VALUES (?, ?)
                ON CONFLICT(chat_id) DO UPDATE SET categories=excluded.categories
                """,
                (chat_id, normalized),
            )
            conn.commit()

    def set_min_price(self, chat_id: int, min_price: float) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO users (chat_id, min_price) VALUES (?, ?)
                ON CONFLICT(chat_id) DO UPDATE SET min_price=excluded.min_price
                """,
                (chat_id, float(min_price)),
            )
            conn.commit()

    def get_user(self, chat_id: int) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT chat_id, categories, min_price FROM users WHERE chat_id = ?",
                (chat_id,),
            )
            row = cur.fetchone()
            if not row:
                return None
            categories = [c for c in (row[1] or "").split(",") if c]
            return {
                "chat_id": int(row[0]),
                "categories": categories,
                "min_price": float(row[2] or 0),
            }

    def get_all_users(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT chat_id, categories, min_price FROM users ORDER BY created_at ASC"
            )
            users: List[Dict[str, Any]] = []
            for row in cur.fetchall():
                categories = [c for c in (row[1] or "").split(",") if c]
                users.append(
                    {
                        "chat_id": int(row[0]),
                        "categories": categories,
                        "min_price": float(row[2] or 0),
                    }
                )
            return users