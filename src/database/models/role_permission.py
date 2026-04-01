from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class RolePermission(Base):
    __tablename__: str = "role_x_permission"
    __table_args__ = (
        UniqueConstraint("id_role", "id_permission"),
        {"comment": "Many-to-many join between roles and permissions"},
    )

    id_role: Mapped[int] = mapped_column(ForeignKey("role.id"), primary_key=True, comment="FK to role")
    id_permission: Mapped[int] = mapped_column(
        ForeignKey("permission.id"), primary_key=True, comment="FK to permission"
    )
