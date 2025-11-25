# Dockerfile
# Use a minimal Python image as the base
FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

LABEL authors="aszarata"

# Set the working directory in the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    curl libsnappy-dev make gcc g++ libc6-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy only dependency files first (to leverage caching)
COPY ../pyproject.toml ../uv.lock ./

# Install project dependencies using uv
RUN uv sync

# Copy the rest of the application code
COPY .. . 

# Expose the application port
EXPOSE 8000

# Run the application with uv
CMD ["uv", "run", "uvicorn", "onnx_app.app:app", "--host", "0.0.0.0", "--port", "8000"]