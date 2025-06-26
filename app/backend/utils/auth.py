import jwt
from fastapi import HTTPException, status
from jwt import PyJWKClient


class Auth0Client:
    def __init__(self, domain: str, api_audience: str, issuer: str, algorithms: list):
        self.domain = domain
        self.api_audience = api_audience
        self.issuer = issuer
        self.algorithms = algorithms
        self.jwks_client = PyJWKClient(f"https://{self.domain}/.well-known/jwks.json")

    def validate_token(self, token: str):
        """
        Validates an Auth0 Access Token (JWT).
        """
        try:
            # Get the signing key from Auth0's JWKS endpoint
            signing_key = self.jwks_client.get_signing_key_from_jwt(token).key

            # Decode and validate the JWT
            payload = jwt.decode(
                token,
                signing_key,
                algorithms=self.algorithms,
                audience=self.api_audience,
                issuer=self.issuer,
                options={
                    "verify_signature": True,
                    "require": ["exp", "iat", "aud", "iss"],
                },
            )

            # # Check for required scopes if specified
            # if required_scopes:
            #     token_scopes = payload.get("scope", "").split()
            #     if not all(scope in token_scopes for scope in required_scopes):
            #         raise HTTPException(
            #             status_code=status.HTTP_403_FORBIDDEN,
            #             detail="Insufficient permissions. Required scopes: "
            #             + ", ".join(required_scopes),
            #         )

            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}"
            )
        except Exception as e:
            # Catch any other unexpected errors during validation
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Authentication error during token validation: {e}",
            )
