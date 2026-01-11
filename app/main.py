import argparse

from app.core.config import load_settings
from app.core.logging import config_logging, get_logger

from app.core.container import Container
from app.core.exceptions import UserAlreadyExists

def main():
    settings = load_settings()
    config_logging(settings.debug)
    logger = get_logger(__name__)

    logger.debug("App starting in %s mode", settings.env)

    parser = argparse.ArgumentParser(description="User registration")
    
    parser.add_argument("--email", required=True)
    
    args = parser.parse_args()  
    container = Container("app/schemas/users.db")
    repo = container.user_repo()
    service = container.user_service()
    
    try:
        user = service.register_user(args.email)
        repo.save(user)

        logger.info("User created: %s", user.email)
    except UserAlreadyExists:
        logger.warning("Attempt to register duplicate user: %s", args.email)
        
        print("User already exists")

if __name__ == "__main__":
    main()