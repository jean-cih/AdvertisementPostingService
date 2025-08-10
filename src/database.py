from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.models.models import Base
from sqlalchemy.pool import NullPool


DATABASE_URL = "sqlite+aiosqlite:///./advertisement.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True, 
    poolclass=NullPool,
    connect_args={"check_same_thread": False}
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()