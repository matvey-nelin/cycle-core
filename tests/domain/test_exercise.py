from typing import Any
from uuid import UUID

import pytest
from uuid6 import uuid7

from domain.exceptions import DuplicateAgonistIdError, IncorrectExerciseNameError, NonExistentAgonistIdError
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
        with pytest.raises(IncorrectExerciseNameError):
            Exercise(name)

    @pytest.mark.parametrize(
        "name",
        [
            pytest.param("e" * 101, id="101_characters_name_error"),
            pytest.param("e" * 200, id="200_characters_name_error"),
        ],
    )
    def test_name_cannot_exceeding_100_characters(self, name: str):
        with pytest.raises(IncorrectExerciseNameError):
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
        with pytest.raises(IncorrectExerciseNameError):
            exercise.name = changed_name

    def test_add_agonist(self):
        exercise = Exercise("Bench press")
        exercise.add_agonist(DETERMINED_UUID_1)
        exercise.add_agonist(DETERMINED_UUID_2)
        assert exercise.agonist_ids == [DETERMINED_UUID_1, DETERMINED_UUID_2]

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(1, id="int_in_value_of_agonist_id"),
            pytest.param("string", id="string_in_value_of_agonist_id"),
            pytest.param([], id="list_in_value_of_agonist_id"),
        ],
    )
    def test_add_agonist_with_incorrect_type_value(self, value: Any):
        exercise = Exercise("Bench press")
        with pytest.raises(TypeError):
            exercise.add_agonist(value)

    def test_add_agonist_with_duplicate(self):
        exercise = Exercise("Bench press")
        exercise.add_agonist(DETERMINED_UUID_1)
        with pytest.raises(DuplicateAgonistIdError):
            exercise.add_agonist(DETERMINED_UUID_1)

    def test_remove_agonist(self):
        exercise = Exercise("Bench press")
        exercise.add_agonist(DETERMINED_UUID_1)
        exercise.add_agonist(DETERMINED_UUID_2)
        assert exercise.agonist_ids == [DETERMINED_UUID_1, DETERMINED_UUID_2]

        exercise.remove_agonist(DETERMINED_UUID_1)
        assert exercise.agonist_ids == [DETERMINED_UUID_2]

        exercise.remove_agonist(DETERMINED_UUID_2)
        assert exercise.agonist_ids == []

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(1, id="int_in_value_of_agonist_id"),
            pytest.param("string", id="string_in_value_of_agonist_id"),
            pytest.param([], id="list_in_value_of_agonist_id"),
        ],
    )
    def test_remove_agonist_with_incorrect_type_value(self, value: Any):
        exercise = Exercise("Bench press")
        exercise.add_agonist(DETERMINED_UUID_1)
        with pytest.raises(TypeError):
            exercise.remove_agonist(value)

    def test_remove_agonist_with_non_existent_id(self):
        exercise = Exercise("Bench press")
        exercise.add_agonist(DETERMINED_UUID_1)
        with pytest.raises(NonExistentAgonistIdError):
            exercise.remove_agonist(DETERMINED_UUID_2)

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
            exercise = Exercise(name)
            for agonist_id in agonist_ids:
                exercise.add_agonist(agonist_id)
            assert exercise.agonist_ids == result_agonist_ids
