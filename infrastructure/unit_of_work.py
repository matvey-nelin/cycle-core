from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from domain.exceptions import DataIntegrityError
from infrastructure.repositories.agonist.sqlalchemy_agonist_repository import (
    SQLAlchemyAgonistRepository,
)
from infrastructure.repositories.workout.sqlalchemy_workout_repository import (
    SQLAlchemyWorkoutRepository,
)
from services.abstract_unit_of_work import AbstractUnitOfWork


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        self.session = self.session_factory()
        self.workouts = SQLAlchemyWorkoutRepository(self.session)
        self.agonists = SQLAlchemyAgonistRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def commit(self) -> None:
        try:
            await self.session.commit()
        except IntegrityError:
            raise DataIntegrityError()

    async def rollback(self) -> None:
        await self.session.rollback()
