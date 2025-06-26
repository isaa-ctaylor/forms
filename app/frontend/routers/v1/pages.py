import base64
import hashlib  # Needed for PKCE code challenge generation
import os
import secrets

import httpx
from config import settings  # Import settings
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()

# In-memory storage for state and code_verifier parameters.
# IMPORTANT: In a production environment, this should be a robust,
# persistent session store (e.g., Redis, database-backed sessions)
# to prevent race conditions, ensure scalability, and handle server restarts.
# Each entry will store a dictionary: {"code_verifier": "...", "timestamp": ...}
auth_flow_data = {}  # Renamed from auth_states for clarity with code_verifier


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serves the main index.html page.
    """
    try:
        with open("./static/index.html", "r") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="index.html not found"
        )


@router.get("/login")
async def login_redirect():
    """
    Initiates the Auth0 login process by redirecting to Auth0 Universal Login.
    Includes state parameter for CSRF protection and PKCE challenge.
    """
    # 1. Generate a secure `state` parameter
    state = secrets.token_urlsafe(32)

    # 2. Generate a secure `code_verifier` (between 43 and 128 characters)
    # Using secrets.token_urlsafe ensures cryptographic randomness.
    # An example length range for the verifier would be 43-128 chars.
    # A 64-character verifier will typically produce a 86-character challenge.
    code_verifier = secrets.token_urlsafe(64)

    # 3. Derive the `code_challenge` from the `code_verifier`
    code_challenge = generate_code_challenge(code_verifier)

    # 4. Store `state` and `code_verifier` for later validation in the callback
    # In a real app, you might also add an expiration timestamp for these entries.
    auth_flow_data[state] = {"code_verifier": code_verifier}

    authorize_url = (
        f"https://{settings.AUTH0_DOMAIN}/authorize?"
        f"response_type=code&"
        f"client_id={settings.AUTH0_CLIENT_ID}&"
        f"redirect_uri={settings.AUTH0_CALLBACK_URL}&"
        f"scope=openid%20profile%20email&"
        f"audience={settings.AUTH0_API_AUDIENCE}&"
        f"state={state}&"  # CSRF protection
        f"code_challenge_method=S256&"
        f"code_challenge={code_challenge}"  # PKCE challenge
    )
    print(f"Redirecting to Auth0: {authorize_url}")
    return RedirectResponse(authorize_url)


def generate_code_challenge(code_verifier: str) -> str:
    """
    Generates a PKCE code challenge using the S256 method.
    """
    # SHA256 hash of the code_verifier
    hashed = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    # Base64url encode the hash, removing padding
    return base64.urlsafe_b64encode(hashed).decode("utf-8").rstrip("=")


@router.get("/callback", response_class=HTMLResponse)
async def auth_callback(
    request: Request,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    error_description: str | None = None,
):
    """
    Handles the Auth0 callback, exchanges the authorization code for tokens.
    """
    # 1. Validate `state` parameter and retrieve stored `code_verifier`
    if state not in auth_flow_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid state parameter or state expired.",
        )

    stored_data = auth_flow_data.pop(
        state
    )  # Remove after use to prevent replay attacks
    code_verifier = stored_data.get("code_verifier")

    if not code_verifier:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Code verifier missing for state.",
        )

    if not code:
        if error:
            if error_description:
                detail = f"Authentication failed: {error} - {error_description}"
            else:
                detail = f"Authentication failed: {error}"
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code missing.",
        )

    try:
        # 2. Exchange the authorization code for tokens, including `code_verifier`
        token_url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.AUTH0_CLIENT_ID,
            "client_secret": settings.AUTH0_CLIENT_SECRET,
            "code": code,
            "redirect_uri": settings.AUTH0_CALLBACK_URL,
            "audience": settings.AUTH0_API_AUDIENCE,
            "code_verifier": code_verifier,  # Pass the retrieved code_verifier
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, headers=headers, data=data)
            response.raise_for_status()
            tokens = response.json()

        access_token = tokens["access_token"]
        id_token = tokens["id_token"]

        return RedirectResponse(
            url=f"/static/dashboard.html#access_token={access_token}&id_token={id_token}"
        )

    except httpx.HTTPStatusError as e:
        print(
            f"HTTP error during token exchange: {e.response.status_code} - {e.response.text}"
        )
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Authentication failed: {e.response.text}",
        )
    except Exception as e:
        print(f"Error during token exchange: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed during token exchange.",
        )
