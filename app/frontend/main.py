import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.v1 import pages

app = FastAPI()

# --- Serve Static Files ---
# Get static files directory relative to the current file
static_dir = os.path.join(os.path.dirname(__file__), "static")
# Mount the 'static' directory to serve CSS, JS, HTML files (like index.html, dashboard.html)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# --- Include API Routers ---
app.include_router(pages.router)


# --- Health Check Route ---
@app.get("/health", summary="Health Check")
async def health_check():
    """
    A simple health check endpoint to confirm the API is running.
    """
    return {"status": "ok", "service": "backend"}
