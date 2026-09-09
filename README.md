# Cycle Core

Бэкенд-сервис для учета тренировок. Построен по принципам гексагональной архитектуры: доменная логика изолирована от веб-фреймворка и базы данных.

[![Tests](https://github.com/matvey-nelin/cycle-core/actions/workflows/tests.yml/badge.svg)](https://github.com/matvey-nelin/cycle-core/actions/workflows/tests.yml)
[![Coverage](docs/coverage.svg)](docs/coverage.svg)
[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)

## О проекте

Основная цель архитектуры — независимость бизнес-правил от деталей реализации. 
- **Домен (domain):** Чистый Python. Здесь живут сущности, агрегаты и инварианты. Никаких импортов из FastAPI или SQLAlchemy.
- **Инфраструктура (infrastructure):** Реализация портов. Репозитории на SQLAlchemy, Unit of Work, модели таблиц БД.
- **Сервисы (services):** Слой приложения. Оркестрация бизнес-процессов и координация работы репозиториев через Unit of Work.
- **API (api):** Адаптер для HTTP. Роутеры FastAPI, DTO на Pydantic, внедрение зависимостей.

## Стек технологий

- **Язык:** Python 3.13
- **Фреймворк:** FastAPI + Uvicorn
- **База данных:** PostgreSQL 16
- **ORM:** SQLAlchemy 2.0 (async) + asyncpg
- **Миграции:** Alembic
- **Валидация:** Pydantic v2
- **Тесты:** pytest + pytest-asyncio (с параметризацией REAL/FAKE)
- **Инструменты:** Docker, Docker Compose, GitHub Actions

## Ключевые решения

1. **Unit of Work:** Гарантирует атомарность транзакций при работе с несколькими репозиториями. Если одна из операций падает, откатывается вся транзакция.
2. **Repository Pattern:** Позволяет заменить ORM или СУБД без изменения кода домена и сервисов.
3. **Подход к тестам:** Используется параметризация `REAL`/`FAKE`. Интеграционные тесты поднимают реальную БД через фикстуры, а юнит-тесты работают с моками. Это ускоряет прогон и сохраняет надежность проверок.

## Быстрый старт

Для локального запуска удобнее всего использовать Docker Compose. Он поднимет базу данных, применит миграции и запустит API.

```bash
git clone https://github.com/matvey-nelin/cycle-core.git
cd cycle-core
docker compose up --build
```

После запуска API будет доступно по адресу: http://localhost:8000  
Интерактивная документация (Swagger): http://localhost:8000/docs

## Тестирование

В проекте используется параметризация тестов (`REAL` / `FAKE`).

```bash
# Запустить все тесты (и REAL, и FAKE)
pytest -v

# Только интеграционные тесты (требует запущенную БД или docker compose)
pytest -v -k REAL

# Только юнит-тесты (быстрые, работают с моками, БД не требуется)
pytest -v -k FAKE

# Проверка покрытия кода
pytest --cov=api --cov=domain --cov=services --cov=infrastructure
```

## CI/CD
В репозитории настроен GitHub Actions (.github/workflows/push_pr_test.yml). При каждом пуше в main или создании Pull Request пайплайн:
1. Поднимает PostgreSQL 16 в сервис-контейнере.
2. Устанавливает зависимости и применяет миграции Alembic.
3. **Pull Request (`tests.yml`)**: запуск тестов с PostgreSQL 16 и сохранение отчета о покрытии.
4. **Merge в `main` (`badge.yml`)**: обновление бейджа покрытия `docs/coverage.svg` без повторного прогона тестов.
Ветка main защищена (Branch Protection): мерж невозможен, если CI-пайплайн завершился с ошибкой.