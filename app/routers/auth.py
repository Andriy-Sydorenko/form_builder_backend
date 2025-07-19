from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db, redis_client
from app.schemas.auth import (
    UserLogin,
    UserLoginResponse,
    UserRegister,
    UserRegisterResponse,
)
from app.services.auth import AuthService as auth_service
from app.services.user import UserService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register/")
async def register(register_data: UserRegister, db: Annotated[AsyncSession, Depends(get_db)]) -> UserRegisterResponse:
    user_service = UserService(db)
    user = await user_service.create_user(register_data.email, register_data.password, register_data.username)
    return UserRegisterResponse.model_validate(user)


@router.post("/login/")
async def login(
    login_data: UserLogin,
    db: Annotated[AsyncSession, Depends(get_db)],
    response: Response,
) -> UserLoginResponse:
    user_service = UserService(db)
    user = await user_service.get_user("email", login_data.email)
    token = auth_service.generate_jwt_token(str(user.id))
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        secure=True,
        samesite="none",  # Frontend on another domain
        path="/",
        max_age=settings.jwt_access_token_expire_minutes * 60,
    )
    redis_client.set(token, str(user.id), ex=settings.jwt_access_token_expire_minutes * 60)
    return UserLoginResponse(token=token)


@router.post("/logout/")
async def logout(user_id: Annotated[str, Depends(auth_service.decode_jwt)], response: Response):  # noqa
    response.delete_cookie(
        key="token",
        httponly=True,
        secure=True,
        samesite="none",  # Frontend on another domain
        path="/",
    )
    return {"message": "Logged out"}
