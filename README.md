[![.github/workflows/ci.yml](https://github.com/diplomatgmg/scheduler/actions/workflows/ci.yml/badge.svg)](https://github.com/diplomatgmg/scheduler/actions/workflows/ci.yml)

# [Scheduler Bot](https://github.com/diplomatgmg/scheduler)

Телеграм-бот для управления постами в каналах.  
Планируй, редактируй, откладывай сообщения с инлайн-кнопками.  
Работает на моём домашнем сервере.  
Код повидал всякое, но этот — чистый и делает дело.

## Что внутри

- **Python 3.12**, **aiogram**
- **SQLAlchemy**, **PostgreSQL**, **PgBouncer**
- **Loguru**, **Sentry**
- **Docker**, **Docker Compose**
- **uvloop**
- **uv**, **mypy**, **ruff**
- **Makefile**

## Структура

Все максимально модульно, интуитивно:
- **bot** — сердце, где живёт логика.
- **core** — настройки, логи, база.
- **db** — модели для PostgreSQL.
- **handlers** — ловят команды и сообщения.
- **keyboards** — кнопки, инлайн и обычные.
- **middlewares** — фильтры, аутентификация, логи.
- **services** — бизнес-логика, работа с юзерами.
- **states** — FSM для сложных диалогов.
- **utils** — всякие полезности.

## CI/CD

Деплой на домашний сервер через self-hosted **GitHub Actions**. Линтинг, билд образа, деплой. Ручками ничего не трогаю.


## Best Practices

- Хорошая архитектура.
- Код по **PEP 8**, проверяется **ruff**. Типизация через **mypy**.
- Документация в коде, но без фанатизма.
