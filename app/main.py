import argparse

from app.core.config import load_settings
from app.core.logging import config_logging, get_logger

from app.domain.services import UserService
from app.repos.memory import UserRepositoryInMemory
from app.core.exceptions import UserAlreadyExists

def main():
    settings = load_settings()
    config_logging(settings.debug)
    logger = get_logger(__name__)

    logger.debug("App starting in %s mode", settings.env)

    parser = argparse.ArgumentParser(description="User registration")
    parser.add_argument("--email", required=True)
    args = parser.parse_args()
    
    repository = UserRepositoryInMemory()
    service = UserService(repository)
    
    try:
        user = service.register_user(args.email)
        repository.save(user)
        logger.info("User created: %s", user.email)
    except UserAlreadyExists:
        logger.warning("Attempt to register duplicate user: %s", args.email)
        print("User already exists")

if __name__ == "__main__":
    main()