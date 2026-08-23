from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.exercise.exercise import Exercise
from domain.exercise.exercise_repository import AbstractExerciseRepository
from infrastructure.mappers.exercise_mapper import ExerciseMapper
from infrastructure.models.agonist import AgonistORM
from infrastructure.models.exercise import ExerciseORM
from infrastructure.repositories.exceptions import IncorrectAgonistIdError, IncorrectExerciseIdError


class SQLAlchemyExerciseRepository(AbstractExerciseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: UUID) -> Exercise | None:
        exercise_orm = await self._fetch_orm(id)
        if exercise_orm is None:
            return None
        return ExerciseMapper.to_domain(exercise_orm)

    async def create(self, exercise: Exercise) -> None:
        agonists = await self._resolve_agonists(exercise.agonist_ids)
        exercise_orm = ExerciseMapper.to_orm(exercise, agonists)
        self.session.add(exercise_orm)

    async def update(self, exercise: Exercise) -> Exercise:
        exercise_orm = await self._fetch_orm(exercise.id)
        if exercise_orm is None:
            raise IncorrectExerciseIdError("Exercise must be added in repository before saving changes")

        exercise_orm.name = exercise.name
        exercise_orm.agonists = await self._resolve_agonists(exercise.agonist_ids)

        return ExerciseMapper.to_domain(exercise_orm)

    async def _fetch_orm(self, exercise_id: UUID) -> ExerciseORM | None:
        query = select(ExerciseORM).where(ExerciseORM.id == exercise_id).options(selectinload(ExerciseORM.agonists))
        return (await self.session.scalars(query)).one_or_none()

    async def _resolve_agonists(self, agonist_ids: list[UUID]) -> list[AgonistORM]:
        if not agonist_ids:
            return []

        query = select(AgonistORM).where(AgonistORM.id.in_(agonist_ids))
        agonists = (await self.session.execute(query)).scalars().all()

        missing = set(agonist_ids) - {a.id for a in agonists}
        if missing:
            raise IncorrectAgonistIdError("Exercise has agonists which non added in database")

        return [*agonists]
