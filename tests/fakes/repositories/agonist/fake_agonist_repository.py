from uuid import UUID

from domain.agonist.agonist import Agonist
from domain.agonist.agonist_repository import AbstractAgonistRepository
from infrastructure.repositories.exceptions import IncorrectAgonistIdError


class FakeAgonistRepository(AbstractAgonistRepository):
    def __init__(self, agonists: dict[UUID, Agonist] | None = None) -> None:
        self._agonists = {**agonists} if agonists else {}
        self._buffer = {}

    async def get_by_id(self, id: UUID) -> Agonist | None:
        agonist = self._buffer.get(id)
        if agonist is None:
            agonist = self._agonists.get(id)
        return agonist

    async def create(self, agonist: Agonist) -> None:
        self._buffer[agonist.id] = agonist

    async def update(self, agonist: Agonist) -> Agonist:
        if self._buffer.get(agonist.id) or self._agonists.get(agonist.id):
            self._buffer[agonist.id] = agonist
            return agonist
        else:
            raise IncorrectAgonistIdError("Agonist must be added in repository before saving changes")

    def _save_current_transaction(self):
        self._agonists.update(self._buffer)
        self._buffer.clear()

    def _clear_buffer(self):
        self._buffer.clear()
