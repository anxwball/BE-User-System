"""
Simple dependency container.

Provide factory methods to obtain repository and service instances.
"""

from app.domain.services import UserService
from app.repos.sqlite import UserRepositorySQLite
from app.core.config import Settings

class Container:
    """Provide application wiring for tests and runtime.

    Initialize with a `db_path` and provide `user_repo()` and `user_service()`
    factories that create new instances on demand.
    """

    def __init__(self, settings: Settings):
        """Initialize the container with a `Settings` instance.

        This enforces a single source of configuration for the application
        and avoids legacy, ad-hoc parameters.
        """
        if not isinstance(settings, Settings):
            raise TypeError("Container requires a Settings instance")
        self._db_path = settings.db_path

    def user_repo(self) -> UserRepositorySQLite:
        """Return a new `UserRepositorySQLite` instance bound to `db_path`.

        This factory returns a fresh repository instance on each call. Callers
        should treat repository instances as short-lived; the container is
        responsible only for wiring and not for managing repository lifecycle.
        """

        return UserRepositorySQLite(self._db_path)

    def user_service(self) -> UserService:
        """Return a new `UserService` using the repository factory.

        The returned `UserService` is constructed with a repository instance
        from `user_repo()`. This keeps the service stateless with regard to
        persistence implementation and simplifies testing.
        """

        return UserService(self.user_repo())