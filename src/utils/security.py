from datetime import UTC, datetime, timedelta
from typing import Any

from jwt import decode, encode  # type:ignore[misc]
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

from src.configurations import configuration

_password_hash = PasswordHash((Argon2Hasher(),))


def hash_password(password: str) -> str:
    return _password_hash.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return _password_hash.verify(password=plain, hash=hashed)


def create_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    if not expires_delta:
        expires_delta = timedelta(minutes=configuration.ACCESS_TOKEN_EXPIRES)

    expire: datetime = datetime.now(UTC) + expires_delta

    payload = {**data, "exp": expire}

    return encode(
        payload,
        configuration.SECRET_KEY,
        algorithm=configuration.JWT_ALGORITHM,
    )


def decode_token(token: str) -> dict[str, Any]:
    return decode(
        token,
        configuration.SECRET_KEY,
        algorithms=[configuration.JWT_ALGORITHM],
    )
