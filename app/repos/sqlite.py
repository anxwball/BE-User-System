"""
SQLite repository implementation.

Provide a concrete `UserRepository` backed by a local SQLite database.
"""

import sqlite3
import os
from app.repos.base import UserRepository


class UserRepositorySQLite(UserRepository):
    """Persist users into a SQLite database.

    Create the database directory if required and ensure the users table
    exists on initialization.
    """

    def __init__(self, db_path: str):
        self._db_path = db_path
        dirpath = os.path.dirname(self._db_path)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        self._create_table()

    def _execute(self, query: str, params=None, commit: bool = False, fetchone: bool = False, fetchall: bool = False):
        """Execute `query` against the SQLite database and return results.

        Use `commit=True` to commit changes. Use `fetchone=True` or
        `fetchall=True` to return rows.
        """

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
        """Create the `users` table if it does not exist."""

        self._execute(
            "CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, email TEXT UNIQUE NOT NULL)",
            commit=True
        )

    def exists(self, email: str) -> bool:
        """Return True if a user with `email` exists in the table."""

        row = self._execute(
            "SELECT 1 FROM users WHERE email = ?",
            (email,),
            fetchone=True
        )
        return row is not None

    def save(self, user) -> None:
        """Persist `user` by storing `id` and `email`.

        Store UUIDs as text to keep the schema simple.
        """

        # Persist both id and email. UUIDs are stored as text.
        self._execute(
            "INSERT INTO users (id, email) VALUES (?, ?)",
            (str(user.id), user.email),
            commit=True
        )