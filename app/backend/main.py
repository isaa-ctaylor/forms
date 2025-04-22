# main.py
from database import database
from fastapi import FastAPI
from routers import auth, users
from sqlalchemy.orm import Session

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
