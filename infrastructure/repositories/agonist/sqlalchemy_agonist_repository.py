from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.agonist.agonist import Agonist
from domain.agonist.agonist_repository import AbstractAgonistRepository
from infrastructure.mappers.agonist_mapper import AgonistMapper
from infrastructure.models.agonist import AgonistORM
from infrastructure.repositories.exceptions import IncorrectAgonistIdError


class SQLAlchemyAgonistRepository(AbstractAgonistRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: UUID) -> Agonist | None:
        agonist_orm = await self._fetch_orm(id)
        if agonist_orm is None:
            return None
        return AgonistMapper.to_domain(agonist_orm)

    async def create(self, agonist: Agonist) -> None:
        agonist_orm = AgonistMapper.to_orm(agonist)
        self.session.add(agonist_orm)

    async def update(self, agonist: Agonist) -> Agonist:
        agonist_orm = await self._fetch_orm(agonist.id)
        if agonist_orm is None:
            raise IncorrectAgonistIdError("Agonist must be added in repository before saving changes")

        agonist_orm.name = agonist.name

        return AgonistMapper.to_domain(agonist_orm)

    async def _fetch_orm(self, agonist_id: UUID) -> AgonistORM | None:
        query = select(AgonistORM).where(AgonistORM.id == agonist_id)
        return (await self.session.scalars(query)).one_or_none()
