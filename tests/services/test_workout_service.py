import datetime

import pytest
from sqlalchemy import text
from uuid6 import uuid7

from domain.workout.workout import Workout, WorkoutSet
from services.exceptions import WorkoutNotFoundError, WorkoutSetNotFoundError
from services.workout_service import WorkoutService

DETERMINED_UUID_1 = uuid7()
DETERMINED_UUID_2 = uuid7()
DETERMINED_UUID_3 = uuid7()
EXERCISE_UUID = uuid7()


@pytest.fixture
async def exercise(sqlalchemy_repository):
    repo = sqlalchemy_repository

    # Inserting the exercise for data integrity (workout set 'exercise_id' not nullable)
    await repo.session.execute(
        text("INSERT INTO exercises (id, name) VALUES (:id, :name)"),
        {"id": EXERCISE_UUID, "name": "Squat"},
    )
    await repo.session.commit()


class TestWorkoutService:
    async def test_create_workout(
        self,
        double_uow,
    ):
        service = WorkoutService(double_uow)

        workout = Workout(
            datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
            datetime.datetime(2026, 8, 1, 13, 00, 00, tzinfo=datetime.UTC),
            datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
            datetime.datetime(2026, 8, 1, 13, 00, 00, tzinfo=datetime.UTC),
        )

        with pytest.raises(WorkoutNotFoundError):
            await service.get_workout(workout.id)

        created_workout_id = await service.create_workout(
            start_time=workout.planned_start_time, end_time=workout.planned_end_time
        )
        created_workout = await service.get_workout(created_workout_id)

        assert created_workout is not None
        assert created_workout.planned_start_time == workout.planned_start_time
        assert created_workout.planned_end_time == workout.planned_end_time
        assert created_workout.actual_start_time == workout.actual_start_time
        assert created_workout.actual_end_time == workout.actual_end_time

    async def test_create_workout_set(
        self,
        double_uow,
        exercise,
    ):
        service = WorkoutService(double_uow)

        workout_id = await service.create_workout()

        # Creating workout sets with service and manually
        await service.create_workout_set(workout_id, EXERCISE_UUID, 8, 60)
        await service.create_workout_set(workout_id, EXERCISE_UUID, 12, 52)

        workout = await service.get_workout(workout_id)

        workout_set1 = WorkoutSet(workout_id, EXERCISE_UUID, 1, 8, 60, 8, 60)
        workout_set2 = WorkoutSet(workout_id, EXERCISE_UUID, 2, 12, 52, 12, 52)

        # Asserting that created with service workout sets symetric with manually workout sets
        for index, workout_set in enumerate([workout_set1, workout_set2]):
            assert workout.sets[index].order == index + 1
            assert workout.sets[index].planned_reps == workout_set.planned_reps
            assert workout.sets[index].planned_weight == workout_set.planned_weight
            assert workout.sets[index].actual_reps == workout_set.actual_reps
            assert workout.sets[index].actual_weight == workout_set.actual_weight
            assert workout.sets[index].planned_tonnage == workout_set.planned_tonnage
            assert workout.sets[index].actual_tonnage == workout_set.actual_tonnage

    async def test_create_workout_set_exception(
        self,
        double_uow,
        exercise,
    ):
        service = WorkoutService(double_uow)
        non_added_workout = Workout()

        # Testing raising exception with non added workout
        with pytest.raises(WorkoutNotFoundError):
            await service.create_workout_set(non_added_workout.id, EXERCISE_UUID)

    async def test_get_workout(
        self,
        double_uow,
        exercise,
    ):
        service = WorkoutService(double_uow)

        created_workout_id = await service.create_workout()
        await service.create_workout_set(created_workout_id, EXERCISE_UUID, 8, 60)
        await service.create_workout_set(created_workout_id, EXERCISE_UUID, 12, 52)
        await service.create_workout_set(created_workout_id, EXERCISE_UUID, 6, 100)

        workout = await service.get_workout(created_workout_id)

        assert workout.planned_tonnage == 1704
        assert workout.actual_tonnage == 1704
        assert workout.completion_percentage == 100

    async def test_get_workout_exception(
        self,
        double_uow,
    ):
        service = WorkoutService(double_uow)
        non_added_workout = Workout()

        # Added just first workout
        await service.create_workout()

        # Testing raising exception with non added workout
        with pytest.raises(WorkoutNotFoundError):
            await service.get_workout(non_added_workout.id)

    async def test_remove_workout_set(
        self,
        double_uow,
        exercise,
    ):
        service = WorkoutService(double_uow)

        # Create workout with sets
        created_workout_id = await service.create_workout()

        first_set_id = await service.create_workout_set(created_workout_id, EXERCISE_UUID, 8, 60)
        second_set_id = await service.create_workout_set(created_workout_id, EXERCISE_UUID, 12, 52)
        third_set_id = await service.create_workout_set(created_workout_id, EXERCISE_UUID, 6, 100)

        created_workout = await service.get_workout(created_workout_id)

        assert [first_set_id, second_set_id, third_set_id] == [wset.id for wset in created_workout.sets]
        assert [1, 2, 3] == [wset.order for wset in created_workout.sets]

        # Delete second workout set and added fourth workout set
        await service.remove_workout_set(created_workout_id, second_set_id)

        fourth_set_id = await service.create_workout_set(created_workout_id, EXERCISE_UUID, 6, 100)
        created_workout = await service.get_workout(created_workout_id)

        assert [first_set_id, third_set_id, fourth_set_id] == [wset.id for wset in created_workout.sets]
        assert [1, 2, 3] == [wset.order for wset in created_workout.sets]

    async def test_remove_workout_set_exception_workout_not_found(
        self,
        double_uow,
    ):
        service = WorkoutService(double_uow)

        with pytest.raises(WorkoutNotFoundError):
            await service.remove_workout_set(uuid7(), uuid7())

    async def test_remove_workout_set_exception_workout_set_not_found(
        self,
        double_uow,
    ):
        service = WorkoutService(double_uow)

        # Create workout with sets
        created_workout_id = await service.create_workout()

        with pytest.raises(WorkoutSetNotFoundError):
            await service.remove_workout_set(created_workout_id, uuid7())
