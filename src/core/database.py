from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from src.core.config import settings


# -------------------------
# ENGINE
# -------------------------
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True
)


# -------------------------
# SESSION FACTORY
# -------------------------
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# -------------------------
# DEPENDENCY
# -------------------------
async def get_db() -> AsyncSession:

    async with AsyncSessionLocal() as session:
        
        yield session
        