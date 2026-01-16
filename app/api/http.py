"""
HTTP adapter using FastAPI.

Expose API endpoints and wire HTTP-level dependencies to domain services.
"""

from fastapi import Depends, FastAPI, HTTPException
import sys
import tempfile
from fastapi.security import OAuth2PasswordRequestForm

from app.api.auth import get_current_user_email
from app.core.container import Container
from app.core.config import load_settings, Settings
from app.api.schemas import UserCreateDTO, UserResponseDTO
from app.core.exceptions import UserAlreadyExists
from app.core.security import create_access_token

app = FastAPI()


settings = load_settings()

if "pytest" in sys.modules:
    _tmp_db = tempfile.NamedTemporaryFile(delete=False)
    # create a settings instance that points to the temp DB for tests
    settings = Settings(env=settings.env, debug=settings.debug, secret_key=settings.secret_key, db_path=_tmp_db.name)

container = Container(settings)


def get_user_service():
    """Return a `UserService` instance from the application container."""

    return container.user_service()


def get_user_repo():
    """Return a `UserRepository` instance from the application container."""

    return container.user_repo()


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Create and return a bearer token for `form_data.username`.

    This endpoint is intentionally minimal — it demonstrates token
    generation for testing and does not validate credentials.
    """

    access_token = create_access_token(subject=form_data.username, secret_key=settings.secret_key)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.post("/users", 
          status_code=201,
          response_model=UserResponseDTO
          )
def create_user(
    payload: UserCreateDTO,
    current_user: str = Depends(get_current_user_email),
    service = Depends(get_user_service),
    repo = Depends(get_user_repo)
):
    """Register a new user using `payload.email`.

    Use the domain `UserService` to enforce business rules and persist the
    returned `User` via the repository. Raise HTTP 409 on duplicates.
    """

    try:
        user = service.register_user(payload.email)
        repo.save(user)

        return UserResponseDTO(email = user.email)
    except UserAlreadyExists as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc)
        )