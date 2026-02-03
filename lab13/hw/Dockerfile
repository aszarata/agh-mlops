FROM python:3.12-slim-bookworm

LABEL authors="aszarata"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl libsnappy-dev make gcc g++ libc6-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY ./pyproject.toml ./uv.lock ./

RUN uv sync

RUN uv run guardrails configure --token $GUARDRAILS_API_KEY --disable-metrics --disable-remote-inferencing
RUN uv run guardrails hub install hub://tryolabs/restricttotopi

COPY .. . 

CMD ["uv", "run", "main.py"]