from uuid import UUID

import pytest
from sqlalchemy import text

from domain.agonist.agonist import Agonist
from domain.exercise.exercise import Exercise
from infrastructure.repositories.exceptions import IncorrectAgonistIdError, IncorrectExerciseIdError
from infrastructure.repositories.exercise.sqlalchemy_exercise_repository import SQLAlchemyExerciseRepository


@pytest.fixture
async def exercise_with_agonists(session_factory):
    first_agonist = Agonist("Triceps brachii")
    second_agonist = Agonist("Pectoralis major")

    async with session_factory() as seeder:
        await seeder.execute(
            text(
                """
                INSERT INTO agonists (id, name)
                VALUES (:first_id, :first_name), (:second_id, :second_name)
                """
            ),
            {
                "first_id": first_agonist.id,
                "first_name": first_agonist.name,
                "second_id": second_agonist.id,
                "second_name": second_agonist.name,
            },
        )
        await seeder.commit()

    exercise = Exercise("Bench press")
    exercise.add_agonist(first_agonist.id)
    exercise.add_agonist(second_agonist.id)

    async with session_factory() as seeder:
        repo = SQLAlchemyExerciseRepository(seeder)
        await repo.create(exercise)
        await seeder.commit()

    return exercise


class TestExerciseRepository:
    async def test_create(
        self,
        session_factory,
        exercise_with_agonists,
    ):
        exercise = exercise_with_agonists

        async with session_factory() as reader:
            created_exercise: Exercise = (
                await reader.execute(
                    text(
                        """
                        SELECT id, name
                        FROM exercises
                        WHERE id = :id
                        """
                    ),
                    {"id": exercise.id},
                )
            ).one()
            received_agonist_ids: tuple[tuple[UUID]] = (
                await reader.execute(
                    text(
                        """
                        SELECT ea.agonist_id
                        FROM exercise_agonist AS ea
                        JOIN agonists AS a ON a.id = ea.agonist_id
                        WHERE ea.exercise_id = :exercise_id
                        ORDER BY a.name ASC
                        """
                    ),
                    {"exercise_id": exercise.id},
                )
            ).all()
            created_exercise_agonist_ids: list[UUID] = [value[0] for value in received_agonist_ids]

        assert created_exercise is not None
        assert created_exercise.id == exercise.id
        assert created_exercise.name == exercise.name
        assert created_exercise_agonist_ids == [exercise.agonist_ids[1], exercise.agonist_ids[0]]

    async def test_create_with_non_existent_agonist(
        self,
        session_factory,
    ):
        # Create workout with non added in repository agonist
        exercise = Exercise("Bench press")
        non_existent_agonist = Agonist("Pectoralis major")
        exercise.add_agonist(non_existent_agonist.id)

        async with session_factory() as seeder:
            repo = SQLAlchemyExerciseRepository(seeder)
            with pytest.raises(IncorrectAgonistIdError):
                await repo.create(exercise)

        async with session_factory() as reader:
            repo = SQLAlchemyExerciseRepository(reader)
            received_exercise = await repo.get_by_id(exercise.id)

        assert received_exercise is None

    async def test_get_by_id_with_existent_exercise(
        self,
        exercise_with_agonists,
        session_factory,
    ):
        exercise = exercise_with_agonists

        async with session_factory() as reader:
            repo = SQLAlchemyExerciseRepository(reader)
            received_exercise = await repo.get_by_id(exercise.id)

        assert received_exercise is not None
        assert received_exercise.id == exercise.id
        assert received_exercise.name == exercise.name
        assert received_exercise.agonist_ids == [exercise.agonist_ids[1], exercise.agonist_ids[0]]

    @pytest.mark.usefixtures("exercise_with_agonists")
    async def test_get_by_non_existent_id_with_filled_database(
        self,
        session_factory,
    ):
        non_added_exercise = Exercise("Squat")

        async with session_factory() as reader:
            repo = SQLAlchemyExerciseRepository(reader)
            received_exercise = await repo.get_by_id(non_added_exercise.id)

        assert received_exercise is None

    async def test_get_by_non_existent_id_with_empty_database(
        self,
        session_factory,
    ):
        non_added_exercise = Exercise("Squat")

        async with session_factory() as reader:
            repo = SQLAlchemyExerciseRepository(reader)
            received_exercise = await repo.get_by_id(non_added_exercise.id)

        assert received_exercise is None

    async def test_update(
        self,
        exercise_with_agonists,
        session_factory,
    ):
        exercise = exercise_with_agonists

        # Add new agonist in database
        agonist = Agonist("Quadriceps Femoris")
        async with session_factory() as seeder:
            await seeder.execute(
                text(
                    """
                    INSERT INTO agonists (id, name)
                    VALUES (:id, :name)
                    """
                ),
                {"id": agonist.id, "name": agonist.name},
            )
            await seeder.commit()

        # Changing exercise with adding and removing agonists
        exercise.name = "Squat"
        exercise.remove_agonist(exercise.agonist_ids[0])
        exercise.add_agonist(agonist.id)

        async with session_factory() as seeder:
            repo = SQLAlchemyExerciseRepository(seeder)
            await repo.update(exercise)
            await seeder.commit()

        async with session_factory() as reader:
            repo = SQLAlchemyExerciseRepository(reader)
            updated_exercise = await repo.get_by_id(exercise.id)

        assert updated_exercise is not None
        assert updated_exercise.id == exercise.id
        assert updated_exercise.name == exercise.name
        assert updated_exercise.agonist_ids == [exercise.agonist_ids[0], exercise.agonist_ids[1]]

    async def test_update_with_non_existent_exercise(
        self,
        session_factory,
    ):
        non_added_exercise = Exercise("Squat")

        async with session_factory() as seeder:
            repo = SQLAlchemyExerciseRepository(seeder)
            with pytest.raises(IncorrectExerciseIdError):
                await repo.update(non_added_exercise)

    async def test_update_with_non_existent_agonist(
        self,
        exercise_with_agonists,
        session_factory,
    ):
        exercise = exercise_with_agonists

        non_added_agonist = Agonist("Quadriceps Femoris")
        exercise.add_agonist(non_added_agonist.id)

        async with session_factory() as seeder:
            repo = SQLAlchemyExerciseRepository(seeder)
            with pytest.raises(IncorrectAgonistIdError):
                await repo.update(exercise)

        async with session_factory() as reader:
            repo = SQLAlchemyExerciseRepository(reader)
            non_updated_exercise = await repo.get_by_id(exercise.id)

        assert non_updated_exercise is not None
        assert non_updated_exercise.agonist_ids == [exercise.agonist_ids[1], exercise.agonist_ids[0]]
