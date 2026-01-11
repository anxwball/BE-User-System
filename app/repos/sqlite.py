import sqlite3
from app.repos.base import UserRepository

class UserRepositorySQLite(UserRepository):
    def __init__(self, db_path: str):
        self._db_path = db_path
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
            "CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY)",
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
        self._execute(
            "INSERT INTO users (email) VALUES (?)",
            (user.email,),
            commit=True
        )