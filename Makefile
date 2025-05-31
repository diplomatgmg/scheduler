.PHONY: help

help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

up: ## compose up
	@docker compose $(DOCKER_PROFILES) up --wait -d
.PHONY: up

down: ## compose down
	@docker compose $(DOCKER_PROFILES) down
.PHONY: down

stop: ## compose stop
	@docker compose $(DOCKER_PROFILES) stop
.PHONY: stop

redis-flush: ## Очищает весь кеш Redis
	@docker compose exec redis redis-cli -p $(REDIS_PORT) -h $(REDIS_HOST) FLUSHALL
.PHONY: redis-flush

venv: ## Создает виртуальное окружение
	@uv sync \
	--no-install-project \
	--dev \
	--group bot \
	--group bot-dev \
	--group api \
	--group api-dev \
	--group tests
.PHONY: venv

lint: ## Запуск линтеров без правок
	@uv run ruff check . && \
	uv run isort . --check-only && \
	uv run ruff format --check . && \
	uv run mypy .
.PHONY: lint

lint-fix: ## Запуск линтеров с правками
	@uv run ruff check . && \
	uv run isort . && \
	uv run ruff format . && \
	uv run mypy .
.PHONY: lint-fix

mm: ## Создание миграции (make mm args="описание")
	@if [ -z "$(args)" ]; then \
        echo "Error: migration message is required"; exit 1; \
    fi
	@docker compose exec bot alembic revision --autogenerate -m "$(args)"
.PHONY: mm

migrate: ## Применяет миграции
	@docker compose exec bot alembic upgrade head
.PHONY: migrate

test: ## Запускает тесты
	docker compose run --quiet --build --rm tester pytest src/tests
.PHONY: test


ENV_FILE = .env
DOCKER_PROFILES :=

# Проверка и загрузка .env файла
ifeq ("$(wildcard $(ENV_FILE))", "$(ENV_FILE)")
  include $(ENV_FILE)
  export
endif

ifeq ($(BOT_USE_WEBHOOK),true)
	DOCKER_PROFILES += --profile api
endif

ifeq ($(CELERY_BEAT_ENABLED),true)
	DOCKER_PROFILES += --profile celery-beat
endif