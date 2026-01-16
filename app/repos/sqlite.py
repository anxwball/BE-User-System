import sqlite3
import os
from app.repos.base import UserRepository

class UserRepositorySQLite(UserRepository):
    def __init__(self, db_path: str):
        self._db_path = db_path
        dirpath = os.path.dirname(self._db_path)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        self._create_table()

    def _execute(self, query: str, params=None, commit: bool = False, fetchone: bool = False, fetchall: bool = False):
        if params is None:
            params = ()
        conn = sqlite3.connect(self._db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if commit:
                conn.commit()
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()
            return None
        finally:
            conn.close()

    def _create_table(self):
        self._execute(
            "CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, email TEXT UNIQUE NOT NULL)",
            commit=True
        )

    def exists(self, email: str) -> bool:
        row = self._execute(
            "SELECT 1 FROM users WHERE email = ?",
            (email,),
            fetchone=True
        )
        return row is not None

    def save(self, user) -> None:
        # Persist both id and email. UUIDs are stored as text.
        self._execute(
            "INSERT INTO users (id, email) VALUES (?, ?)",
            (str(user.id), user.email),
            commit=True
        )