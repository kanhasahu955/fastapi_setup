from sqlalchemy.ext.asyncio import (create_async_engine, AsyncSession,async_sessionmaker)
from sqlmodel import SQLModel

from app.core.env import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url, 
    echo = settings.debug,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
    )

AsyncSessionLocal = async_sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit=False
)

async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

async def close_db():
    await engine.dispose()

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session