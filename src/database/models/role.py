from typing import ClassVar

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .permission import Permission


class Role(Base):
    __tablename__: str = "role"
    __table_args__: ClassVar = {"comment": "Platform roles (Admin, PM)"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, comment="Role display name")

    permissions: Mapped[set[Permission]] = relationship(secondary="role_x_permission", lazy="raise")
