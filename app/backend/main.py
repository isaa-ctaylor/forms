from config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.v1 import protected

app = FastAPI()

# --- CORS Configuration ---
# IMPORTANT: Adjust origins for your production environment.
# Make sure to include the exact URL of your frontend application.
origins = [
    "http://localhost:8000",  # If frontend is also a FastAPI app on 8000
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers, including Authorization
)

# --- Include API Routers ---
app.include_router(protected.router)


# --- Health Check Route ---
@app.get("/health", summary="Health Check")
async def health_check():
    """
    A simple health check endpoint to confirm the API is running.
    """
    return {"status": "ok", "service": "backend"}
