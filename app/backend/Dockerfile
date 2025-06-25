# Stage 1: Build Stage - Install Poetry dependencies
# Using Python 3.13.5-slim-bookworm
FROM python:3.13.5-slim-bookworm AS poetry-build

# Set environment variables for Poetry and Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install Poetry itself
# Pin to a specific Poetry version for consistency
RUN pip install poetry==2.1.3

# Set the working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock first to leverage Docker cache
COPY pyproject.toml poetry.lock ./

# Install project dependencies using Poetry
# --no-root to not install the project itself yet
# --compile to compile .pyc files during installation for faster startup
RUN poetry install --no-root --compile


# Stage 2: Production Stage - Minimal runtime image
# Using Python 3.13.5-slim-bookworm again for consistency
FROM python:3.13.5-slim-bookworm AS production-stage

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Create a non-root user and group
RUN groupadd --system appuser && useradd --system --gid appuser appuser

# Create the application directory and set permissions
WORKDIR /app
RUN chown appuser:appuser /app

# Switch to the non-root user
USER appuser

# Copy only the installed Python packages from the poetry-build stage's virtual environment
# The path /app/.venv is created because POETRY_VIRTUALENVS_IN_PROJECT=true
# Ensure the Python version directory is correct (e.g., python3.13)
COPY --from=poetry-build /app/.venv /app/.venv

# Add the virtual environment's bin directory to the PATH for the appuser
ENV PATH="/app/.venv/bin:$PATH"

# Copy your application code
COPY ./ .

# Expose the port Uvicorn will listen on
EXPOSE 8000

# Command to run the FastAPI application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]