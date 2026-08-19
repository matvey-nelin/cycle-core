import datetime
from contextlib import nullcontext as does_not_raise
from uuid import UUID

import pytest
from uuid6 import uuid7

from domain.exceptions import DomainError, IncorrectOrderValueError, IncorrectRepsValueError, IncorrectWeightValueError, IncorrectWorkoutTimesError
from domain.workout.workout import Workout, WorkoutSet

DETERMINED_UUID_1: UUID = uuid7()
DETERMINED_UUID_2: UUID = uuid7()
DETERMINED_UUID_3: UUID = uuid7()
WORKOUT_UUID = uuid7()
EXERCISE_UUID = uuid7()


@pytest.fixture
def workout_sets():
    return [
        WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 1, 6, 20, 6, 20),  # 100
        WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 2, 6, 20, 4, 20),  # 66.67
        WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 3, 12, 5, 15, 7.5),  # 187.5
        WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 4, 12, 5, 12, 7.5),  # 150
        WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 5, 8, 80, 6, 80),  # 75
    ]


@pytest.fixture
def empty_workout_sets():
    return []


class TestWorkoutSet:
    @pytest.mark.parametrize(
        "reps_value, reps_type, exception",
        [
            pytest.param(-1, "planned_reps", pytest.raises(IncorrectRepsValueError), id="pass_negative_limit_value_to_planned_reps"),
            pytest.param(-12345, "planned_reps", pytest.raises(IncorrectRepsValueError), id="pass_negative_value_to_planned_reps"),
            pytest.param(-1, "actual_reps", pytest.raises(IncorrectRepsValueError), id="pass_negative_limit_value_to_actual_reps"),
            pytest.param(-12345, "actual_reps", pytest.raises(IncorrectRepsValueError), id="pass_negative_value_to_actual_reps"),
        ],
    )
    def test_reps_cannot_be_negative(self, reps_value: int, reps_type: str, exception):
        with exception:
            if reps_type == "planned_reps":
                WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 1, planned_reps=reps_value)

            elif reps_type == "actual_reps":
                WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 1, actual_reps=reps_value)

    @pytest.mark.parametrize(
        "reps_value, result_reps_value, reps_type",
        [
            pytest.param(0, 0, "planned_reps", id="pass_zero_value_to_planned_reps"),
            pytest.param(1, 1, "planned_reps", id="pass_positive_limit_value_to_planned_reps"),
            pytest.param(25, 25, "planned_reps", id="pass_positive_value_to_planned_reps"),
            pytest.param(0, 0, "actual_reps", id="pass_zero_value_to_actual_reps"),
            pytest.param(1, 1, "actual_reps", id="pass_positive_limit_value_to_actual_reps"),
            pytest.param(25, 25, "actual_reps", id="pass_positive_value_to_actual_reps"),
        ],
    )
    def test_reps_can_be_positive_and_zero(self, reps_value: int, result_reps_value: int, reps_type: str):
        if reps_type == "planned_reps":
            workout_set = WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 1, planned_reps=reps_value)
            assert workout_set.planned_reps == result_reps_value

        elif reps_type == "actual_reps":
            workout_set = WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 1, actual_reps=reps_value)
            assert workout_set.actual_reps == result_reps_value

    @pytest.mark.parametrize(
        "weight_value, weight_type, exception",
        [
            pytest.param(-1, "planned_weight", pytest.raises(IncorrectWeightValueError), id="pass_negative_limit_value_to_planned_weight"),
            pytest.param(-12345, "planned_weight", pytest.raises(IncorrectWeightValueError), id="pass_negative_value_to_planned_weight"),
            pytest.param(-1, "actual_weight", pytest.raises(IncorrectWeightValueError), id="pass_negative_limit_value_to_actual_weight"),
            pytest.param(-12345, "actual_weight", pytest.raises(IncorrectWeightValueError), id="pass_negative_value_to_actual_weight"),
        ],
    )
    def test_weight_cannot_be_negative(self, weight_value: int, weight_type: str, exception):
        with exception:
            if weight_type == "planned_weight":
                WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 1, planned_weight=weight_value)

            elif weight_type == "actual_weight":
                WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 1, actual_weight=weight_value)

    @pytest.mark.parametrize(
        "weight_value, result_weight_value, weight_type",
        [
            pytest.param(0, 0, "planned_weight", id="pass_zero_value_to_planned_weight"),
            pytest.param(1, 1, "planned_weight", id="pass_positive_limit_value_to_planned_weight"),
            pytest.param(25, 25, "planned_weight", id="pass_positive_value_to_planned_weight"),
            pytest.param(0, 0, "actual_weight", id="pass_zero_value_to_actual_weight"),
            pytest.param(1, 1, "actual_weight", id="pass_positive_limit_value_to_actual_weight"),
            pytest.param(25, 25, "actual_weight", id="pass_positive_value_to_actual_weight"),
        ],
    )
    def test_weight_can_be_positive_and_zero(self, weight_value: int, result_weight_value: int, weight_type: str):
        if weight_type == "planned_weight":
            workout_set = WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 1, planned_weight=weight_value)
            assert workout_set.planned_weight == result_weight_value

        elif weight_type == "actual_weight":
            workout_set = WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 1, actual_weight=weight_value)
            assert workout_set.actual_weight == result_weight_value

    @pytest.mark.parametrize(
        "weight_value, result_weight_value, weight_type",
        [
            pytest.param(0, 0, "planned_weight", id="pass_integer_value_to_planned_weight"),
            pytest.param(1.0, 1.0, "planned_weight", id="pass_float_value_to_planned_weight"),
            pytest.param(0, 0, "actual_weight", id="pass_integer_value_to_actual_weight"),
            pytest.param(1.0, 1.0, "actual_weight", id="pass_float_value_to_actual_weight"),
        ],
    )
    def test_weight_can_accept_integer_and_float(
        self, weight_value: float, result_weight_value: float, weight_type: str
    ):
        if weight_type == "planned_weight":
            workout_set = WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 1, planned_weight=weight_value)
            assert workout_set.planned_weight == result_weight_value
            assert isinstance(workout_set.planned_weight, float)

        elif weight_type == "actual_weight":
            workout_set = WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 1, actual_weight=weight_value)
            assert workout_set.actual_weight == result_weight_value
            assert isinstance(workout_set.actual_weight, float)

    def test_reps_default_value_is_zero(self):
        workout_set = WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 1)
        assert workout_set.planned_reps == 0
        assert workout_set.actual_reps == 0

    def test_weights_default_value_is_zero(self):
        workout_set = WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 1)
        assert workout_set.planned_weight == 0
        assert workout_set.actual_weight == 0

    @pytest.mark.parametrize(
        "field_name, invalid_value, exception",
        [
            pytest.param("planned_reps", -1, pytest.raises(IncorrectRepsValueError), id="negative_planned_reps"),
            pytest.param("actual_reps", -1, pytest.raises(IncorrectRepsValueError), id="negative_actual_reps"),
            pytest.param("planned_weight", -1, pytest.raises(IncorrectWeightValueError), id="negative_planned_weight"),
            pytest.param("actual_weight", -1, pytest.raises(IncorrectWeightValueError), id="negative_actual_weight"),
            pytest.param("order", 0, pytest.raises(IncorrectOrderValueError), id="zero_order"),
        ],
    )
    def test_validation_on_change_exceptions(self, field_name: str, invalid_value: float, exception):
        workout_set = WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 1)
        with exception:
            setattr(workout_set, field_name, invalid_value)

    @pytest.mark.parametrize(
        "planned_reps, planned_weight, result_planned_tonnage",
        [
            pytest.param(0, 0, 0, id="planned_tonnage_equals_zero"),
            pytest.param(6, 0, 6, id="planned_tonnage_equals_reps"),
            pytest.param(1, 0.5, 1, id="planned_weight_less_than_one"),
            pytest.param(6, 80, 480, id="planned_tonnage_equals_product_of_numbers"),
        ],
    )
    def test_planned_tonnage_calculation(self, planned_reps: int, planned_weight: float, result_planned_tonnage: float):
        workout_set = WorkoutSet(
            WORKOUT_UUID, EXERCISE_UUID, 1, planned_reps=planned_reps, planned_weight=planned_weight
        )
        assert workout_set.planned_tonnage == result_planned_tonnage

    @pytest.mark.parametrize(
        "actual_reps, actual_weight, result_actual_tonnage",
        [
            pytest.param(0, 0, 0, id="actual_tonnage_equals_zero"),
            pytest.param(6, 0, 6, id="actual_tonnage_equals_reps"),
            pytest.param(1, 0.5, 1, id="actual_weight_less_than_one"),
            pytest.param(6, 80, 480, id="actual_tonnage_equals_product_of_numbers"),
        ],
    )
    def test_actual_tonnage_calculation(self, actual_reps: int, actual_weight: float, result_actual_tonnage: float):
        workout_set = WorkoutSet(WORKOUT_UUID, EXERCISE_UUID, 1, actual_reps=actual_reps, actual_weight=actual_weight)
        assert workout_set.actual_tonnage == result_actual_tonnage

    @pytest.mark.parametrize(
        "planned_reps, planned_weight, actual_reps, actual_weight, result_completion_percentage",
        [
            pytest.param(0, 0, 0, 0, 0, id="completion_percentage_equals_zero"),
            pytest.param(
                0,
                0,
                6,
                10,
                0,
                id="completion_percentage_equals_zero_with_non_zero_actual_tonnage",
            ),
            pytest.param(5, 0, 6, 0, 120, id="completion_percentage_with_zero_weights"),
            pytest.param(
                8,
                60,
                8,
                90,
                150,
                id="completion_percentage_when_actual_weight_exceeds_planned_weight",
            ),
            pytest.param(
                12,
                25,
                15,
                25,
                125,
                id="completion_percentage_when_actual_reps_exceeds_planned_reps",
            ),
            pytest.param(
                8,
                60,
                8,
                40,
                66.67,
                id="completion_percentage_when_actual_weight_less_planned_weight",
            ),
            pytest.param(
                12,
                25,
                10,
                25,
                83.33,
                id="completion_percentage_when_actual_reps_less_planned_reps",
            ),
        ],
    )
    def test_completion_percentage_calculation(
        self,
        planned_reps: int,
        planned_weight: float,
        actual_reps: int,
        actual_weight: float,
        result_completion_percentage: float,
    ):
        workout_set = WorkoutSet(
            workout_id=WORKOUT_UUID,
            exercise_id=EXERCISE_UUID,
            order=1,
            planned_reps=planned_reps,
            planned_weight=planned_weight,
            actual_reps=actual_reps,
            actual_weight=actual_weight,
        )
        assert workout_set.completion_percentage == result_completion_percentage


class TestWorkout:
    def test_workout_with_all_times_none(self):
        workout = Workout()
        assert workout.planned_start_time is None
        assert workout.planned_end_time is None
        assert workout.actual_start_time is None
        assert workout.actual_end_time is None

    @pytest.mark.parametrize(
        "time_type, time_value",
        [
            pytest.param(
                "planned_start_time",
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
                id="only_planned_start_time",
            ),
            pytest.param(
                "planned_end_time",
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
                id="only_planned_end_time",
            ),
            pytest.param(
                "actual_start_time",
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
                id="only_actual_start_time",
            ),
            pytest.param(
                "actual_end_time",
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
                id="only_actual_end_time",
            ),
        ],
    )
    def test_create_workout_with_incomplete_data(self, time_type: str, time_value: datetime.datetime):
        workout = Workout()
        setattr(workout, time_type, time_value)
        assert getattr(workout, time_type) == time_value

        for field in ["planned_start_time", "planned_end_time", "actual_start_time", "actual_end_time"]:
            if field != time_type:
                assert getattr(workout, field) is None

    @pytest.mark.parametrize(
        "start_time, end_time, exception",
        [
            pytest.param(
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
                does_not_raise(),
                id="planned_times_equals",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 00, 00, 00, tzinfo=datetime.UTC),
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
                does_not_raise(),
                id="planned_start_time_less_end_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
                datetime.datetime(2026, 8, 1, 00, 00, 00, tzinfo=datetime.UTC),
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
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
                does_not_raise(),
                id="actual_times_equals",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 00, 00, 00, tzinfo=datetime.UTC),
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
                does_not_raise(),
                id="actual_start_time_less_end_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
                datetime.datetime(2026, 8, 1, 00, 00, 00, tzinfo=datetime.UTC),
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
            assert (workout.actual_start_time == start_time) and (workout.actual_end_time == end_time)

    @pytest.mark.parametrize(
        "time_value, time_type, exception",
        [
            pytest.param(
                datetime.datetime(2026, 8, 1, 12, 30, 00, tzinfo=datetime.UTC),
                "start_time",
                does_not_raise(),
                id="changed_start_time_equals_end_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 11, 00, 00, tzinfo=datetime.UTC),
                "start_time",
                does_not_raise(),
                id="changed_start_time_less_end_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 13, 00, 00, tzinfo=datetime.UTC),
                "start_time",
                pytest.raises(IncorrectWorkoutTimesError),
                id="changed_start_time_exceeds_end_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
                "end_time",
                does_not_raise(),
                id="changed_end_time_equals_start_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 11, 00, 00, tzinfo=datetime.UTC),
                "end_time",
                pytest.raises(IncorrectWorkoutTimesError),
                id="changed_end_time_less_start_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 13, 00, 00, tzinfo=datetime.UTC),
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
            planned_start_time=datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
            planned_end_time=datetime.datetime(2026, 8, 1, 12, 30, 00, tzinfo=datetime.UTC),
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
                datetime.datetime(2026, 8, 1, 12, 30, 00, tzinfo=datetime.UTC),
                "start_time",
                does_not_raise(),
                id="changed_start_time_equals_end_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 11, 00, 00, tzinfo=datetime.UTC),
                "start_time",
                does_not_raise(),
                id="changed_start_time_less_end_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 13, 00, 00, tzinfo=datetime.UTC),
                "start_time",
                pytest.raises(IncorrectWorkoutTimesError),
                id="changed_start_time_exceeds_end_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
                "end_time",
                does_not_raise(),
                id="changed_end_time_equals_start_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 11, 00, 00, tzinfo=datetime.UTC),
                "end_time",
                pytest.raises(IncorrectWorkoutTimesError),
                id="changed_end_time_less_start_time",
            ),
            pytest.param(
                datetime.datetime(2026, 8, 1, 13, 00, 00, tzinfo=datetime.UTC),
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
            actual_start_time=datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
            actual_end_time=datetime.datetime(2026, 8, 1, 12, 30, 00, tzinfo=datetime.UTC),
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
            planned_start_time=datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
            planned_end_time=datetime.datetime(2026, 8, 1, 12, 30, 00, tzinfo=datetime.UTC),
        )

        workout.planned_start_time = None
        assert workout.planned_start_time is None

        workout.planned_end_time = None
        assert workout.planned_end_time is None

    def test_actual_time_changed_to_none(self):
        workout = Workout(
            actual_start_time=datetime.datetime(2026, 8, 1, 12, 00, 00, tzinfo=datetime.UTC),
            actual_end_time=datetime.datetime(2026, 8, 1, 12, 30, 00, tzinfo=datetime.UTC),
        )

        workout.actual_start_time = None
        assert workout.actual_start_time is None

        workout.actual_end_time = None
        assert workout.actual_end_time is None

    def test_workout_planned_tonnage_calculation_with_sets(self, workout_sets):
        workout = Workout()
        for wset in workout_sets:
            workout.add_set(
                exercise_id=wset.exercise_id,
                planned_reps=wset.planned_reps,
                planned_weight=wset.planned_weight,
                actual_reps=wset.actual_reps,
                actual_weight=wset.actual_weight,
            )
        assert (workout.planned_tonnage == 1000) and isinstance(workout.planned_tonnage, float)

    def test_workout_actual_tonnage_calculation_with_sets(self, workout_sets):
        workout = Workout()
        for wset in workout_sets:
            workout.add_set(
                exercise_id=wset.exercise_id,
                planned_reps=wset.planned_reps,
                planned_weight=wset.planned_weight,
                actual_reps=wset.actual_reps,
                actual_weight=wset.actual_weight,
            )
        assert (workout.actual_tonnage == 882.5) and isinstance(workout.actual_tonnage, float)

    def test_workout_planned_tonnage_calculation_without_sets(self, empty_workout_sets):
        workout = Workout()
        for wset in empty_workout_sets:
            workout.add_set(
                exercise_id=wset.exercise_id,
                planned_reps=wset.planned_reps,
                planned_weight=wset.planned_weight,
                actual_reps=wset.actual_reps,
                actual_weight=wset.actual_weight,
            )
        assert (workout.planned_tonnage == 0) and isinstance(workout.planned_tonnage, float)

    def test_workout_actual_tonnage_calculation_without_sets(self, empty_workout_sets):
        workout = Workout()
        for wset in empty_workout_sets:
            workout.add_set(
                exercise_id=wset.exercise_id,
                planned_reps=wset.planned_reps,
                planned_weight=wset.planned_weight,
                actual_reps=wset.actual_reps,
                actual_weight=wset.actual_weight,
            )
        assert (workout.actual_tonnage == 0) and isinstance(workout.actual_tonnage, float)

    def test_workout_completion_percentage_calculation_with_sets(self, workout_sets):
        workout = Workout()
        for wset in workout_sets:
            workout.add_set(
                exercise_id=wset.exercise_id,
                planned_reps=wset.planned_reps,
                planned_weight=wset.planned_weight,
                actual_reps=wset.actual_reps,
                actual_weight=wset.actual_weight,
            )
        assert (workout.completion_percentage == 115.83) and isinstance(workout.completion_percentage, float)

    def test_workout_completion_percentage_calculation_without_sets(self, empty_workout_sets):
        workout = Workout()
        for wset in empty_workout_sets:
            workout.add_set(
                exercise_id=wset.exercise_id,
                planned_reps=wset.planned_reps,
                planned_weight=wset.planned_weight,
                actual_reps=wset.actual_reps,
                actual_weight=wset.actual_weight,
            )
        assert (workout.completion_percentage == 0) and isinstance(workout.completion_percentage, float)

    def test_can_remove_set_after_creation(self, workout_sets):
        workout = Workout()
        for wset in workout_sets:
            workout.add_set(
                exercise_id=wset.exercise_id,
                planned_reps=wset.planned_reps,
                planned_weight=wset.planned_weight,
                actual_reps=wset.actual_reps,
                actual_weight=wset.actual_weight,
            )

        workout_set = workout.sets[0]
        workout.remove_set(workout_set.id)
        assert workout_set not in workout.sets
        assert [wset.order for wset in workout.sets] == [1, 2, 3, 4]

    def test_workout_set_has_correct_workout_id_after_added(self):
        workout = Workout()
        workout.add_set(exercise_id=EXERCISE_UUID)
        assert workout.sets[0].workout_id == workout.id

    def test_workout_set_has_correct_order_after_added(self, workout_sets):
        workout = Workout()
        for wset in workout_sets:
            workout.add_set(
                exercise_id=wset.exercise_id,
                planned_reps=wset.planned_reps,
                planned_weight=wset.planned_weight,
                actual_reps=wset.actual_reps,
                actual_weight=wset.actual_weight,
            )

        assert [wset.order for wset in workout.sets] == [wset.order for wset in workout_sets]
