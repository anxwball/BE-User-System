from app.repos.base import UserRepository

class UserRepositoryInMemory(UserRepository):
    """ 
    In-memory repository optimized for O(1) average lookup by email.
    """
    # Using dict to ensure average O(1) lookup for existence checks
    def __init__(self):
        self._users = {}
    
    def exists(self, email: str) -> bool:
        return email in self._users
    
    def save(self, user):
        self._users[user.email] = user