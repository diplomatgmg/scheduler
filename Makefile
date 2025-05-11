.PHONY: help

help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

venv: ## Создает виртуальное окружение
	@uv sync \
	--no-install-project \
	--dev \
	--group bot \
	--group bot-dev \
	--group api \
	--group api-dev
.PHONY: venv

up: ## compose up
	docker compose up --build -d
.PHONY: up

down: ## compose down
	docker compose down
.PHONY: down

stop: ## compose stop
	docker compose stop
.PHONY: stop

lint: ## Запуск линтеров
	@uv run ruff check . && \
	uv run isort . && \
	uv run ruff format . && \
	uv run mypy .
.PHONY: lint

mm: ## Создает миграцию с переданным описанием
	@docker compose exec bot alembic revision --autogenerate -m "$(args)"
.PHONY: mm

migrate: ## Применяет миграции
	@docker compose exec bot alembic upgrade head
.PHONY: migrate
