from uuid import UUID

from pydantic import EmailStr, Field, computed_field

from .base import Base


class User(Base):
    id: UUID | None = Field(default=None, description="")
    name: str
    last_name: str
    email: EmailStr

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.name} {self.last_name}"


class UserCreate(User):
    name: str
    lastname: str
    email: EmailStr
    password: str = Field(min_length=8)
