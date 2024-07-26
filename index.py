from fastapi import FastAPI
from routes.todo import user

app = FastAPI()
app.include_router(user)
