from collections.abc import Sequence
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import Result, ScalarResult, Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Role, User


@dataclass
class UserRepository:
    _session: AsyncSession

    async def get_all(self) -> Sequence[User]:
        users: ScalarResult[User] = await self._session.scalars(select(User))
        return users.all()

    async def get_user_by_email(self, email: str) -> User | None:
        statement: Select[tuple[User]] = (
            select(User).options(selectinload(User.role).selectinload(Role.permissions))
        ).where(User.email == email)

        result: Result[tuple[User]] = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        return await self._session.get(User, user_id)

    async def create_user(self, name: str, lastname: str, password: str, email: str, id_role: int) -> User:
        user_created = User(name=name, lastname=lastname, password=password, email=email, id_role=id_role)

        self._session.add(user_created)

        await self._session.refresh(user_created)

        return user_created
