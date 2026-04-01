from typing import ClassVar

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Permission(Base):
    __tablename__: str = "permission"
    __table_args__: ClassVar = {"comment": "Available permissions in the platform"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, comment="Permission identifier (e.g. create_project)")
