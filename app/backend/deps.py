from config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from utils.auth import Auth0Client

# Initialize HTTPBearer for extracting the token from the Authorization header
security = HTTPBearer()

# Create an instance of Auth0Client for token validation
# This instance will be reused across requests
_auth0_client_instance = Auth0Client(
    domain=settings.AUTH0_DOMAIN,
    api_audience=settings.AUTH0_API_AUDIENCE,
    issuer=settings.AUTH0_ISSUER,
    algorithms=settings.AUTH0_ALGORITHMS,
)


def get_auth0_client() -> Auth0Client:
    """
    Dependency that provides the Auth0Client instance.
    """
    return _auth0_client_instance


async def verify_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth0_svc: Auth0Client = Depends(get_auth0_client),
    # required_scopes: list | None = None,
) -> dict:
    """
    FastAPI dependency to verify the access token from the request header.
    Raises HTTPException on failure. Returns the decoded token payload on success.
    """
    token = credentials.credentials  # Extract the token string
    try:
        # Use the Auth0Client instance to validate the token
        payload = auth0_svc.validate_token(token)  # type: ignore
        return payload
    except HTTPException as e:
        # Re-raise HTTPExceptions from validate_token (e.g., 401, 403)
        raise e
    except Exception as e:
        # Catch any other unexpected errors during the dependency execution
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {e}",
        )
