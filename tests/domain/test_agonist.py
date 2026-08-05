import pytest

from domain.agonist import Agonist


class TestAgonist:
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
            Agonist(name)

    @pytest.mark.parametrize(
        "name",
        [
            pytest.param("a" * 101, id="101_characters_name_error"),
            pytest.param("a" * 200, id="200_characters_name_error"),
        ],
    )
    def test_name_cannot_exceeding_100_characters(self, name: str):
        with pytest.raises(ValueError):
            Agonist(name)

    @pytest.mark.parametrize(
        "name, result_name",
        [
            pytest.param(
                "Pectoralis major", "Pectoralis major", id="normal_name_passes"
            ),
            pytest.param("A", "A", id="1_character_name_passes"),
            pytest.param("A" * 100, "A" * 100, id="100_characters_name_passes"),
        ],
    )
    def test_name_correct_passed(self, name: str, result_name: str):
        agonist = Agonist(name)
        assert agonist.name == result_name

    @pytest.mark.parametrize(
        "name, result_name",
        [
            pytest.param(" Pectoralis major", "Pectoralis major", id="leading_space"),
            pytest.param("Pectoralis major ", "Pectoralis major", id="trailing_space"),
            pytest.param("\tPectoralis major", "Pectoralis major", id="leading_tab"),
            pytest.param("Pectoralis major\t", "Pectoralis major", id="trailing_tab"),
            pytest.param(
                "\nPectoralis major", "Pectoralis major", id="leading_newline"
            ),
            pytest.param(
                "Pectoralis major\n", "Pectoralis major", id="trailing_newline"
            ),
        ],
    )
    def test_name_correct_striped(self, name: str, result_name: str):
        agonist = Agonist(name)
        assert agonist.name == result_name

    @pytest.mark.parametrize(
        "initial_name, changed_name, result_name",
        [
            pytest.param(
                "Pectoralis major",
                "Pectoralis major ",
                "Pectoralis major",
                id="trailing_space",
            ),
            pytest.param(
                "Pectoralis major",
                " Pectoralis major",
                "Pectoralis major",
                id="leading_space",
            ),
            pytest.param(
                "Pectoralis major",
                "\tPectoralis major\t",
                "Pectoralis major",
                id="tabs",
            ),
        ],
    )
    def test_name_striped_after_changes(
        self, initial_name: str, changed_name: str, result_name: str
    ):
        agonist = Agonist(initial_name)
        agonist.name = changed_name
        assert agonist.name == result_name

    @pytest.mark.parametrize(
        "changed_name",
        [
            pytest.param("", id="empty_string"),
            pytest.param("   ", id="only_spaces"),
            pytest.param("a" * 101, id="exceeds_100_characters"),
        ],
    )
    def test_name_validation_error_on_change(self, changed_name: str):
        agonist = Agonist("Pectoralis major")
        with pytest.raises(ValueError):
            agonist.name = changed_name
