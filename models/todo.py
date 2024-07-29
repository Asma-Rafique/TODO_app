from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from config.db import Base, engine
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class TodoItem(Base):
    __tablename__ = 'todo_items'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(Boolean, default=False)
    # date = Column(DateTime, default=datetime.utcnow)this was created dbapi error
    date = Column(DateTime(timezone=False), default=datetime.utcnow)

# async def init_db():
#     async with engine.begin() as conn:
#         # Drop all tables (optional, for a clean start)
#         # await conn.run_sync(Base.metadata.drop_all)
#         # Create all tables
#         await conn.run_sync(Base.metadata.create_all)
