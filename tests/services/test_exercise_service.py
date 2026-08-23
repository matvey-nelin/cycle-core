import pytest

from domain.agonist.agonist import Agonist
from domain.exceptions import DuplicateAgonistIdError, IncorrectExerciseNameError, NonExistentAgonistIdError
from domain.exercise.exercise import Exercise
from services.abstract_unit_of_work import AbstractUnitOfWork
from services.exceptions import AgonistNotFoundError, ExerciseNotFoundError
from services.exercise_service import ExerciseService


@pytest.fixture
def service(double_uow):
    uow: AbstractUnitOfWork = double_uow
    return ExerciseService(uow)


class TestExerciseService:
    async def test_create_exercise(
        self,
        double_uow,
    ):
        uow: AbstractUnitOfWork = double_uow
        service = ExerciseService(uow)

        exercise_id = await service.create_exercise("Bench press")
        async with uow:
            exercise = await uow.exercises.get_by_id(exercise_id)

        assert exercise is not None
        assert exercise.name == "Bench press"

    async def test_create_exercise_with_incorrect_exercise_name_error(
        self,
        service,
    ):
        with pytest.raises(IncorrectExerciseNameError):
            await service.create_exercise("")

    async def test_get_exercise(
        self,
        service,
    ):
        exercise_id = await service.create_exercise("Bench press")
        exercise = await service.get_exercise(exercise_id)

        assert exercise.id == exercise_id
        assert exercise.name == "Bench press"

    async def test_get_exercise_with_exercise_not_found_error(
        self,
        service,
    ):
        exercise = Exercise("Bench press")

        with pytest.raises(ExerciseNotFoundError):
            await service.get_exercise(exercise.id)

    async def test_update_exercise(
        self,
        service,
    ):
        exercise_id = await service.create_exercise("Bench press")
        await service.update_exercise(exercise_id, "Squat")

        exercise = await service.get_exercise(exercise_id)

        assert exercise.id == exercise_id
        assert exercise.name == "Squat"

    async def test_update_exercise_with_exercise_not_found_error(
        self,
        service,
    ):
        exercise = Exercise("Bench press")

        with pytest.raises(ExerciseNotFoundError):
            await service.update_exercise(exercise.id, "Squat")

    async def test_update_exercise_with_incorrect_exercise_name_error(
        self,
        service,
    ):
        exercise_id = await service.create_exercise("Bench press")

        with pytest.raises(IncorrectExerciseNameError):
            await service.update_exercise(exercise_id, "")

    async def test_add_agonist(
        self,
        double_uow,
    ):
        uow: AbstractUnitOfWork = double_uow
        service = ExerciseService(uow)

        exercise_id = await service.create_exercise("Bench press")

        async with uow:
            agonist = Agonist("Pectoralis major")
            await uow.agonists.create(agonist)
            await uow.commit()
        await service.add_agonist(exercise_id, agonist.id)

        exercise = await service.get_exercise(exercise_id)

        assert exercise.id == exercise_id
        assert exercise.name == "Bench press"
        assert exercise.agonist_ids == [agonist.id]

    async def test_add_agonist_with_exercise_not_found_error(
        self,
        double_uow,
    ):
        uow: AbstractUnitOfWork = double_uow
        service = ExerciseService(uow)

        exercise = Exercise("Bench press")

        async with uow:
            agonist = Agonist("Pectoralis major")
            await uow.agonists.create(agonist)
            await uow.commit()

        with pytest.raises(ExerciseNotFoundError):
            await service.add_agonist(exercise.id, agonist.id)

    async def test_add_agonist_with_agonist_not_found_error(
        self,
        double_uow,
    ):
        uow: AbstractUnitOfWork = double_uow
        service = ExerciseService(uow)

        exercise_id = await service.create_exercise("Bench press")
        agonist = Agonist("Pectoralis major")

        with pytest.raises(AgonistNotFoundError):
            await service.add_agonist(exercise_id, agonist.id)

    async def test_add_agonist_with_duplicate_agonist_id_error(
        self,
        double_uow,
    ):
        uow: AbstractUnitOfWork = double_uow
        service = ExerciseService(uow)

        exercise_id = await service.create_exercise("Bench press")

        async with uow:
            agonist = Agonist("Pectoralis major")
            await uow.agonists.create(agonist)
            await uow.commit()
        await service.add_agonist(exercise_id, agonist.id)

        with pytest.raises(DuplicateAgonistIdError):
            await service.add_agonist(exercise_id, agonist.id)

    async def test_remove_agonist(
        self,
        double_uow,
    ):
        uow: AbstractUnitOfWork = double_uow
        service = ExerciseService(uow)

        exercise_id = await service.create_exercise("Bench press")

        async with uow:
            agonist = Agonist("Pectoralis major")
            await uow.agonists.create(agonist)
            await uow.commit()

        await service.add_agonist(exercise_id, agonist.id)
        exercise = await service.get_exercise(exercise_id)
        assert exercise.id == exercise_id
        assert exercise.agonist_ids == [agonist.id]

        await service.remove_agonist(exercise_id, agonist.id)
        exercise = await service.get_exercise(exercise_id)
        assert exercise.id == exercise_id
        assert exercise.agonist_ids == []

    async def test_remove_agonist_with_exercise_not_found_error(
        self,
        double_uow,
    ):
        uow: AbstractUnitOfWork = double_uow
        service = ExerciseService(uow)

        exercise = Exercise("Bench press")

        async with uow:
            agonist = Agonist("Pectoralis major")
            await uow.agonists.create(agonist)
            await uow.commit()

        with pytest.raises(ExerciseNotFoundError):
            await service.remove_agonist(exercise.id, agonist.id)

    async def test_remove_agonist_with_non_existent_agonist_id_error(
        self,
        double_uow,
    ):
        uow: AbstractUnitOfWork = double_uow
        service = ExerciseService(uow)

        exercise_id = await service.create_exercise("Bench press")

        async with uow:
            agonist = Agonist("Pectoralis major")
            await uow.agonists.create(agonist)
            await uow.commit()

        with pytest.raises(NonExistentAgonistIdError):
            await service.remove_agonist(exercise_id, agonist.id)
