from .base import Base


class Token(Base):
    access_token: str
    token_type: str = "bearer"  # noqa: S105


class Tokens(Base):
    access_token: Token
    refresh_token: str
