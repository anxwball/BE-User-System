import pytest
from app.domain.services import UserService
from app.repos.memory import UserRepositoryInMemory
from app.core.exceptions import UserAlreadyExists

def test_register_user_success():
    repo = UserRepositoryInMemory()
    service = UserService(repo)
    user = service.register_user("test@email.com")
    repo.save(user)

    assert user.email == "test@email.com"

def test_register_user_duplicate_email():
    repo = UserRepositoryInMemory()
    service = UserService(repo)
    user = service.register_user("test@email.com")
    repo.save(user)

    with pytest.raises(UserAlreadyExists):
        service.register_user("test@email.com")