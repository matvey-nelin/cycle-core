import datetime
from uuid import UUID

from domain.workout.workout import Workout
from infrastructure.repositories.exceptions import IncorrectExerciseIdError
from services.abstract_unit_of_work import AbstractUnitOfWork
from services.exceptions import ExerciseNotFoundError, WorkoutNotFoundError


class WorkoutService:
    def __init__(self, unit_of_work: AbstractUnitOfWork) -> None:
        self.uow = unit_of_work

    async def get_workout(self, workout_id: UUID) -> Workout:
        async with self.uow:
            return await self._get_workout_or_raise(workout_id)

    async def create_workout(
        self,
        start_time: datetime.datetime | None = None,
        end_time: datetime.datetime | None = None,
    ) -> UUID:
        async with self.uow:
            workout = Workout(
                planned_start_time=start_time,
                planned_end_time=end_time,
                actual_start_time=start_time,
                actual_end_time=end_time,
            )
            await self.uow.workouts.create(workout)
            await self.uow.commit()
        return workout.id

    async def add_workout_set(
        self,
        workout_id: UUID,
        exercise_id: UUID,
        reps: int = 0,
        weight: float = 0,
    ) -> UUID:
        async with self.uow:
            workout = await self._get_workout_or_raise(workout_id)
            workout.add_set(
                exercise_id=exercise_id,
                planned_reps=reps,
                planned_weight=weight,
                actual_reps=reps,
                actual_weight=weight,
            )
            try:
                await self.uow.workouts.update(workout)
                await self.uow.commit()
            except IncorrectExerciseIdError as _ex:
                raise ExerciseNotFoundError(_ex.message)
        return workout.sets[-1].id

    async def remove_workout_set(self, workout_id: UUID, workout_set_id: UUID) -> None:
        async with self.uow:
            workout = await self._get_workout_or_raise(workout_id)
            workout.remove_set(workout_set_id)
            await self.uow.workouts.update(workout)
            await self.uow.commit()

    async def _get_workout_or_raise(self, workout_id: UUID) -> Workout:
        """Method-helper without context"""
        workout = await self.uow.workouts.get_by_id(workout_id)
        if workout is None:
            raise WorkoutNotFoundError()
        return workout
