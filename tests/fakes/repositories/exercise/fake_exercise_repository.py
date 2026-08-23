from uuid import UUID

from domain.agonist.agonist import Agonist
from domain.exercise.exercise import Exercise
from domain.exercise.exercise_repository import AbstractExerciseRepository
from infrastructure.repositories.exceptions import IncorrectAgonistIdError, IncorrectExerciseIdError


class FakeExerciseRepository(AbstractExerciseRepository):
    def __init__(
        self,
        exercises: dict[UUID, Exercise] | None = None,
        agonists: dict[UUID, Agonist] | None = None,
    ) -> None:
        self._agonists = agonists if agonists is not None else {}
        self._exercises = exercises if exercises is not None else {}

        self._buffer = {}

    async def get_by_id(self, id: UUID) -> Exercise | None:
        exercise = self._buffer.get(id)
        if exercise is None:
            exercise = self._exercises.get(id)
        if exercise is None:
            return None
        ordered = sorted(exercise.agonist_ids, key=lambda aid: self._agonists[aid].name)
        return Exercise.reconstruct(exercise.id, exercise.name, ordered)

    async def create(self, exercise: Exercise) -> None:
        self._buffer[exercise.id] = exercise

    async def update(self, exercise: Exercise) -> Exercise:
        if self._buffer.get(exercise.id) or self._exercises.get(exercise.id):
            for agonist_id in exercise.agonist_ids:
                if agonist_id not in self._agonists:
                    raise IncorrectAgonistIdError("Agonist must be added in repository before saving changes")

            self._buffer[exercise.id] = exercise
            return exercise
        else:
            raise IncorrectExerciseIdError("Exercise must be added in repository before saving changes")

    def _save_current_transaction(self):
        self._exercises.update(self._buffer)
        self._buffer.clear()

    def _clear_buffer(self):
        self._buffer.clear()
