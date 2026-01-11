from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.domain.services import UserService
from app.repos.sqlite import UserRepositorySQLite
from app.core.exceptions import UserAlreadyExists

app = FastAPI()

class UserCreate(BaseModel):
    email: str

@app.post("/users", status_code=201)
def create_user(payload: UserCreate):
    repo = UserRepositorySQLite("app/schemas/users.db")
    service = UserService(repo)

    try:
        user = service.register_user(payload.email)
        repo.save(user)

        return {"email": user.email}
    except UserAlreadyExists as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc)
        )