from deps import verify_access_token  # Import the dependency
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(
    prefix="/api",  # All routes in this router will start with /api
    tags=["API Protected"],  # Tags for OpenAPI documentation
)


@router.get("/protected")
async def protected_route(current_user: dict = Depends(verify_access_token)):
    """
    An example endpoint that requires a valid access token.
    """
    return {
        "message": f"Hello, {current_user.get('nickname', current_user.get('sub'))}! This is a protected API endpoint."
    }
