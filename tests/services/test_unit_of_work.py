import pytest

from domain.workout.workout import Workout
from infrastructure.repositories.exceptions import IncorrectWorkoutIdError
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from tests.fakes.fake_unit_of_work import FakeUnitOfWork


class TestUnitOfWork:
    async def test_commit_with_one_operation(self, double_uow):
        uow: SQLAlchemyUnitOfWork | FakeUnitOfWork = double_uow

        async with uow:
            workout = Workout()
            await uow.workouts.create(workout)
            await uow.commit()

        async with uow:
            committed_workout = await uow.workouts.get_by_id(workout.id)

        assert committed_workout is not None
        assert committed_workout.id == workout.id

    async def test_rollback_with_one_operation(self, double_uow):
        uow: SQLAlchemyUnitOfWork | FakeUnitOfWork = double_uow

        async with uow:
            workout = Workout()
            await uow.workouts.create(workout)

        async with uow:
            committed_workout = await uow.workouts.get_by_id(workout.id)

        assert committed_workout is None

    async def test_rollback_on_error_with_one_operation(self, double_uow):
        uow: SQLAlchemyUnitOfWork | FakeUnitOfWork = double_uow

        with pytest.raises(IncorrectWorkoutIdError):
            async with uow:
                workout = Workout()
                await uow.workouts.update(workout)
                await uow.commit()

        async with uow:
            committed_workout = await uow.workouts.get_by_id(workout.id)

        assert committed_workout is None

    async def test_commit_with_two_operation(self, double_uow):
        uow: SQLAlchemyUnitOfWork | FakeUnitOfWork = double_uow

        async with uow:
            first_workout = Workout()
            await uow.workouts.create(first_workout)

            second_workout = Workout()
            await uow.workouts.create(second_workout)

            await uow.commit()

        async with uow:
            first_committed_workout = await uow.workouts.get_by_id(first_workout.id)
            second_committed_workout = await uow.workouts.get_by_id(second_workout.id)

        assert first_committed_workout is not None
        assert second_committed_workout is not None
        assert first_committed_workout.id == first_workout.id
        assert second_committed_workout.id == second_workout.id

    async def test_rollback_with_two_operation(self, double_uow):
        uow: SQLAlchemyUnitOfWork | FakeUnitOfWork = double_uow

        async with uow:
            first_workout = Workout()
            await uow.workouts.create(first_workout)

            second_workout = Workout()
            await uow.workouts.create(second_workout)

        async with uow:
            first_committed_workout = await uow.workouts.get_by_id(first_workout.id)
            second_committed_workout = await uow.workouts.get_by_id(second_workout.id)

        assert first_committed_workout is None
        assert second_committed_workout is None

    async def test_rollback_on_error_with_two_operation(self, double_uow):
        uow: SQLAlchemyUnitOfWork | FakeUnitOfWork = double_uow

        with pytest.raises(IncorrectWorkoutIdError):
            async with uow:
                first_workout = Workout()
                await uow.workouts.create(first_workout)

                second_workout = Workout()
                await uow.workouts.update(second_workout)

                await uow.commit()

        async with uow:
            first_committed_workout = await uow.workouts.get_by_id(first_workout.id)
            second_committed_workout = await uow.workouts.get_by_id(second_workout.id)

        assert first_committed_workout is None
        assert second_committed_workout is None
