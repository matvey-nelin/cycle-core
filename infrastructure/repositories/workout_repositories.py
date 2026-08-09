from abc import ABC, abstractmethod

from domain.workout import Workout


class AbstractWorkoutRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> Workout | None:
        pass

    @abstractmethod
    def get_all(self) -> list[Workout]:
        pass

    @abstractmethod
    def get_all_ids(self) -> list[str]:
        pass

    @abstractmethod
    def add(self, obj: Workout) -> None:
        pass


class InMemoryWorkoutRepository(AbstractWorkoutRepository):
    def __init__(self, workouts: dict[str, Workout] | None = None) -> None:
        self._workouts = {**workouts} if workouts else {}

    def get_by_id(self, id: str):
        return self._workouts.get(str(id), None)

    def get_all(self):
        return list(self._workouts.values())

    def get_all_ids(self):
        return list(self._workouts.keys())

    def add(self, workout: Workout):
        self._workouts[workout.id] = workout
