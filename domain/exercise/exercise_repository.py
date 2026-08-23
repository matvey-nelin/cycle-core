from abc import ABC, abstractmethod
from uuid import UUID

from domain.exercise.exercise import Exercise


class AbstractExerciseRepository(ABC):
    def __init__(self) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Exercise | None:
        """Returns Exercise domain object by passed id"""

    @abstractmethod
    async def create(self, exercise: Exercise) -> None:
        """Adds a new exercise in repository"""

    @abstractmethod
    async def update(self, exercise: Exercise) -> Exercise:
        """Save changes in existent Exercise"""
        ...
