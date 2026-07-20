from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class UserLogin(BaseModel):
    email: EmailStr
    password: str