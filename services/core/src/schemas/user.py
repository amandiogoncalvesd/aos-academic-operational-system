from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    role: UserRole = UserRole.student
    institution_id: str | None = None
    avatar_url: str | None = None


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    avatar_url: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None
    institution_id: str | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    is_active: bool
    is_verified: bool
    last_login: datetime | None = None
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserPasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)


class UserPasswordReset(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class ForgotPassword(BaseModel):
    email: EmailStr
