import pytest
from sqlalchemy import text

from domain.agonist.agonist import Agonist
from infrastructure.repositories.agonist.sqlalchemy_agonist_repository import SQLAlchemyAgonistRepository
from infrastructure.repositories.exceptions import IncorrectAgonistIdError


class TestAgonistRepository:
    async def test_create(
        self,
        session_factory,
    ):
        agonist = Agonist("Pectoralis major")

        async with session_factory() as seeder:
            repo = SQLAlchemyAgonistRepository(seeder)
            await repo.create(agonist)
            await seeder.commit()

        async with session_factory() as seeder:
            created_agonist: Agonist = (
                await seeder.execute(text("SELECT id, name FROM agonists WHERE id = :id"), {"id": agonist.id})
            ).one()

        assert created_agonist is not None
        assert created_agonist.id == agonist.id
        assert created_agonist.name == agonist.name

    async def test_get_by_id_with_existent_agonist(
        self,
        session_factory,
    ):
        agonist = Agonist("Pectoralis major")
        async with session_factory() as seeder:
            repo = SQLAlchemyAgonistRepository(seeder)
            await repo.create(agonist)
            await seeder.commit()

        async with session_factory() as reader:
            repo = SQLAlchemyAgonistRepository(reader)
            received_agonist = await repo.get_by_id(agonist.id)

        assert received_agonist is not None
        assert received_agonist.id == agonist.id
        assert received_agonist.name == agonist.name

    async def test_get_by_non_existent_id_with_filled_database(
        self,
        session_factory,
    ):
        added_agonist = Agonist("Pectoralis major")
        non_added_agonist = Agonist("Pectoralis minor")

        async with session_factory() as seeder:
            repo = SQLAlchemyAgonistRepository(seeder)
            await repo.create(added_agonist)
            await seeder.commit()

        async with session_factory() as reader:
            repo = SQLAlchemyAgonistRepository(reader)
            received_agonist = await repo.get_by_id(non_added_agonist.id)

        assert received_agonist is None

    async def test_get_by_non_existent_id_with_empty_database(
        self,
        session_factory,
    ):
        non_added_agonist = Agonist("Pectoralis minor")

        async with session_factory() as reader:
            repo = SQLAlchemyAgonistRepository(reader)
            received_agonist = await repo.get_by_id(non_added_agonist.id)

        assert received_agonist is None

    async def test_update(
        self,
        session_factory,
    ):
        agonist = Agonist("Pectoralis major")

        async with session_factory() as seeder:
            repo = SQLAlchemyAgonistRepository(seeder)
            await repo.create(agonist)
            await seeder.commit()

        agonist.name = "Pectoralis minor"

        async with session_factory() as seeder:
            repo = SQLAlchemyAgonistRepository(seeder)
            await repo.update(agonist)
            await seeder.commit()

        async with session_factory() as reader:
            repo = SQLAlchemyAgonistRepository(reader)
            updated_agonist = await repo.get_by_id(agonist.id)

        assert isinstance(updated_agonist, Agonist)
        assert updated_agonist.id == agonist.id
        assert updated_agonist.name == agonist.name

    async def test_update_non_existent_agonist(
        self,
        session_factory,
    ):
        agonist = Agonist("Pectoralis major")
        agonist.name = "Pectoralis minor"

        async with session_factory() as seeder:
            repo = SQLAlchemyAgonistRepository(seeder)
            with pytest.raises(IncorrectAgonistIdError):
                await repo.update(agonist)
