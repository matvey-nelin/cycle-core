from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.workout.workout import Workout
from domain.workout.workout_repository import AbstractWorkoutRepository
from infrastructure.mappers.workout_mapper import WorkoutMapper, WorkoutSetMapper
from infrastructure.models.exercise import ExerciseORM
from infrastructure.models.workout import WorkoutORM
from infrastructure.repositories.exceptions import IncorrectExerciseIdError, IncorrectWorkoutIdError


class SQLAlchemyWorkoutRepository(AbstractWorkoutRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: UUID) -> Workout | None:
        workout_orm = await self._fetch_orm(id)
        if workout_orm is None:
            return None
        return WorkoutMapper.to_domain(workout_orm)

    async def create(self, workout: Workout) -> None:
        workout_orm = WorkoutMapper.to_orm(workout)
        self.session.add(workout_orm)

    async def update(self, workout: Workout) -> Workout:
        workout_orm = await self._fetch_orm(workout.id)
        if workout_orm is None:
            raise IncorrectWorkoutIdError("Workout must be added in repository before saving changes")

        workout_orm.planned_start_time = workout.planned_start_time
        workout_orm.planned_end_time = workout.planned_end_time
        workout_orm.actual_start_time = workout.actual_start_time
        workout_orm.actual_end_time = workout.actual_end_time

        orm_sets = {wset.id: wset for wset in workout_orm.sets}
        domain_sets = {wset.id: wset for wset in workout.sets}

        await self._ensure_exercises_exist({dset.exercise_id for dset in domain_sets.values()})

        for dset in list(domain_sets.values()):
            if dset.id in orm_sets:
                oset = orm_sets[dset.id]
                oset.exercise_id = dset.exercise_id
                oset.order = dset.order
                oset.planned_reps = dset.planned_reps
                oset.planned_weight = dset.planned_weight
                oset.actual_reps = dset.actual_reps
                oset.actual_weight = dset.actual_weight
            else:
                workout_orm.sets.append(WorkoutSetMapper.to_orm(dset))

        for oset in list(orm_sets.values()):
            if oset.id not in domain_sets:
                workout_orm.sets.remove(oset)

        return WorkoutMapper.to_domain(workout_orm)

    async def _fetch_orm(self, workout_id: UUID) -> WorkoutORM | None:
        query = select(WorkoutORM).where(WorkoutORM.id == workout_id).options(selectinload(WorkoutORM.sets))
        return (await self.session.scalars(query)).one_or_none()

    async def _ensure_exercises_exist(self, exercise_ids: set[UUID]) -> None:
        if not exercise_ids:
            return

        query = select(ExerciseORM.id).where(ExerciseORM.id.in_(exercise_ids))
        rows = (await self.session.execute(query)).scalars().all()
        missing = exercise_ids - set(rows)

        if missing:
            raise IncorrectExerciseIdError("Workout set must have the existent 'exercise_id' value")
