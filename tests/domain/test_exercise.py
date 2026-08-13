from typing import Any
from uuid import UUID

import pytest
from uuid6 import uuid7

from domain.exercise.exercise import Exercise

DETERMINED_UUID_1 = uuid7()
DETERMINED_UUID_2 = uuid7()
DETERMINED_UUID_3 = uuid7()
DETERMINED_UUID_4 = uuid7()


class TestExercise:
    @pytest.mark.parametrize(
        "name",
        [
            pytest.param("", id="empty_name"),
            pytest.param(" ", id="only_space_name"),
            pytest.param("\t", id="only_tabulation_name"),
            pytest.param("\n", id="only_new_line_characters_name"),
        ],
    )
    def test_name_cannot_be_empty(self, name: str):
        with pytest.raises(ValueError):
            Exercise(name)

    @pytest.mark.parametrize(
        "name",
        [
            pytest.param("e" * 101, id="101_characters_name_error"),
            pytest.param("e" * 200, id="200_characters_name_error"),
        ],
    )
    def test_name_cannot_exceeding_100_characters(self, name: str):
        with pytest.raises(ValueError):
            Exercise(name)

    @pytest.mark.parametrize(
        "name, result_name",
        [
            pytest.param("Bench press", "Bench press", id="normal_name_passes"),
            pytest.param("E", "E", id="1_character_name_passes"),
            pytest.param("E" * 100, "E" * 100, id="100_characters_name_passes"),
        ],
    )
    def test_name_correct_passed(self, name: str, result_name: str):
        exercise = Exercise(name)
        assert exercise.name == result_name

    @pytest.mark.parametrize(
        "name, result_name",
        [
            pytest.param(" Bench press", "Bench press", id="leading_space"),
            pytest.param("Bench press ", "Bench press", id="trailing_space"),
            pytest.param("\tBench press", "Bench press", id="leading_tab"),
            pytest.param("Bench press\t", "Bench press", id="trailing_tab"),
            pytest.param("\nBench press", "Bench press", id="leading_newline"),
            pytest.param("Bench press\n", "Bench press", id="trailing_newline"),
        ],
    )
    def test_name_correct_striped(self, name: str, result_name: str):
        exercise = Exercise(name)
        assert exercise.name == result_name

    @pytest.mark.parametrize(
        "initial_name, changed_name, result_name",
        [
            pytest.param("Bench press", "Bench press ", "Bench press", id="trailing_space"),
            pytest.param("Bench press", " Bench press", "Bench press", id="leading_space"),
            pytest.param("Bench press", "\tBench press\t", "Bench press", id="tabs"),
        ],
    )
    def test_name_striped_after_changes(self, initial_name: str, changed_name: str, result_name: str):
        exercise = Exercise(initial_name)
        exercise.name = changed_name
        assert exercise.name == result_name

    @pytest.mark.parametrize(
        "changed_name",
        [
            pytest.param("", id="empty_string"),
            pytest.param("   ", id="only_spaces"),
            pytest.param("a" * 101, id="exceeds_100_characters"),
        ],
    )
    def test_name_validation_error_on_change(self, changed_name: str):
        exercise = Exercise("Bench press")
        with pytest.raises(ValueError):
            exercise.name = changed_name

    @pytest.mark.parametrize(
        "name, agonist_ids, result_agonist_ids",
        [
            pytest.param("Pull-ups", None, [], id="none_agonist_ids_value"),
            pytest.param("Pull-ups", [], [], id="empty_list_agonist_ids_value"),
            pytest.param(
                "Pull-ups",
                [DETERMINED_UUID_1],
                [DETERMINED_UUID_1],
                id="1_element_agonist_ids_value",
            ),
            pytest.param(
                "Pull-ups",
                [DETERMINED_UUID_1, DETERMINED_UUID_2, DETERMINED_UUID_3],
                [DETERMINED_UUID_1, DETERMINED_UUID_2, DETERMINED_UUID_3],
                id="few_elements_agonist_ids_value",
            ),
        ],
    )
    def test_exercise_can_be_with_and_without_agonists(
        self, name: str, agonist_ids: list[UUID] | None, result_agonist_ids: list[UUID]
    ):
        if agonist_ids is None:
            exercise = Exercise(name)
            assert exercise.agonist_ids == result_agonist_ids
        else:
            exercise = Exercise(name, agonist_ids)
            assert exercise.agonist_ids == result_agonist_ids

    @pytest.mark.parametrize(
        "agonist_ids_value",
        [
            pytest.param(1, id="int_in_agonist_ids"),
            pytest.param([1], id="list_of_integer_in_agonist_ids"),
            pytest.param(["String", 10], id="list_with_mixed_values_in_agonist_ids"),
        ],
    )
    def test_incorrect_value_of_agonist_ids(self, agonist_ids_value: Any):
        with pytest.raises(ValueError):
            Exercise("Bench press", agonist_ids_value)

    @pytest.mark.parametrize(
        "initial_agonist_ids_value, changed_agonist_ids_value",
        [
            pytest.param([DETERMINED_UUID_1], None, id="none_in_changed_agonist_ids"),
            pytest.param([DETERMINED_UUID_1], 1, id="int_in_changed_agonist_ids"),
            pytest.param([DETERMINED_UUID_1], [1, 2], id="list_of_integers_in_changed_agonist_ids"),
            pytest.param(
                [DETERMINED_UUID_1],
                ["String", 10],
                id="list_with_mixed_values_in_changed_agonist_ids",
            ),
        ],
    )
    def test_agonist_ids_value_changed_to_incorrect_value(
        self, initial_agonist_ids_value: list[UUID], changed_agonist_ids_value: Any
    ):
        exercise = Exercise("Bench press", initial_agonist_ids_value)

        with pytest.raises(ValueError):
            exercise.agonist_ids = changed_agonist_ids_value

    @pytest.mark.parametrize(
        "initial_agonist_ids_value, changed_agonist_ids_value, result_agonist_ids_value",
        [
            pytest.param(
                [DETERMINED_UUID_1, DETERMINED_UUID_2, DETERMINED_UUID_3],
                [],
                [],
                id="empty_list_in_changed_agonist_ids",
            ),
            pytest.param(
                [DETERMINED_UUID_1, DETERMINED_UUID_2, DETERMINED_UUID_3],
                [DETERMINED_UUID_4],
                [DETERMINED_UUID_4],
                id="list_with_1_string_in_changed_agonist_ids",
            ),
        ],
    )
    def test_agonist_ids_value_changed_to_correct_value(
        self,
        initial_agonist_ids_value: list[UUID],
        changed_agonist_ids_value: Any,
        result_agonist_ids_value: list[UUID],
    ):
        exercise = Exercise("Bench press", initial_agonist_ids_value)
        exercise.agonist_ids = changed_agonist_ids_value
        assert exercise.agonist_ids == result_agonist_ids_value
