from fastapi import Security
from fastapi.routing import APIRouter
from utils.auth import verify_token

router = APIRouter(
    prefix="/v1/users",
    tags=["users"],
)


@router.get("/me")
async def get_current_user(auth_result: str = Security(verify_token.verify)):
    return auth_result
