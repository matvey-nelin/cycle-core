import datetime

import pytest

from domain.workout import Workout
from repositories.workout_repositories import InMemoryWorkoutRepository


class TestInMemoryWorkoutRepository:
    @pytest.fixture
    def workouts(self) -> dict[str, Workout]:
        workouts = {}

        for _ in range(5):
            workout = Workout()
            workouts[workout.id] = workout

        return workouts

    @pytest.fixture
    def new_workout(self) -> Workout:
        return Workout(
            datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
            datetime.datetime(2026, 8, 1, 13, 00, 00, tzinfo=datetime.timezone.utc),
            datetime.datetime(2026, 8, 1, 12, 15, 00, tzinfo=datetime.timezone.utc),
            datetime.datetime(2026, 8, 1, 13, 15, 00, tzinfo=datetime.timezone.utc),
        )

    def test_get_by_id_incorrect(self, new_workout):
        repo = InMemoryWorkoutRepository()
        repo.add(new_workout)

        founded_workout = repo.get_by_id("incorrect id")

        assert founded_workout is None

    def test_get_by_id_correct(self, new_workout):
        repo = InMemoryWorkoutRepository()
        repo.add(new_workout)

        founded_workout = repo.get_by_id(new_workout.id)

        assert founded_workout is not None

        assert founded_workout == new_workout

    def test_list(self, workouts):
        repo = InMemoryWorkoutRepository(workouts)
        assert repo.get_all() == list(workouts.values())

    def test_list_ids(self, workouts):
        repo = InMemoryWorkoutRepository(workouts)
        assert repo.get_all_ids() == list(workouts.keys())

    def test_add(self, workouts, new_workout):
        repo = InMemoryWorkoutRepository(workouts)
        assert new_workout.id not in list(repo.get_all_ids())

        repo.add(new_workout)
        assert new_workout.id in list(repo.get_all_ids())

    def test_add_doesnt_change_base_dict(self, workouts, new_workout):
        repo = InMemoryWorkoutRepository(workouts)

        repo.add(new_workout)

        assert new_workout.id in list(repo.get_all_ids())
        assert new_workout.id not in list(workouts)
