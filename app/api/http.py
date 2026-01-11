from fastapi import Depends, FastAPI, HTTPException

from app.core.container import Container
from app.api.schemas import UserCreateDTO, UserResponseDTO
from app.core.exceptions import UserAlreadyExists

app = FastAPI()
container = Container("app/schemas/users.db")

def get_user_service():
    return container.user_service()

def get_user_repo():
    return container.user_repo()

@app.post("/users", 
          status_code=201,
          response_model=UserResponseDTO
          )
def create_user(
    payload: UserCreateDTO,
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