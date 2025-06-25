from fastapi import FastAPI

app = FastAPI()


@app.get("/{path_name:path}")
async def hello_world(path_name: str):
    """
    Returns a simple hello world message for any path.
    """
    return {"message": f"Hello, world! You accessed: {path_name}"}
