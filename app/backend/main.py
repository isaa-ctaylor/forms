# main.py
from database import database
from fastapi import FastAPI
from routers import users
from sqlalchemy.orm import Session

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
