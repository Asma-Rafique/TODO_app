from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from config.db import Base, engine
from datetime import datetime


class TodoItem(Base):
    __tablename__ = 'todo_items'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(Boolean, default=False)
    date = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)
