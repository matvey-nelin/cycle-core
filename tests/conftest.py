import os
from contextlib import asynccontextmanager

import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from infrastructure.models import Base
from infrastructure.repositories.agonist.sqlalchemy_agonist_repository import SQLAlchemyAgonistRepository
from infrastructure.repositories.exercise.sqlalchemy_exercise_repository import SQLAlchemyExerciseRepository
from infrastructure.repositories.workout.sqlalchemy_workout_repository import SQLAlchemyWorkoutRepository
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
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


@pytest_asyncio.fixture
async def sqlalchemy_workout_repository(session_factory):
    async with session_factory() as session:
        yield SQLAlchemyWorkoutRepository(session)


@pytest_asyncio.fixture
async def sqlalchemy_agonist_repository(session_factory):
    async with session_factory() as session:
        yield SQLAlchemyAgonistRepository(session)


@pytest_asyncio.fixture
async def sqlalchemy_exercise_repository(session_factory):
    async with session_factory() as session:
        yield SQLAlchemyExerciseRepository(session)


@pytest_asyncio.fixture(params=["real", "fake"], ids=["REAL", "FAKE"])
async def double_uow(request):
    if request.param == "real":
        async with test_db() as factory:
            yield SQLAlchemyUnitOfWork(session_factory=factory)
    else:
        yield FakeUnitOfWork()
