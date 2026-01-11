import sqlite3
from app.repos.base import UserRepository

class UserRepositorySQLite(UserRepository):
    def __init__(self, db_path: str):
        self._conn = sqlite3.connect(db_path)
        self._create_table()

    def _get_cursor(self):
        return self._conn.cursor()
    
    def _execute(self, query: str, params = None, commit = False):
        cursor = self._get_cursor()
        
        if params is None:
            params = ()
        
        cursor.execute(query, params)

        if commit:
            self._conn.commit()
        
        return cursor


    def _create_table(self):
        self._execute(
            "CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY)",
            commit=True
        )

    def exists(self, email: str) -> bool:
        cursor = self._execute(
            "SELECT 1 FROM users WHERE email = ?",
            (email,)
        )

        return cursor.fetchone() is not None
    
    def save(self, user) -> None:
        self._execute(
            "INSERT INTO users (email) VALUES (?)",
            (user.email,),
            commit=True
        )