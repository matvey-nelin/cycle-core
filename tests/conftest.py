import os
from contextlib import asynccontextmanager

import pytest_asyncio
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.dependencies import get_agonist_service, get_exercise_service, get_workout_service
from infrastructure.models import Base
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from main import app
from services.agonist_service import AgonistService
from services.exercise_service import ExerciseService
from services.workout_service import WorkoutService
from tests.fakes.fake_unit_of_work import FakeUnitOfWork

load_dotenv()
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


@asynccontextmanager
async def test_db():
    """Create a new session factory with test database"""
    if TEST_DATABASE_URL is None:
        raise ValueError("TEST_DATABASE_URL not set in environment")

    engine = create_async_engine(TEST_DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(engine, expire_on_commit=False)

    yield factory

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def session_factory():
    async with test_db() as factory:
        yield factory


@pytest_asyncio.fixture(params=["real", "fake"], ids=["REAL", "FAKE"])
async def double_uow(request):
    if request.param == "real":
        async with test_db() as factory:
            yield SQLAlchemyUnitOfWork(session_factory=factory)
    else:
        yield FakeUnitOfWork()


@pytest_asyncio.fixture(params=["REAL", "FAKE"])
async def client(request, session_factory):
    if request.param == "REAL":
        app.dependency_overrides[get_workout_service] = lambda: WorkoutService(SQLAlchemyUnitOfWork(session_factory))
        app.dependency_overrides[get_exercise_service] = lambda: ExerciseService(SQLAlchemyUnitOfWork(session_factory))
        app.dependency_overrides[get_agonist_service] = lambda: AgonistService(SQLAlchemyUnitOfWork(session_factory))
    else:
        fake_uow = FakeUnitOfWork()
        app.dependency_overrides[get_workout_service] = lambda: WorkoutService(fake_uow)
        app.dependency_overrides[get_exercise_service] = lambda: ExerciseService(fake_uow)
        app.dependency_overrides[get_agonist_service] = lambda: AgonistService(fake_uow)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
