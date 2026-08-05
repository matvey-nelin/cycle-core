import datetime

import pytest

from domain.workout import Workout
from domain.workout_set import WorkoutSet
from repositories.workout_repositories import InMemoryWorkoutRepository
from services.exceptions import WorkoutNotFoundError
from services.workout_service import WorkoutService


class TestWorkoutService:
    def test_create_workout(self):
        service = WorkoutService(InMemoryWorkoutRepository())

        workout = Workout(
            datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
            datetime.datetime(2026, 8, 1, 13, 00, 00, tzinfo=datetime.timezone.utc),
            datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
            datetime.datetime(2026, 8, 1, 13, 00, 00, tzinfo=datetime.timezone.utc),
        )

        created_workout = service.repository.get_by_id(workout.id)
        assert created_workout is None

        created_workout_id = service.create_workout(
            workout.planned_start_time, workout.planned_end_time
        )
        created_workout = service.repository.get_by_id(created_workout_id)

        assert created_workout is not None
        assert created_workout.planned_start_time == workout.planned_start_time
        assert created_workout.planned_end_time == workout.planned_end_time
        assert created_workout.actual_start_time == workout.actual_start_time
        assert created_workout.actual_end_time == workout.actual_end_time

    def test_create_workout_set(self):
        service = WorkoutService(InMemoryWorkoutRepository())

        workout_id = service.create_workout()
        workout = service.repository.get_by_id(workout_id)

        service.create_workout_set(workout_id, "e1", 8, 60)
        service.create_workout_set(workout_id, "e2", 12, 52)

        workout_set1 = WorkoutSet("e1", 8, 60, 8, 60)
        workout_set2 = WorkoutSet("e2", 12, 52, 12, 52)

        assert workout is not None

        for index, workout_set in enumerate([workout_set1, workout_set2]):
            assert workout.sets[index].planned_tonnage == workout_set.planned_tonnage
            assert workout.sets[index].actual_tonnage == workout_set.actual_tonnage

            assert workout.sets[index].order == index + 1

    def test_get_workout_statistics(self):
        service = WorkoutService(InMemoryWorkoutRepository())

        created_workout_id = service.create_workout()
        service.create_workout_set(created_workout_id, "e1", 8, 60)
        service.create_workout_set(created_workout_id, "e2", 12, 52)
        service.create_workout_set(created_workout_id, "e3", 6, 100)

        got_workout = service.get_workout(created_workout_id)

        assert got_workout.planned_tonnage == 1704
        assert got_workout.actual_tonnage == 1704
        assert got_workout.completion_percentage == 100

    def test_add_workout_set_workout_not_found_error(self):
        service = WorkoutService(InMemoryWorkoutRepository())

        workout1 = Workout()
        workout2 = Workout()

        # Added just first workout
        service.repository.add(workout1)

        # Testing raising exception with not added workout
        with pytest.raises(WorkoutNotFoundError):
            service.create_workout_set(workout2.id, "exercise1")

    def test_get_workout_statistics_workout_not_found_error(self):
        service = WorkoutService(InMemoryWorkoutRepository())

        workout1 = Workout()
        workout2 = Workout()

        # Added just first workout
        service.repository.add(workout1)

        # Testing raising exception with not added workout
        with pytest.raises(WorkoutNotFoundError):
            service.get_workout(workout2.id)
