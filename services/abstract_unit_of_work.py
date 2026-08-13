import abc

from domain.workout.workout_repository import AbstractWorkoutRepository


class AbstractUnitOfWork(abc.ABC):
    workouts: AbstractWorkoutRepository

    def __init__(self) -> None: ...

    async def __aenter__(self) -> "AbstractUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            await self.rollback()

    @abc.abstractmethod
    async def commit(self) -> None: ...

    @abc.abstractmethod
    async def rollback(self) -> None: ...
