from uuid import UUID

from domain.agonist.agonist import Agonist
from services.abstract_unit_of_work import AbstractUnitOfWork
from services.exceptions import AgonistNotFoundError


class AgonistService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def get_agonist(self, agonist_id: UUID) -> Agonist:
        async with self.uow:
            return await self._get_agonist_or_raise(agonist_id)

    async def create_agonist(self, name: str) -> UUID:
        agonist = Agonist(name)
        async with self.uow:
            await self.uow.agonists.create(agonist)
            await self.uow.commit()
        return agonist.id

    async def update_agonist(self, agonist_id: UUID, name: str | None = None) -> None:
        async with self.uow:
            agonist = await self._get_agonist_or_raise(agonist_id)
            if name is not None:
                agonist.name = name
            await self.uow.agonists.update(agonist)
            await self.uow.commit()

    async def _get_agonist_or_raise(self, agonist_id: UUID) -> Agonist:
        """Method-helper without context"""
        agonist = await self.uow.agonists.get_by_id(agonist_id)
        if agonist is None:
            raise AgonistNotFoundError()
        return agonist
