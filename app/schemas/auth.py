from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, SecretStr, StringConstraints

from app.constants import EMAIL_MAX_LENGTH, EMAIL_MIN_LENGTH
from app.schemas.base import BaseValidatedModel


class UserRegister(BaseValidatedModel):
    email: Annotated[EmailStr, StringConstraints(min_length=EMAIL_MIN_LENGTH, max_length=EMAIL_MAX_LENGTH)]
    password: SecretStr = Field(..., min_length=8)
    username: str | None = Field(None, min_length=3)


class UserRegisterResponse(BaseModel):
    email: Annotated[EmailStr, StringConstraints(min_length=EMAIL_MIN_LENGTH, max_length=EMAIL_MAX_LENGTH)]
    username: str | None = Field(None, min_length=3)

    class Config:
        from_attributes = True


class UserLogin(BaseValidatedModel):
    email: Annotated[EmailStr, StringConstraints(min_length=EMAIL_MIN_LENGTH, max_length=EMAIL_MAX_LENGTH)]
    password: SecretStr = Field(..., min_length=8)


class UserLoginResponse(BaseModel):
    token: str
    token_type: str = "bearer"
