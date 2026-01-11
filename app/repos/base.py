from abc import ABC, abstractmethod
from app.domain.models import User

class UserRepository(ABC):
    @abstractmethod
    def exists(self, email: str) -> bool:
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        pass