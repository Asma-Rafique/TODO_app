from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[bool] = False
    date: Optional[datetime] = None


class TodoCreate(TodoBase):
    pass


class TodoItem(TodoBase):
    id: int

    class Config:
        orm_mode = True
