from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field, condate
from src.database.models import Role


class UserModel(BaseModel):
    first_name: str = Field(default="", max_length=25)
    last_name: str = Field(default="", max_length=30)
    username: str = Field(min_length=6, max_length=12)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)
    phone_number: str = Field(default="", max_length=25)
    born_date: date | None
    description: str = Field(default="", max_length=250)


class UserResponse(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    username: str
    email: EmailStr
    phone_number: str | None
    born_date: date | None
    description: str | None
    avatar: str
    roles: Role
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserEmailModel(BaseModel):
    email: EmailStr


# class UserResponse(BaseModel):
#     id: int
#     username: str
#     email: str
#     avatar: str
#     role: Role

#     class Config:
#         from_attributes = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"