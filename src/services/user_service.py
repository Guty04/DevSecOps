from collections.abc import Sequence
from dataclasses import dataclass

from src.database.models import User as UserDB
from src.errors import UserAlreadyExistError
from src.repositories import UserRepository
from src.schemas import User, UserCreate
from src.utils import hash_password


@dataclass
class UserService:
    _repository: UserRepository

    async def get_all(self) -> list[User]:
        users_db: Sequence[UserDB] = await self._repository.get_all()

        return [User.model_validate(user) for user in users_db]

    async def create_user(self, user_create: UserCreate) -> User:
        user_exist: UserDB | None = await self._repository.get_user_by_email(user_create.email)

        if user_exist:
            raise UserAlreadyExistError()

        hashed_password: str = hash_password(user_create.password)

        user_created: UserDB = await self._repository.create_user(
            name=user_create.name,
            lastname=user_create.lastname,
            password=hashed_password,
            email=user_create.email,
            id_role=1,
        )

        return User.model_validate(user_created)
