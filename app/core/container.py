"""
Simple dependency container.

Provide factory methods to obtain repository and service instances.
"""

from app.domain.services import UserService
from app.repos.sqlite import UserRepositorySQLite
from app.core.config import Settings
from typing import Union


class Container:
    """Provide application wiring for tests and runtime.

    Initialize with a `db_path` and provide `user_repo()` and `user_service()`
    factories that create new instances on demand.
    """

    def __init__(self, settings: Union[Settings, str]):
        """Initialize the container with a `Settings` instance or a legacy db_path string.

        Passing a `Settings` object is preferred (it includes `db_path`).
        """
        if isinstance(settings, str):
            self._db_path = settings
        else:
            self._db_path = settings.db_path

    def user_repo(self) -> UserRepositorySQLite:
        """Return a new `UserRepositorySQLite` instance bound to `db_path`."""

        return UserRepositorySQLite(self._db_path)

    def user_service(self) -> UserService:
        """Return a new `UserService` using the repository factory."""

        return UserService(self.user_repo())