from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.user import UserUpdate, UserUpdateResponse
from app.services.auth import AuthService as auth_service
from app.services.user import UserService


router = APIRouter(prefix="/me", tags=["me"])


@router.patch("/")
async def update_user(
    user_update: UserUpdate,
    user_id: Annotated[str, Depends(auth_service.decode_jwt)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserUpdateResponse:
    user_service = UserService(db)
    user = await user_service.get_user("id", user_id)
    await user_service.update_user(user, user_update.model_dump(exclude_none=True), ["email", "username"])
    return UserUpdateResponse.model_validate(user)
