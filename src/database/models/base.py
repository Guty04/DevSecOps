from datetime import datetime

from sqlalchemy import TIMESTAMP, MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

convention: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        comment="Timestamp when the record was created",
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="Timestamp when the record was last updated",
    )
    is_active: Mapped[bool] = mapped_column(
        server_default="true",
        default=True,
        comment="Soft-delete flag",
    )
