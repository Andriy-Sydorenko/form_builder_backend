from typing import Any

from fastapi import HTTPException, status
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user import UserRepository
from app.utils import ph


class UserService:
    IMMUTABLE_FIELDS = frozenset({"email"})

    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)

    async def get_user(
        self,
        filter_field: str,
        value: Any,
        selected_fields: list[str] | None = None,
        include_relations: list[str] | None = None,
    ) -> User:
        user = await self.user_repo.get_user(filter_field, value, selected_fields, include_relations)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def create_user(
        self,
        email: str,
        password: SecretStr,
        username: str | None = None,
        selected_fields: list[str] | None = None,
    ) -> User:
        existing = await self.user_repo.get_user("email", email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

        password_hash = ph.hash(password.get_secret_value())
        new_user = User(email=email, username=username, password_hash=password_hash)
        return await self.user_repo.create_user(new_user, selected_fields)

    async def update_user(self, user: User, data: dict, selected_fields: list[str]) -> User:
        # Check for immutable fields first
        if any(field in self.IMMUTABLE_FIELDS for field in data):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot update immutable fields: {', '.join(self.IMMUTABLE_FIELDS)}",
            )
        return await self.user_repo.update_user(user=user, data=data, selected_fields=selected_fields)

    async def delete_user(self, user_id: str):
        user = await self.get_user("id", user_id)
        await self.user_repo.delete_user(user)
