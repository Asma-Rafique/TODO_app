from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
DATABASE_URL = 'postgresql+asyncpg://postgres:asmarafique@localhost:5432/todo_database'
Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
