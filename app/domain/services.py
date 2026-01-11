from uuid import uuid4
from app.domain.models import User
from app.core.exceptions import UserAlreadyExists

class UserService:
    def __init__(self, repository):
        self.repository = repository

    def register_user(self, email:str) -> User:
        if self.repository.exists(email):
            raise UserAlreadyExists()
        
        user = User(id=uuid4(), email=email)
        return user