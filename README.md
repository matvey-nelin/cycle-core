# Cycle Core

Backend-ядро дневника для планирования и учета тренировок. В приложении предусмотрено многоуровневое планирование (микроциклы, мезоциклы, макроциклы), а также управление агонистами, упражнениями, шаблонами тренировок и микроциклов. 
Доступна расширенная статистика по тренировочному процессу, на основе данных учета тренировок.

[![Tests](https://github.com/matvey-nelin/cycle-core/actions/workflows/tests.yml/badge.svg)](https://github.com/matvey-nelin/cycle-core/actions/workflows/tests.yml)
[![Coverage](docs/coverage.svg)](docs/coverage.svg)
[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)

## О проекте

Данная архитектура выбрана для сохранения возможности перехода на микросервисную архитектуру через минимальные изменения кода, а также для независимости от платформы и варианта использования приложения. Программа сможет развернуться как и в клиент-серверной архитектуре, так и локально. 

- **Домен (domain):** Датаклассы на Python с реализацией бизнес-правил.
- **Инфраструктура (infrastructure):** Слой репозиториев. Используется SQLAlchemy и PostgreSQL.
- **Сервисы (services):** Слой приложения. Для каждого агрегата выделен свой сервисный класс с вариантами использования.
- **API (api):** Слой API. Вывод функционала приложения во внешний мир через FastAPI и валидацией через Pydantic.

## Стек технологий

- **Язык:** Python 3.13
- **Фреймворк:** FastAPI + Uvicorn
- **База данных:** PostgreSQL 16
- **ORM:** SQLAlchemy 2.0 (async) + asyncpg
- **Миграции:** Alembic
- **Валидация:** Pydantic v2
- **Тесты:** pytest + pytest-asyncio (с параметризацией REAL/FAKE)
- **Инструменты:** Docker, Docker Compose, GitHub Actions

## Развертывание

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
В репозитории настроен GitHub Actions (.github/workflows/push_pr_test.yml) для защиты от непроверенного кода. При каждом пуше в main или создании Pull Request пайплайн:
1. Поднимает PostgreSQL 16 в сервис-контейнере.
2. Устанавливает зависимости и применяет миграции Alembic.
3. **Pull Request (`tests.yml`)**: запуск тестов с PostgreSQL 16 и сохранение отчета о покрытии.
4. **Merge в `main` (`badge.yml`)**: обновление бейджа покрытия `docs/coverage.svg` без повторного прогона тестов.
