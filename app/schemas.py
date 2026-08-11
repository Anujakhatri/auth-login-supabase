from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Credentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr | None = None
    role: str | None = None
    confirmed_at: str | None = None


class AuthResponse(BaseModel):
    user: UserResponse | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    token_type: str = "bearer"
    expires_in: int | None = None


class MessageResponse(BaseModel):
    message: str


class ProfileResponse(BaseModel):
    user: UserResponse
    message: str


class DashboardResponse(BaseModel):
    user_id: str
    message: str
    data: dict[str, Any]
