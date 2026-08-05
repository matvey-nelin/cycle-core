import pytest

from domain.workout_set import WorkoutSet


class TestWorkoutSet:
    @pytest.mark.parametrize(
        "reps_value, reps_type",
        [
            pytest.param(
                -1, "planned_reps", id="pass_negative_limit_value_to_planned_reps"
            ),
            pytest.param(
                -12345, "planned_reps", id="pass_negative_value_to_planned_reps"
            ),
            pytest.param(
                -1, "actual_reps", id="pass_negative_limit_value_to_actual_reps"
            ),
            pytest.param(
                -12345, "actual_reps", id="pass_negative_value_to_actual_reps"
            ),
        ],
    )
    def test_reps_cannot_be_negative(self, reps_value: int, reps_type: str):
        with pytest.raises(ValueError):
            if reps_type == "planned_reps":
                WorkoutSet("exercise1", planned_reps=reps_value)

            elif reps_type == "actual_reps":
                WorkoutSet("exercise1", actual_reps=reps_value)

    @pytest.mark.parametrize(
        "reps_value, result_reps_value, reps_type",
        [
            pytest.param(0, 0, "planned_reps", id="pass_zero_value_to_planned_reps"),
            pytest.param(
                1, 1, "planned_reps", id="pass_positive_limit_value_to_planned_reps"
            ),
            pytest.param(
                25, 25, "planned_reps", id="pass_positive_value_to_planned_reps"
            ),
            pytest.param(0, 0, "actual_reps", id="pass_zero_value_to_actual_reps"),
            pytest.param(
                1, 1, "actual_reps", id="pass_positive_limit_value_to_actual_reps"
            ),
            pytest.param(
                25, 25, "actual_reps", id="pass_positive_value_to_actual_reps"
            ),
        ],
    )
    def test_reps_can_be_positive_and_zero(
        self, reps_value: int, result_reps_value: int, reps_type: str
    ):
        if reps_type == "planned_reps":
            workout_set = WorkoutSet("exercise1", planned_reps=reps_value)
            assert workout_set.planned_reps == result_reps_value

        elif reps_type == "actual_reps":
            workout_set = WorkoutSet("exercise1", actual_reps=reps_value)
            assert workout_set.actual_reps == result_reps_value

    @pytest.mark.parametrize(
        "weight_value, weight_type",
        [
            pytest.param(
                -1, "planned_weight", id="pass_negative_limit_value_to_planned_weight"
            ),
            pytest.param(
                -12345, "planned_weight", id="pass_negative_value_to_planned_weight"
            ),
            pytest.param(
                -1, "actual_weight", id="pass_negative_limit_value_to_actual_weight"
            ),
            pytest.param(
                -12345, "actual_weight", id="pass_negative_value_to_actual_weight"
            ),
        ],
    )
    def test_weight_cannot_be_negative(self, weight_value: int, weight_type: str):
        with pytest.raises(ValueError):
            if weight_type == "planned_weight":
                WorkoutSet("exercise1", planned_weight=weight_value)

            elif weight_type == "actual_weight":
                WorkoutSet("exercise1", actual_weight=weight_value)

    @pytest.mark.parametrize(
        "weight_value, result_weight_value, weight_type",
        [
            pytest.param(
                0, 0, "planned_weight", id="pass_zero_value_to_planned_weight"
            ),
            pytest.param(
                1, 1, "planned_weight", id="pass_positive_limit_value_to_planned_weight"
            ),
            pytest.param(
                25, 25, "planned_weight", id="pass_positive_value_to_planned_weight"
            ),
            pytest.param(0, 0, "actual_weight", id="pass_zero_value_to_actual_weight"),
            pytest.param(
                1, 1, "actual_weight", id="pass_positive_limit_value_to_actual_weight"
            ),
            pytest.param(
                25, 25, "actual_weight", id="pass_positive_value_to_actual_weight"
            ),
        ],
    )
    def test_weight_can_be_positive_and_zero(
        self, weight_value: int, result_weight_value: int, weight_type: str
    ):
        if weight_type == "planned_weight":
            workout_set = WorkoutSet("exercise1", planned_weight=weight_value)
            assert workout_set.planned_weight == result_weight_value

        elif weight_type == "actual_weight":
            workout_set = WorkoutSet("exercise1", actual_weight=weight_value)
            assert workout_set.actual_weight == result_weight_value

    @pytest.mark.parametrize(
        "weight_value, result_weight_value, weight_type",
        [
            pytest.param(
                0, 0, "planned_weight", id="pass_integer_value_to_planned_weight"
            ),
            pytest.param(
                1.0, 1.0, "planned_weight", id="pass_float_value_to_planned_weight"
            ),
            pytest.param(
                0, 0, "actual_weight", id="pass_integer_value_to_actual_weight"
            ),
            pytest.param(
                1.0, 1.0, "actual_weight", id="pass_float_value_to_actual_weight"
            ),
        ],
    )
    def test_weight_can_accept_integer_and_float(
        self, weight_value: float, result_weight_value: float, weight_type: str
    ):
        if weight_type == "planned_weight":
            workout_set = WorkoutSet("exercise1", planned_weight=weight_value)
            assert workout_set.planned_weight == result_weight_value
            assert isinstance(workout_set.planned_weight, float)

        elif weight_type == "actual_weight":
            workout_set = WorkoutSet("exercise1", actual_weight=weight_value)
            assert workout_set.actual_weight == result_weight_value
            assert isinstance(workout_set.actual_weight, float)

    def test_reps_default_value_is_zero(self):
        workout_set = WorkoutSet("exercise1")
        assert workout_set.planned_reps == 0
        assert workout_set.actual_reps == 0

    def test_weights_default_value_is_zero(self):
        workout_set = WorkoutSet("exercise1")
        assert workout_set.planned_weight == 0
        assert workout_set.actual_weight == 0

    @pytest.mark.parametrize(
        "field_name, invalid_value",
        [
            pytest.param("planned_reps", -1, id="negative_planned_reps"),
            pytest.param("actual_reps", -1, id="negative_actual_reps"),
            pytest.param("planned_weight", -1, id="negative_planned_weight"),
            pytest.param("actual_weight", -1, id="negative_actual_weight"),
            pytest.param("order", 0, id="zero_order"),
        ],
    )
    def test_validation_on_change(self, field_name: str, invalid_value: float):
        workout_set = WorkoutSet(
            "exercise1",
        )
        with pytest.raises(ValueError):
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
    def test_planned_tonnage_calculation(
        self, planned_reps: int, planned_weight: float, result_planned_tonnage: float
    ):
        workout_set = WorkoutSet(
            "exercise1", planned_reps=planned_reps, planned_weight=planned_weight
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
    def test_actual_tonnage_calculation(
        self, actual_reps: int, actual_weight: float, result_actual_tonnage: float
    ):
        workout_set = WorkoutSet(
            "exercise1", actual_reps=actual_reps, actual_weight=actual_weight
        )
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
            "exercise1",
            planned_reps=planned_reps,
            planned_weight=planned_weight,
            actual_reps=actual_reps,
            actual_weight=actual_weight,
        )
        assert workout_set.completion_percentage == result_completion_percentage
