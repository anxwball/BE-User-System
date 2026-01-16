"""
Simple dependency container.

Provide factory methods to obtain repository and service instances.
"""

from app.domain.services import UserService
from app.repos.sqlite import UserRepositorySQLite


class Container:
    """Provide application wiring for tests and runtime.

    Initialize with a `db_path` and provide `user_repo()` and `user_service()`
    factories that create new instances on demand.
    """

    def __init__(self, db_path: str):
        self._db_path = db_path

    def user_repo(self):
        """Return a new `UserRepositorySQLite` instance bound to `db_path`."""

        return UserRepositorySQLite(self._db_path)

    def user_service(self):
        """Return a new `UserService` using the repository factory."""

        return UserService(self.user_repo())