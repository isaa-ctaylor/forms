# main.py
from database import database
from fastapi import FastAPI
from routers import auth, users
from sqlalchemy.orm import Session
from utils.admin import create_default_admin

database.Base.metadata.create_all(bind=database.engine)

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_default_admin()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
