from abc import ABC, abstractmethod
from uuid import UUID

from domain.agonist.agonist import Agonist


class AbstractAgonistRepository(ABC):
    def __init__(self) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Agonist | None:
        """Returns Agonist domain object by passed id"""

    @abstractmethod
    async def create(self, agonist: Agonist) -> None:
        """Adds a new agonist in repository"""

    @abstractmethod
    async def update(self, agonist: Agonist) -> Agonist:
        """Save changes in existent Agonist"""
        ...
