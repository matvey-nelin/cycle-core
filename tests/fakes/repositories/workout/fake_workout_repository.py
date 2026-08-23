from uuid import UUID

from domain.exercise.exercise import Exercise
from domain.workout.workout import Workout
from domain.workout.workout_repository import AbstractWorkoutRepository
from infrastructure.repositories.exceptions import IncorrectExerciseIdError, IncorrectWorkoutIdError


class FakeWorkoutRepository(AbstractWorkoutRepository):
    def __init__(
        self, workouts: dict[UUID, Workout] | None = None, exercises: dict[UUID, Exercise] | None = None
    ) -> None:
        self._exercises = exercises if exercises is not None else {}
        self._workouts = workouts if workouts is not None else {}
        self._buffer = {}

    async def get_by_id(self, id: UUID) -> Workout | None:
        workout = self._buffer.get(id)
        if workout is None:
            workout = self._workouts.get(id)
        return workout

    async def create(self, workout: Workout) -> None:
        self._buffer[workout.id] = workout

    async def update(self, workout: Workout) -> Workout:
        if self._buffer.get(workout.id) or self._workouts.get(workout.id):
            for wset in workout.sets:
                if wset.exercise_id not in self._exercises:
                    raise IncorrectExerciseIdError("Workout set must have the existent 'exercise_id' value")

            self._buffer[workout.id] = workout
            return workout
        else:
            raise IncorrectWorkoutIdError("Workout must be added in repository before saving changes")

    def _save_current_transaction(self):
        self._workouts.update(self._buffer)
        self._buffer.clear()

    def _clear_buffer(self):
        self._buffer.clear()
