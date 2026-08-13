from services.workout_service import WorkoutService
from tests.fakes.fake_unit_of_work import FakeUnitOfWork

uow = FakeUnitOfWork()


def get_workout_service() -> WorkoutService:
    return WorkoutService(uow)
