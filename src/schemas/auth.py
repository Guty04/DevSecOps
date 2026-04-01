from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"  # noqa: S105


class Tokens(BaseModel):
    access_token: Token
    refresh_token: str
