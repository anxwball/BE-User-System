"""
Pydantic DTOs for the HTTP API.

Define input and output shapes used by the HTTP endpoints.
"""

from pydantic import BaseModel, EmailStr, Field


class UserCreateDTO(BaseModel):
    """Represent input payload to create a user.

    Validate that `email` is a well-formed email address.
    """

    email: EmailStr = Field(..., description="Valid email address")


class UserResponseDTO(BaseModel):
    """Represent the API response after creating a user."""

    email: EmailStr