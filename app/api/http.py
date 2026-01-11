from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from app.core.container import Container
from app.core.exceptions import UserAlreadyExists

app = FastAPI()
container = Container("app/schemas/users.db")

class UserCreate(BaseModel):
    email: str

def get_user_service():
    return container.user_service()

def get_user_repo():
    return container.user_repo()

@app.post("/users", status_code=201)
def create_user(
    payload: UserCreate,
    service = Depends(get_user_service),
    repo = Depends(get_user_repo)
):
    try:
        user = service.register_user(payload.email)
        repo.save(user)
        
        return {"email": user.email}
    except UserAlreadyExists as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc)
        )