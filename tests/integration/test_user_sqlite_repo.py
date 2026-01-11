import os
import tempfile
import pytest

from app.domain.services import UserService
from app.repos.sqlite import UserRepositorySQLite
from app.core.exceptions import UserAlreadyExists

def test_user_persistence_in_sqlite():
    with tempfile.NamedTemporaryFile(delete=False) as db_file:
        db_path = db_file.name

    try:
        repo = UserRepositorySQLite(db_path)
        service = UserService(repo)
        user = service.register_user("sqlite@email.com")
        repo.save(user)

        assert repo.exists(user.email)
    finally:
        os.remove(db_path)


def test_register_user_duplicate_email_with_sqlite():
    with tempfile.NamedTemporaryFile(delete=False) as db_file:
        db_path = db_file.name

    try:
        repo = UserRepositorySQLite(db_path)
        service = UserService(repo)
        user = service.register_user("sqlitedup@email.com")
        repo.save(user)

        with pytest.raises(UserAlreadyExists):
            service.register_user("sqlitedup@email.com")
    finally:
        os.remove(db_path)

def test_empty_sqlite_repository_starts_clean():
    with tempfile.NamedTemporaryFile(delete=False) as db_file:
        db_path = db_file.name

    try:
        repo = UserRepositorySQLite(db_path)

        assert not repo.exists("nobody@example.com")
    finally:
        os.remove(db_path)