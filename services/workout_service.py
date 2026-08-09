import datetime
from uuid import UUID

from domain.workout import Workout
from domain.workout_set import WorkoutSet
from infrastructure.repositories.workout_repositories import AbstractWorkoutRepository
from services.exceptions import WorkoutNotFoundError


class WorkoutService:
    def __init__(self, repository: AbstractWorkoutRepository) -> None:
        self.repository = repository

    def get_workout(self, workout_id: str | UUID) -> Workout:
        workout = self.repository.get_by_id(str(workout_id))
        if not workout:
            raise WorkoutNotFoundError("Passed incorrect id")

        return workout

    def create_workout(
        self,
        start_time: datetime.datetime | None = None,
        end_time: datetime.datetime | None = None,
    ) -> str:
        workout = Workout(
            planned_start_time=start_time,
            planned_end_time=end_time,
            actual_start_time=start_time,
            actual_end_time=end_time,
        )
        self.repository.add(workout)

        return workout.id

    def create_workout_set(
        self,
        workout_id: str | UUID,
        exercise_id: str | UUID,
        reps: int = 0,
        weight: float = 0,
    ) -> None:
        workout_set = WorkoutSet(
            exercise_id=str(exercise_id),
            planned_reps=reps,
            planned_weight=weight,
            actual_reps=reps,
            actual_weight=weight,
        )

        workout = self.repository.get_by_id(str(workout_id))
        if not workout:
            raise WorkoutNotFoundError("Passed incorrect id")

        workout.add_set(workout_set)
        self.repository.add(workout)
