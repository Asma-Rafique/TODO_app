from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.db import get_db, engine
from models.todo import TodoItem
from sqlalchemy.future import select
from schemas.todo import TodoCreate, TodoItem as TodoItemSchema
user = APIRouter()
# TodoItem.Base.metadata.create_all(bind=engine)


@user.post("/todos/", response_model=TodoItemSchema)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    add_todo = TodoItem(**todo.dict())
    db.add(add_todo)
    db.commit()
    db.refresh(add_todo)
    return add_todo


@user.get("/get_all_todos/", response_model=list[TodoItemSchema])
async def read_todos(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    result = db.execute(select(TodoItem).offset(skip).limit(limit))
    todos = result.scalars().all()
    return todos


@user.get("/get_todo/{todo_title}", response_model=list[TodoItemSchema])
async def read_todo_title(todo_title: str, db: Session = Depends(get_db)):
    result = db.execute(select(TodoItem).filter(TodoItem.title == todo_title))
    todos = result.scalars().all()
    if todos is None:
        raise HTTPException(status_code=404, detail="todo title not found")
    return todos


@user.put("/update_todos/{todo_title}", response_model=TodoItemSchema)
async def update_todo(todo_title: str, todo: TodoCreate, db: Session = Depends(get_db)):
    result = db.execute(select(TodoItem).filter(TodoItem.title == todo_title))
    todos = result.scalars().first()
    if todos is None:
        raise HTTPException(status_code=404, detail="todo title not found")
    for key, value in todo.dict(exclude_unset=True).items():
        setattr(todos, key, value)
    db.commit()
    db.refresh(todos)
    return todos


@user.delete("/delete_todo/{todo_title}", response_model=TodoItemSchema)
async def delete_todo(todo_title: str, db: Session = Depends(get_db)):
    result = db.execute(select(TodoItem).filter(TodoItem.title == todo_title))
    todos = result.scalars().first()
    if todos is None:
        raise HTTPException(status_code=404, detail="todo title not found")
    db.delete(todos)
    db.commit()
    return todos
