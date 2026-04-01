import ssl
from collections.abc import AsyncGenerator
from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.configurations import configuration
from src.enums import Environment

_ssl_context = ssl.create_default_context()
_ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2


@dataclass
class Database:
    engine: AsyncEngine = field(
        default_factory=lambda: create_async_engine(
            url=configuration.DATABASE_URL.encoded_string(),
            echo=configuration.ENVIRONMENT == Environment.DEVELOPMENT,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600,
            pool_pre_ping=True,
            pool_timeout=30,
            connect_args={"ssl": _ssl_context},
        )
    )
    session_maker: async_sessionmaker[AsyncSession] = field(init=False)

    def __post_init__(self) -> None:
        self.session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def get_async_session(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_maker() as session:
            try:
                yield session
                await session.commit()

            except Exception:
                await session.rollback()
                raise


database: Database = Database()
