from uuid import UUID

from domain.exercise.exercise import Exercise
from infrastructure.repositories.exceptions import IncorrectAgonistIdError
from infrastructure.unit_of_work import AbstractUnitOfWork
from services.exceptions import AgonistNotFoundError, ExerciseNotFoundError


class ExerciseService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def get_exercise(self, exercise_id: UUID) -> Exercise:
        async with self.uow:
            return await self._get_exercise_or_raise(exercise_id)

    async def create_exercise(self, name: str) -> UUID:
        exercise = Exercise(name)
        async with self.uow:
            await self.uow.exercises.create(exercise)
            await self.uow.commit()
        return exercise.id

    async def update_exercise(self, exercise_id: UUID, name: str | None = None) -> None:
        async with self.uow:
            exercise = await self._get_exercise_or_raise(exercise_id)
            if name is not None:
                exercise.name = name
            await self.uow.exercises.update(exercise)
            await self.uow.commit()

    async def add_agonist(self, exercise_id: UUID, agonist_id: UUID) -> None:
        async with self.uow:
            exercise = await self._get_exercise_or_raise(exercise_id)
            exercise.add_agonist(agonist_id)
            try:
                await self.uow.exercises.update(exercise)
                await self.uow.commit()
            except IncorrectAgonistIdError as _ex:
                raise AgonistNotFoundError(_ex.message)

    async def remove_agonist(self, exercise_id: UUID, agonist_id: UUID) -> None:
        async with self.uow:
            exercise = await self._get_exercise_or_raise(exercise_id)
            exercise.remove_agonist(agonist_id)
            await self.uow.exercises.update(exercise)
            await self.uow.commit()

    async def _get_exercise_or_raise(self, exercise_id: UUID) -> Exercise:
        """Method-helper without context"""
        exercise = await self.uow.exercises.get_by_id(exercise_id)
        if exercise is None:
            raise ExerciseNotFoundError()
        return exercise
