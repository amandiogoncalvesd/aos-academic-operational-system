"""Engine SQLAlchemy 2.0 async, sessão e Base declarativa."""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=not settings.is_sqlite,
    connect_args={"check_same_thread": False} if settings.is_sqlite else {},
)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    """Cria tabelas (dev/test). Em produção usar Alembic."""
    from . import models  # noqa: F401  (regista os models)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
