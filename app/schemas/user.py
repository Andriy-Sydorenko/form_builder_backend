from typing import Annotated

from pydantic import BaseModel, EmailStr, HttpUrl, SecretStr, StringConstraints

from app.constants import EMAIL_MAX_LENGTH, EMAIL_MIN_LENGTH
from app.schemas.base import BaseValidatedModel


class UserUpdate(BaseValidatedModel):
    username: str | None = None
    password: SecretStr | None = None


class UserUpdateResponse(BaseModel):
    email: Annotated[EmailStr, StringConstraints(min_length=EMAIL_MIN_LENGTH, max_length=EMAIL_MAX_LENGTH)]
    username: str | None = None
    avatar_url: HttpUrl | None

    class Config:
        from_attributes = True
