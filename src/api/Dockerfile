FROM ghcr.io/astral-sh/uv:0.7.3-python3.13-alpine AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONPATH=/app/src \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./


# ============================ #
#        DEPS INSTALLING      #
# ============================ #
FROM base AS deps-dev

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --dev --group api --group api-dev

FROM base AS deps-prod

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --group api


# ================================= #
#           DEVELOPMENT             #
# ================================= #
FROM deps-dev AS development

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# ================================= #
#           PRODUCTION              #
# ================================= #
FROM deps-prod AS production

RUN apk add --no-cache curl

COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
