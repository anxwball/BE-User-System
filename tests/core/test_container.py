from app.core.container import Container
from app.core.config import Settings
from app.domain.services import UserService
from app.repos.memory import UserRepositoryInMemory

def test_container_user_registration():
    settings = Settings(env="test", debug=True, secret_key=None, db_path=":memory:")
    container = Container(settings)
    service = container.user_service()
    
    assert isinstance(service, UserService)

class CustomContainer(Container):
    def __init__(self, settings: Settings):
        super().__init__(settings)

    def user_repo(self):
        return UserRepositoryInMemory()
    
def test_container_override_repo():
    settings = Settings(env="test", debug=True, secret_key=None, db_path="unused")
    container = CustomContainer(settings)
    service = container.user_service()

    assert isinstance(service, UserService)
    assert isinstance(service.repository, UserRepositoryInMemory)