from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.workout.workout import Workout
from domain.workout.workout_repository import AbstractWorkoutRepository
from infrastructure.mappers.workout_mapper import WorkoutMapper, WorkoutSetMapper
from infrastructure.models.workout import WorkoutORM
from infrastructure.repositories.exceptions import IncorrectWorkoutIdError


class SQLAlchemyWorkoutRepository(AbstractWorkoutRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, workout_id: UUID) -> Workout | None:
        workout_orm = await self._fetch_orm(workout_id)
        if workout_orm is None:
            return None
        return WorkoutMapper.to_domain(workout_orm)

    def create(self, workout: Workout) -> None:
        workout_orm = WorkoutMapper.to_orm(workout)
        self.session.add(workout_orm)

    async def update(self, workout_domain: Workout) -> Workout:
        workout_orm = await self._fetch_orm(workout_domain.id)
        if workout_orm is None:
            raise IncorrectWorkoutIdError("Workout must be added in repository before saving changes")

        workout_orm.planned_start_time = workout_domain.planned_start_time
        workout_orm.planned_end_time = workout_domain.planned_end_time
        workout_orm.actual_start_time = workout_domain.actual_start_time
        workout_orm.actual_end_time = workout_domain.actual_end_time

        orm_sets = {wset.id: wset for wset in workout_orm.sets}
        domain_sets = {wset.id: wset for wset in workout_domain.sets}

        for dset_id, dset in domain_sets.items():
            if dset_id in orm_sets:
                oset = orm_sets[dset_id]
                oset.exercise_id = dset.exercise_id
                oset.order = dset.order
                oset.planned_reps = dset.planned_reps
                oset.planned_weight = dset.planned_weight
                oset.actual_reps = dset.actual_reps
                oset.actual_weight = dset.actual_weight
            else:
                workout_orm.sets.append(WorkoutSetMapper.to_orm(dset))

        for oset_id, oset in orm_sets.items():
            if oset_id not in domain_sets:
                workout_orm.sets.remove(oset)

        return WorkoutMapper.to_domain(workout_orm)

    async def _fetch_orm(self, workout_id: UUID) -> WorkoutORM | None:
        query = select(WorkoutORM).where(WorkoutORM.id == workout_id).options(selectinload(WorkoutORM.sets))
        return (await self.session.scalars(query)).one_or_none()
