from uuid import UUID

from domain.agonist.agonist import Agonist
from domain.exercise.exercise import Exercise
from domain.workout.workout import Workout
from services.abstract_unit_of_work import AbstractUnitOfWork
from tests.fakes.repositories.agonist.fake_agonist_repository import FakeAgonistRepository
from tests.fakes.repositories.exercise.fake_exercise_repository import FakeExerciseRepository
from tests.fakes.repositories.workout.fake_workout_repository import FakeWorkoutRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self) -> None:
        self._agonists: dict[UUID, Agonist] = {}
        self._exercises: dict[UUID, Exercise] = {}
        self._workouts: dict[UUID, Workout] = {}
        self.agonists: FakeAgonistRepository = FakeAgonistRepository(self._agonists)
        self.exercises: FakeExerciseRepository = FakeExerciseRepository(self._exercises, self._agonists)
        self.workouts: FakeWorkoutRepository = FakeWorkoutRepository(self._workouts, self._exercises)

    async def __aenter__(self) -> AbstractUnitOfWork:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self.agonists._clear_buffer()
        self.exercises._clear_buffer()
        self.workouts._clear_buffer()

    async def commit(self) -> None:
        self.agonists._save_current_transaction()
        self.exercises._save_current_transaction()
        self.workouts._save_current_transaction()

    async def rollback(self) -> None:
        self.agonists._clear_buffer()
        self.exercises._clear_buffer()
        self.workouts._clear_buffer()
