from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost/dbname"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    poolclass=NullPool
    )


new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session()
    async with new_session() as session:
        try:
            yield session
            await sessoin.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()