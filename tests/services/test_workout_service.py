import datetime

import pytest
from uuid6 import uuid7

from domain.exceptions import (
    IncorrectRepsValueError,
    IncorrectWeightValueError,
    IncorrectWorkoutSetIdError,
    IncorrectWorkoutTimesError,
)
from domain.exercise.exercise import Exercise
from domain.workout.workout import Workout, WorkoutSet
from services.abstract_unit_of_work import AbstractUnitOfWork
from services.exceptions import ExerciseNotFoundError, WorkoutNotFoundError
from services.workout_service import WorkoutService


@pytest.fixture
async def exercise(double_uow):
    uow: AbstractUnitOfWork = double_uow
    exercise = Exercise("Squat")

    # Inserting the exercise for data integrity (workout set 'exercise_id' not nullable)
    async with uow:
        await uow.exercises.create(exercise)
        await uow.commit()

    return exercise


@pytest.fixture
def service(double_uow):
    uow: AbstractUnitOfWork = double_uow
    return WorkoutService(uow)


class TestWorkoutService:
    async def test_create_workout(
        self,
        service,
    ):
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

    async def test_create_workout_with_incorrect_workout_times_error(
        self,
        service,
    ):
        with pytest.raises(IncorrectWorkoutTimesError):
            await service.create_workout(
                datetime.datetime(2026, 8, 20, 13, 00, 00),
                datetime.datetime(2026, 8, 20, 12, 00, 00),
            )

    async def test_get_workout(
        self,
        service,
        exercise,
    ):
        created_workout_id = await service.create_workout()
        await service.add_workout_set(created_workout_id, exercise.id, 8, 60)
        await service.add_workout_set(created_workout_id, exercise.id, 12, 52)
        await service.add_workout_set(created_workout_id, exercise.id, 6, 100)

        workout = await service.get_workout(created_workout_id)

        assert workout.planned_tonnage == 1704
        assert workout.actual_tonnage == 1704
        assert workout.completion_percentage == 100

    async def test_get_workout_with_workout_not_found_error(
        self,
        service,
    ):
        non_added_workout = Workout()
        await service.create_workout()

        with pytest.raises(WorkoutNotFoundError):
            await service.get_workout(non_added_workout.id)

    async def test_add_workout_set(
        self,
        service,
        exercise,
    ):
        workout_id = await service.create_workout()

        # Creating workout sets with service and manually
        await service.add_workout_set(workout_id, exercise.id, 8, 60)
        await service.add_workout_set(workout_id, exercise.id, 12, 52)

        workout = await service.get_workout(workout_id)

        workout_set1 = WorkoutSet(workout_id, exercise.id, 1, 8, 60, 8, 60)
        workout_set2 = WorkoutSet(workout_id, exercise.id, 2, 12, 52, 12, 52)

        # Asserting that created with service workout sets symetric with manually workout sets
        for index, workout_set in enumerate([workout_set1, workout_set2]):
            assert workout.sets[index].order == index + 1
            assert workout.sets[index].planned_reps == workout_set.planned_reps
            assert workout.sets[index].planned_weight == workout_set.planned_weight
            assert workout.sets[index].actual_reps == workout_set.actual_reps
            assert workout.sets[index].actual_weight == workout_set.actual_weight
            assert workout.sets[index].planned_tonnage == workout_set.planned_tonnage
            assert workout.sets[index].actual_tonnage == workout_set.actual_tonnage

    async def test_add_workout_set_with_workout_not_found_error(
        self,
        service,
        exercise,
    ):
        non_added_workout = Workout()

        # Testing raising exception with non added workout
        with pytest.raises(WorkoutNotFoundError):
            await service.add_workout_set(non_added_workout.id, exercise.id)

    async def test_add_workout_set_with_incorrect_reps_value_error(self, service, exercise):
        workout_id = await service.create_workout()
        with pytest.raises(IncorrectRepsValueError):
            await service.add_workout_set(workout_id, exercise.id, -1, 60)

    async def test_add_workout_set_with_incorrect_weight_value_error(self, service, exercise):
        workout_id = await service.create_workout()
        with pytest.raises(IncorrectWeightValueError):
            await service.add_workout_set(workout_id, exercise.id, 6, -60)

    async def test_add_workout_set_with_exercise_not_found_error(
        self,
        service,
    ):
        workout_id = await service.create_workout()
        with pytest.raises(ExerciseNotFoundError):
            await service.add_workout_set(workout_id, uuid7())

    async def test_remove_workout_set(
        self,
        service,
        exercise,
    ):
        # Create workout with sets
        created_workout_id = await service.create_workout()

        first_set_id = await service.add_workout_set(created_workout_id, exercise.id, 8, 60)
        second_set_id = await service.add_workout_set(created_workout_id, exercise.id, 12, 52)
        third_set_id = await service.add_workout_set(created_workout_id, exercise.id, 6, 100)

        created_workout = await service.get_workout(created_workout_id)

        assert [first_set_id, second_set_id, third_set_id] == [wset.id for wset in created_workout.sets]
        assert [1, 2, 3] == [wset.order for wset in created_workout.sets]

        # Delete second workout set and added fourth workout set
        await service.remove_workout_set(created_workout_id, second_set_id)

        fourth_set_id = await service.add_workout_set(created_workout_id, exercise.id, 6, 100)
        created_workout = await service.get_workout(created_workout_id)

        assert [first_set_id, third_set_id, fourth_set_id] == [wset.id for wset in created_workout.sets]
        assert [1, 2, 3] == [wset.order for wset in created_workout.sets]

    async def test_remove_workout_set_with_workout_not_found(
        self,
        service,
    ):
        with pytest.raises(WorkoutNotFoundError):
            await service.remove_workout_set(uuid7(), uuid7())

    async def test_remove_workout_set_with_incorrect_workout_set_id_error(
        self,
        service,
    ):
        # Create workout with sets
        created_workout_id = await service.create_workout()

        with pytest.raises(IncorrectWorkoutSetIdError):
            await service.remove_workout_set(created_workout_id, uuid7())
