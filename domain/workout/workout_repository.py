from abc import ABC, abstractmethod
from uuid import UUID

from domain.workout.workout import Workout


class AbstractWorkoutRepository(ABC):
    def __init__(self) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Workout | None:
        """Returns Workout domain object by passed id"""

    @abstractmethod
    async def create(self, workout: Workout) -> None:
        """Adds a new workout in repository"""

    @abstractmethod
    async def update(self, workout: Workout) -> Workout:
        """Save changes in existent Workout"""
        ...
