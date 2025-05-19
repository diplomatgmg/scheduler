FROM python:3.13-alpine AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONPATH=/app/src \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN apk add --no-cache uv

COPY pyproject.toml uv.lock ./


# ============================ #
#         DEPS INSTALLING      #
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

CMD ["python", "-m", "api.main"]


# ================================= #
#           PRODUCTION              #
# ================================= #
FROM deps-prod AS production

COPY . .

CMD ["python", "-m", "api.main"]
