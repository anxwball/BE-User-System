"""
Repository interfaces.

Define repository contracts used by domain services so persistence can be
swapped without changing domain code.
"""

from abc import ABC, abstractmethod
from app.domain.models import User


class UserRepository(ABC):
    """Define the API a user repository must implement.

    - `exists(email)` should return True when a user with `email` already
      exists in the data store.
    - `save(user)` should persist the provided `User` instance.
    """

    @abstractmethod
    def exists(self, email: str) -> bool:
        """Return True if `email` exists in the repository."""

    @abstractmethod
    def save(self, user: User) -> None:
        """Persist `user` to the repository."""