<p align="center">
    <a href="https://github.com/diplomatgmg/scheduler/actions/workflows/ci-cd.yml"><img src="https://img.shields.io/github/actions/workflow/status/diplomatgmg/scheduler/ci-cd.yml?label=CI/CD%20Pipeline" alt="CI/CD Pipeline"></a>
    <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Code style"></a>
    <a href="https://github.com/astral-sh/uv"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="Package manager"></a>
    <a href="https://www.python.org/downloads"><img src="https://img.shields.io/badge/python-3.12%2B-blue?label=Python" alt="Python"></a>
<p>


# [Scheduler Bot](https://github.com/diplomatgmg/scheduler)

Телеграм-бот для управления постами в каналах.  
Планируй, редактируй, откладывай сообщения с инлайн-кнопками.  
Чистый, структурированный код согласно best-practices.
Работает на моём домашнем сервере.  

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
