from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[bool] = False
    date: Optional[datetime] = None


class TodoCreate(TodoBase):
    pass


class UserModel(BaseModel):
    username: str
    password: str


class TodoItem(TodoBase):
    id: int

    class Config:
        orm_mode = True
