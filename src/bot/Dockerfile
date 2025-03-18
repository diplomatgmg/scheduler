FROM ghcr.io/astral-sh/uv:0.6.7-python3.13-alpine AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONPATH=/app/src \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app


COPY . .


# ================================= #
#           DEVELOPMENT             #
# ================================= #
FROM base AS development


RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --group bot --group dev

CMD ["hupper", "-q", "-m", "bot"]


# ================================= #
#           PRODUCTION              #
# ================================= #
FROM base AS production

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --group bot

CMD ["python", "-m", "bot"]