FROM python:3.13.2-alpine

WORKDIR /project/scheduler

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apk update &&  \
    apk upgrade

COPY ./requirements.txt ./requirements.txt
RUN --mount=type=cache,target=/root/.cache/uv uv pip install --system -r requirements.txt

COPY . .

CMD ["uv", "run", "src/main.py"]
