from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.auth import get_current_user_email
from app.core.container import Container
from app.api.schemas import UserCreateDTO, UserResponseDTO
from app.core.exceptions import UserAlreadyExists
from app.core.security import create_access_token

app = FastAPI()
container = Container("app/schemas/users.db")

def get_user_service():
    return container.user_service()

def get_user_repo():
    return container.user_repo()

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = create_access_token(subject=form_data.username)
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
    try:
        user = service.register_user(payload.email)
        repo.save(user)
        
        return UserResponseDTO(email = user.email)
    except UserAlreadyExists as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc)
        )