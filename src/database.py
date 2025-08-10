from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.models.models import Base
from sqlalchemy.pool import NullPool

# Используем SQLite с асинхронным драйвером
DATABASE_URL = "sqlite+aiosqlite:///./advertisement.db"

# Настройки движка для SQLite
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Логирование SQL-запросов
    poolclass=NullPool,
    connect_args={"check_same_thread": False}  # Важно для SQLite!
)

# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)

async def get_db() -> AsyncSession:
    """Генератор сессий для Dependency Injection"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()