"""
Domain services.

Provide business use-cases for user registration.
"""

from uuid import uuid4
from app.domain.models import User
from app.core.exceptions import UserAlreadyExists


class UserService:
    """Provide user-related domain operations.

    Instantiate with a repository implementing the repository contract.
    """

    def __init__(self, repository):
        self.repository = repository

    def register_user(self, email: str) -> User:
        """Register a user with `email` and return the created `User`.

        Validate uniqueness using the repository and raise
        `UserAlreadyExists` when a duplicate is found.
        """

        if self.repository.exists(email):
            raise UserAlreadyExists(email)

        user = User(id=uuid4(), email=email)
        return user