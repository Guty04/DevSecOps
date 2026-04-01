from dataclasses import dataclass
from datetime import timedelta
from typing import Any
from uuid import UUID

from src.database.models import User
from src.errors import AuthenticationError, AuthorizationError, InvalidTokenError, UserNotFoundError
from src.repositories import UserRepository
from src.schemas import Token, Tokens
from src.utils import create_token, decode_token, verify_password


@dataclass
class AuthService:
    _repository: UserRepository

    async def authenticate_user(self, email: str, password: str) -> User:
        user: User | None = await self._repository.get_user_by_email(email=email)

        if user is None or not user.is_active:
            raise UserNotFoundError()

        if not verify_password(plain=password, hashed=user.password):
            raise AuthenticationError()

        return user

    async def get_current_user(self, access_token: str, required_scopes: set[str]) -> User:
        try:
            payload: dict[str, Any] = decode_token(token=access_token)

        except InvalidTokenError as token_error:
            raise AuthenticationError() from token_error

        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise AuthenticationError()

        user: User | None = await self._repository.get_user_by_id(UUID(user_id))

        if user is None or not user.is_active:
            raise AuthenticationError()

        user_permissions: set[str] = {permission.name for permission in user.role.permissions}

        if not required_scopes.issubset(user_permissions):
            raise AuthorizationError()

        return user

    async def refresh_token(self, token: str) -> Token:
        try:
            token_data: dict[str, Any] = decode_token(token)

        except InvalidTokenError as token_error:
            raise AuthenticationError() from token_error

        if token_data.get("type") != "refresh":
            raise AuthenticationError()

        user_id: str | None = token_data.get("sub")

        if user_id is None:
            raise AuthenticationError()

        user: User | None = await self._repository.get_user_by_id(UUID(user_id))

        if user is None:
            raise AuthenticationError()

        if not user.is_active:
            raise AuthorizationError()

        return Token(access_token=self.create_access_token(user))

    async def login(self, email: str, password: str) -> Tokens:
        user: User = await self.authenticate_user(email, password)

        return Tokens(
            access_token=Token(access_token=self.create_access_token(user)),
            refresh_token=self.create_refresh_token(user),
        )

    def create_access_token(self, user: User) -> str:
        return create_token(
            data={"sub": str(user.id), "name": f"{user.name} {user.lastname}", "role": user.role.name, "type": "access"}
        )

    def create_refresh_token(self, user: User) -> str:
        return create_token(
            data={"sub": str(user.id), "type": "refresh"},
            expires_delta=timedelta(hours=24),
        )
