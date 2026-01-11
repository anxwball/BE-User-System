from pydantic import BaseModel, EmailStr, Field

class UserCreateDTO(BaseModel):
    email: EmailStr = Field(..., description="Valid email address")

class UserResponseDTO(BaseModel):
    email: EmailStr