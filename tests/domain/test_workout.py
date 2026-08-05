import datetime
from contextlib import nullcontext as does_not_raise

import pytest

from domain.exceptions import IncorrectWorkoutTimesError
from domain.workout import Workout
from domain.workout_set import WorkoutSet


class TestWorkout:
    @pytest.fixture
    def workout_sets(self):
        return [
            WorkoutSet("exercise1", 6, 20, 6, 20),  # 100
            WorkoutSet("exercise1", 6, 20, 4, 20),  # 66.67
            WorkoutSet("exercise2", 12, 5, 15, 7.5),  # 187.5
            WorkoutSet("exercise2", 12, 5, 12, 7.5),  # 150
            WorkoutSet("exercise3", 8, 80, 6, 80),  # 75
        ]

    @pytest.fixture
    def empty_workout_sets(self):
        return []

    @pytest.mark.parametrize(
        "time_type, time_value",
        [
            pytest.param(
                "planned_start_time",
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
                id="only_planned_start_time",
            ),
            pytest.param(
                "planned_end_time",
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
                id="only_planned_end_time",
            ),
            pytest.param(
                "actual_start_time",
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
                id="only_actual_start_time",
            ),
            pytest.param(
                "actual_end_time",
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
                id="only_actual_end_time",
            ),
        ],
    )
    def test_create_workout_with_incomplete_data(
        self, time_type: str, time_value: datetime.datetime
    ):
        workout = Workout()
        setattr(workout, time_type, time_value)
        assert getattr(workout, time_type) == time_value

        all_fields = [
            "planned_start_time",
            "planned_end_time",
            "actual_start_time",
            "actual_end_time",
        ]

        for field in all_fields:
            if field != time_type:
                assert getattr(workout, field) is None

    def test_workout_with_all_times_none(self):
        workout = Workout()
        assert workout.planned_start_time is None
        assert workout.planned_end_time is None
        assert workout.actual_start_time is None
        assert workout.actual_end_time is None

    @pytest.mark.parametrize(
        "start_time, end_time, exception",
        [
            pytest.param(
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
                does_not_raise(),
                id="planned_times_equals",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 00, 00, 00, tzinfo=datetime.timezone.utc),
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
                does_not_raise(),
                id="planned_start_time_less_end_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
                datetime.datetime(2026, 8, 1, 00, 00, 00, tzinfo=datetime.timezone.utc),
                pytest.raises(IncorrectWorkoutTimesError),
                id="planned_start_time_exceeds_end_time",
            ),
        ],
    )
    def test_create_workout_with_planned_times(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        exception: does_not_raise | pytest.RaisesExc[IncorrectWorkoutTimesError],
    ):
        with exception:
            workout = Workout(planned_start_time=start_time, planned_end_time=end_time)
            assert workout.planned_start_time == start_time
            assert workout.planned_end_time == end_time

    @pytest.mark.parametrize(
        "start_time, end_time, exception",
        [
            pytest.param(
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
                does_not_raise(),
                id="actual_times_equals",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 00, 00, 00, tzinfo=datetime.timezone.utc),
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
                does_not_raise(),
                id="actual_start_time_less_end_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
                datetime.datetime(2026, 8, 1, 00, 00, 00, tzinfo=datetime.timezone.utc),
                pytest.raises(IncorrectWorkoutTimesError),
                id="actual_start_time_exceeds_end_time",
            ),
        ],
    )
    def test_create_workout_with_actual_times(
        self,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        exception: does_not_raise | pytest.RaisesExc[IncorrectWorkoutTimesError],
    ):
        with exception:
            workout = Workout(actual_start_time=start_time, actual_end_time=end_time)
            assert (workout.actual_start_time == start_time) and (
                workout.actual_end_time == end_time
            )

    @pytest.mark.parametrize(
        "time_value, time_type, exception",
        [
            pytest.param(
                datetime.datetime(2026, 8, 1, 12, 30, 00, tzinfo=datetime.timezone.utc),
                "start_time",
                does_not_raise(),
                id="changed_start_time_equals_end_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 11, 00, 00, tzinfo=datetime.timezone.utc),
                "start_time",
                does_not_raise(),
                id="changed_start_time_less_end_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 13, 00, 00, tzinfo=datetime.timezone.utc),
                "start_time",
                pytest.raises(IncorrectWorkoutTimesError),
                id="changed_start_time_exceeds_end_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
                "end_time",
                does_not_raise(),
                id="changed_end_time_equals_start_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 11, 00, 00, tzinfo=datetime.timezone.utc),
                "end_time",
                pytest.raises(IncorrectWorkoutTimesError),
                id="changed_end_time_less_start_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 13, 00, 00, tzinfo=datetime.timezone.utc),
                "end_time",
                does_not_raise(),
                id="changed_end_time_exceeds_start_time",
            ),
        ],
    )
    def test_planned_time_changed(
        self,
        time_value: datetime.datetime,
        time_type: str,
        exception: does_not_raise | pytest.RaisesExc[IncorrectWorkoutTimesError],
    ):
        workout = Workout(
            planned_start_time=datetime.datetime(
                2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc
            ),
            planned_end_time=datetime.datetime(
                2026, 8, 1, 12, 30, 00, tzinfo=datetime.timezone.utc
            ),
        )

        with exception:
            if time_type == "start_time":
                workout.planned_start_time = time_value
                assert workout.planned_start_time == time_value
            elif time_type == "end_time":
                workout.planned_end_time = time_value
                assert workout.planned_end_time == time_value

    @pytest.mark.parametrize(
        "time_value, time_type, exception",
        [
            pytest.param(
                datetime.datetime(2026, 8, 1, 12, 30, 00, tzinfo=datetime.timezone.utc),
                "start_time",
                does_not_raise(),
                id="changed_start_time_equals_end_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 11, 00, 00, tzinfo=datetime.timezone.utc),
                "start_time",
                does_not_raise(),
                id="changed_start_time_less_end_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 13, 00, 00, tzinfo=datetime.timezone.utc),
                "start_time",
                pytest.raises(IncorrectWorkoutTimesError),
                id="changed_start_time_exceeds_end_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc),
                "end_time",
                does_not_raise(),
                id="changed_end_time_equals_start_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 11, 00, 00, tzinfo=datetime.timezone.utc),
                "end_time",
                pytest.raises(IncorrectWorkoutTimesError),
                id="changed_end_time_less_start_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 13, 00, 00, tzinfo=datetime.timezone.utc),
                "end_time",
                does_not_raise(),
                id="changed_end_time_exceeds_start_time",
            ),
        ],
    )
    def test_actual_time_changed(
        self,
        time_value: datetime.datetime,
        time_type: str,
        exception: does_not_raise | pytest.RaisesExc[IncorrectWorkoutTimesError],
    ):
        workout = Workout(
            actual_start_time=datetime.datetime(
                2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc
            ),
            actual_end_time=datetime.datetime(
                2026, 8, 1, 12, 30, 00, tzinfo=datetime.timezone.utc
            ),
        )

        with exception:
            if time_type == "start_time":
                workout.actual_start_time = time_value
                assert workout.actual_start_time == time_value
            elif time_type == "end_time":
                workout.actual_end_time = time_value
                assert workout.actual_end_time == time_value

    def test_planned_time_changed_to_none(self):
        workout = Workout(
            planned_start_time=datetime.datetime(
                2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc
            ),
            planned_end_time=datetime.datetime(
                2026, 8, 1, 12, 30, 00, tzinfo=datetime.timezone.utc
            ),
        )

        workout.planned_start_time = None
        assert workout.planned_start_time is None

        workout.planned_end_time = None
        assert workout.planned_end_time is None

    def test_actual_time_changed_to_none(self):
        workout = Workout(
            actual_start_time=datetime.datetime(
                2026, 8, 1, 12, 00, 00, tzinfo=datetime.timezone.utc
            ),
            actual_end_time=datetime.datetime(
                2026, 8, 1, 12, 30, 00, tzinfo=datetime.timezone.utc
            ),
        )

        workout.actual_start_time = None
        assert workout.actual_start_time is None

        workout.actual_end_time = None
        assert workout.actual_end_time is None

    def test_workout_planned_tonnage_calculation_with_sets(
        self, workout_sets: list[WorkoutSet]
    ):
        workout = Workout()
        for w_set in workout_sets:
            workout.add_set(w_set)
        assert (workout.planned_tonnage == 1000) and isinstance(
            workout.planned_tonnage, float
        )

    def test_workout_actual_tonnage_calculation_with_sets(
        self, workout_sets: list[WorkoutSet]
    ):
        workout = Workout()
        for w_set in workout_sets:
            workout.add_set(w_set)
        assert (workout.actual_tonnage == 882.5) and isinstance(
            workout.actual_tonnage, float
        )

    def test_workout_planned_tonnage_calculation_without_sets(
        self, empty_workout_sets: list
    ):
        workout = Workout()
        for w_set in empty_workout_sets:
            workout.add_set(w_set)
        assert (workout.planned_tonnage == 0) and isinstance(
            workout.planned_tonnage, float
        )

    def test_workout_actual_tonnage_calculation_without_sets(
        self, empty_workout_sets: list
    ):
        workout = Workout()
        for w_set in empty_workout_sets:
            workout.add_set(w_set)
        assert (workout.actual_tonnage == 0) and isinstance(
            workout.actual_tonnage, float
        )

    def test_workout_completion_percentage_calculation_with_sets(
        self, workout_sets: list[WorkoutSet]
    ):
        workout = Workout()
        for w_set in workout_sets:
            workout.add_set(w_set)
        assert (workout.completion_percentage == 115.83) and isinstance(
            workout.completion_percentage, float
        )

    def test_workout_completion_percentage_calculation_without_sets(
        self, empty_workout_sets: list
    ):
        workout = Workout()
        for w_set in empty_workout_sets:
            workout.add_set(w_set)
        assert (workout.completion_percentage == 0) and isinstance(
            workout.completion_percentage, float
        )

    def test_can_remove_set_after_creation(self, workout_sets: list[WorkoutSet]):
        workout = Workout()
        for w_set in workout_sets:
            workout.add_set(w_set)
        workout_set = workout_sets[0]

        workout.sets.remove(workout_set)
        assert workout_set not in workout.sets

    def test_workout_set_has_correct_workout_id_after_added(self):
        workout = Workout()
        workout_set = WorkoutSet("exercise1")

        assert workout_set.workout_id is None

        workout.add_set(workout_set)
        assert workout_set.workout_id == workout.id

    def test_workout_set_has_correct_order_after_added(self):
        workout = Workout()
        workout_set = WorkoutSet("exercise1", 8, 80, 5, 80)

        workout.add_set(workout_set)
        index_set = workout.sets.index(workout_set)

        assert workout.sets[index_set].order == len(workout.sets)

    def test_workout_set_has_initial_not_none_order_after_added(self):
        workout = Workout()
        workout_set = WorkoutSet("exercise1", 8, 80, 5, 80)
        workout_set.order = 3

        workout.add_set(workout_set)
        index_set = workout.sets.index(workout_set)

        assert workout.sets[index_set].order == workout_set.order

    def test_set_order_sets(self):
        workout = Workout()

        first_workout_set = WorkoutSet("exercise1")
        second_workout_set = WorkoutSet("exercise1")
        third_workout_set = WorkoutSet("exercise1")

        first_workout_set.order = 1
        second_workout_set.order = 2
        third_workout_set.order = 3

        for w_set in [second_workout_set, third_workout_set, first_workout_set]:
            workout.add_set(w_set)
        workout_orders = [workout_set.order for workout_set in workout.sets]

        assert workout_orders == [2, 3, 1]

        workout.set_order_sets()
        workout_orders = [workout_set.order for workout_set in workout.sets]
        assert workout_orders == [1, 2, 3]
