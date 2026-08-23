import pytest

from domain.agonist.agonist import Agonist
from domain.exceptions import IncorrectAgonistNameError
from services.abstract_unit_of_work import AbstractUnitOfWork
from services.agonist_service import AgonistService
from services.exceptions import AgonistNotFoundError


@pytest.fixture
def service(double_uow):
    uow: AbstractUnitOfWork = double_uow
    return AgonistService(uow)


class TestAgonistService:
    async def test_create_agonist(
        self,
        double_uow,
    ):
        uow: AbstractUnitOfWork = double_uow
        service = AgonistService(uow)

        agonist_id = await service.create_agonist("Pectoralis major")
        async with uow:
            agonist = await uow.agonists.get_by_id(agonist_id)

        assert agonist is not None
        assert agonist.name == "Pectoralis major"

    async def test_create_agonist_with_incorrect_agonist_name_error(
        self,
        service,
    ):
        with pytest.raises(IncorrectAgonistNameError):
            await service.create_agonist("")

    async def test_get_agonist(
        self,
        service,
    ):
        agonist_id = await service.create_agonist("Pectoralis major")
        agonist = await service.get_agonist(agonist_id)

        assert agonist.id == agonist_id
        assert agonist.name == "Pectoralis major"

    async def test_get_agonist_with_agonist_not_found_error(
        self,
        service,
    ):
        agonist = Agonist("Pectoralis major")

        with pytest.raises(AgonistNotFoundError):
            await service.get_agonist(agonist.id)

    async def test_update_agonist(
        self,
        service,
    ):
        agonist_id = await service.create_agonist("Pectoralis major")
        await service.update_agonist(agonist_id, "Pectoralis minor")

        agonist = await service.get_agonist(agonist_id)

        assert agonist.id == agonist_id
        assert agonist.name == "Pectoralis minor"

    async def test_update_agonist_with_agonist_not_found_error(
        self,
        service,
    ):
        agonist = Agonist("Pectoralis major")

        with pytest.raises(AgonistNotFoundError):
            await service.update_agonist(agonist.id)

    async def test_update_agonist_with_incorrect_agonist_name_error(
        self,
        service,
    ):
        agonist_id = await service.create_agonist("Pectoralis major")

        with pytest.raises(IncorrectAgonistNameError):
            await service.update_agonist(agonist_id, "")
