from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AUTH0_DOMAIN: str
    AUTH0_CLIENT_ID: str
    AUTH0_CLIENT_SECRET: str
    AUTH0_API_AUDIENCE: str
    AUTH0_CALLBACK_URL: str  # This frontend app's callback URL
    FRONTEND_PORT: int = 8000  # Default port for frontend during development
    BACKEND_API_URL: str  # The URL of your separate backend API

    class Config:
        env_file = "frontend/.env"  # Path to the .env file for the frontend app
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore
