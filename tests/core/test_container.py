from app.core.container import Container
from app.domain.services import UserService
from app.repos.memory import UserRepositoryInMemory

def test_container_user_registration():
    container = Container(db_path=":memory:")
    service = container.user_service()
    
    assert isinstance(service, UserService)

class CustomContainer(Container):
    def __init__(self, db_path: str):
        super().__init__(db_path)

    def user_repo(self):
        return UserRepositoryInMemory()
    
def test_container_override_repo():
    container = CustomContainer(db_path="unused")
    service = container.user_service()

    assert isinstance(service, UserService)
    assert isinstance(service.repository, UserRepositoryInMemory)