from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, computed_field


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)


class User(UserBase):
    id: UUID | None = None
    name: str
    last_name: str
    email: EmailStr

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.name} {self.last_name}"


class UserCreate(UserBase):
    name: str
    lastname: str
    email: EmailStr
    password: str = Field(min_length=8)
