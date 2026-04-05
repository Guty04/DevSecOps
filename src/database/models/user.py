from typing import ClassVar
from uuid import UUID

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .role import Role


class User(Base):
    __tablename__: str = "user"
    __table_args__: ClassVar = {"comment": "Platform users (PMs, Admins)"}

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    name: Mapped[str] = mapped_column(String(100), comment="First name")
    lastname: Mapped[str] = mapped_column(String(100), comment="Last name")
    email: Mapped[str] = mapped_column(String(255), index=True, unique=True, comment="Login email")
    password: Mapped[str] = mapped_column(String(255), comment="Argon2-hashed password")
    id_role: Mapped[int] = mapped_column(ForeignKey("role.id"), comment="FK to assigned role")

    role: Mapped[Role] = relationship(lazy="raise")
