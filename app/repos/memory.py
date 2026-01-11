from app.repos.base import UserRepository

class UserRepositoryInMemory(UserRepository):
    def __init__(self):
        self._users = {}
    
    def exists(self, email: str) -> bool:
        return email in self._users
    
    def save(self, user):
        self._users[user.email] = user