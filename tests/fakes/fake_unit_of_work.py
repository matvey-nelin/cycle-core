from services.abstract_unit_of_work import AbstractUnitOfWork
from tests.fakes.repositories.agonist.fake_agonist_repository import FakeAgonistRepository
from tests.fakes.repositories.workout.fake_workout_repository import FakeWorkoutRepository


class FakeUnitOfWork(AbstractUnitOfWork):
    workouts: FakeWorkoutRepository = FakeWorkoutRepository()
    agonists: FakeAgonistRepository = FakeAgonistRepository()

    async def __aenter__(self) -> AbstractUnitOfWork:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self.workouts._clear_buffer()
        self.agonists._clear_buffer()

    async def commit(self) -> None:
        self.workouts._save_current_transaction()
        self.agonists._save_current_transaction()

    async def rollback(self) -> None:
        self.workouts._clear_buffer()
        self.agonists._clear_buffer()
