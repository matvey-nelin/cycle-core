from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from infrastructure.config import settings
from infrastructure.models import Base  # noqa: F401

if settings.DATABASE_URL is not None:
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
