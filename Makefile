up:
	docker-compose up --build -d

env:
	uv sync --frozen --group bot --group dev
