"""
Application entrypoints.

Expose the FastAPI `app` for ASGI servers while keeping the CLI `main()`
function for one-off command-line user registration.
"""

import argparse

from app.core.config import load_settings
from app.core.logging import config_logging, get_logger

from app.core.container import Container
from app.core.exceptions import UserAlreadyExists

# `uvicorn app.main:app --reload`
from app.api.http import app as app


def main():
    """Run CLI registration flow.

    Load settings, configure logging, build application wiring and attempt
    to register the email provided via the `--email` argument.
    """
    settings = load_settings()
    config_logging(settings.debug)
    logger = get_logger(__name__)

    logger.debug("App starting in %s mode", settings.env)

    parser = argparse.ArgumentParser(description="User registration")
    
    parser.add_argument("--email", required=True)
    
    args = parser.parse_args()  
    container = Container(settings)
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