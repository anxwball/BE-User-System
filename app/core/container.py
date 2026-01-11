from app.domain.services import UserService
from app.repos.sqlite import UserRepositorySQLite

class Container:
    def __init__(self, db_path: str):
        self._db_path = db_path
    
    def user_repo(self):
        return UserRepositorySQLite(self._db_path)
    
    def user_service(self):
        return UserService(self.user_repo())