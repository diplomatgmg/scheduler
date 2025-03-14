FROM python:3.13.2-alpine AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /project/src

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apk update &&  \
    apk upgrade

COPY requirements/production.txt ./requirements/


# ================================= #
#           DEVELOPMENT             #
# ================================= #
FROM base AS development

COPY requirements/development.txt ./requirements/
RUN --mount=type=cache,target=/root/.cache/uv uv pip install --system -r requirements/development.txt

COPY . .

CMD ["hupper", "-q", "-m", "main", "--watch", "./src"]


# ================================= #
#           PRODUCTION              #
# ================================= #
FROM base AS production

RUN --mount=type=cache,target=/root/.cache/uv uv pip install --system -r requirements/production.txt

COPY . .

CMD ["uv", "run", "main.py"]