from fastapi import FastAPI, Depends, status, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import timedelta, datetime
from config.db import get_db, engine
from models.todo import TodoItem, User
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.todo import TodoCreate, TodoItem as TodoItemSchema, Token, UserModel
from config.encryption import get_password_hash
from config.authentication import authenticate_user, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES
user = APIRouter()
# TodoItem.Base.metadata.create_all(bind=engine)


@user.post('/register')
async def create_user(user_detail: UserModel, db: AsyncSession = Depends(get_db)):
    '''
    input user details
    return successful if user not already exist
    '''
    existing_user = await db.execute(select(User).filter(
        User.username == user_detail.username))
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    userd = User(username=user_detail.username,
                 hashed_password=get_password_hash(user_detail.password))
    db.add(userd)
    await db.commit()
    await db.refresh(userd)
    return {"msg": " User created successfully"}


@user.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user.post("/todos/", response_model=TodoItemSchema)
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if todo.date and todo.date.tzinfo is not None:
        todo.date = todo.date.replace(tzinfo=None)  # Make datetime naive
    add_todo = TodoItem(**todo.dict())
    db.add(add_todo)
    await db.commit()
    await db.refresh(add_todo)
    return add_todo


@user.get("/get_all_todos/", response_model=list[TodoItemSchema])
async def read_todos(skip: int = 0, limit: int = 5, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(TodoItem).offset(skip).limit(limit))
    todos = result.scalars().all()
    return todos


@user.get("/get_todo/{todo_title}", response_model=list[TodoItemSchema])
async def read_todo_title(todo_title: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(TodoItem).filter(TodoItem.title == todo_title))
    todos = result.scalars().all()
    if todos is None:
        raise HTTPException(status_code=404, detail="todo title not found")
    return todos


@user.put("/update_todos/{todo_title}", response_model=TodoItemSchema)
async def update_todo(todo_title: str, todo: TodoCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(TodoItem).filter(TodoItem.title == todo_title))
    todos = result.scalars().first()
    if todos is None:
        raise HTTPException(status_code=404, detail="todo title not found")
    for key, value in todo.dict(exclude_unset=True).items():
        if isinstance(value, datetime) and value.tzinfo is not None:
            value = value.replace(tzinfo=None)  # Make datetime naive
        setattr(todos, key, value)
    await db.commit()
    await db.refresh(todos)
    return todos


@user.delete("/delete_todo/{todo_title}", response_model=TodoItemSchema)
async def delete_todo(todo_title: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(TodoItem).filter(TodoItem.title == todo_title))
    todos = result.scalars().first()
    if todos is None:
        raise HTTPException(status_code=404, detail="todo title not found")
    await db.delete(todos)
    await db.commit()
    return todos
