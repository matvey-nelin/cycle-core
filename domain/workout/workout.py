import statistics
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID

from uuid6 import uuid7

from domain.exceptions import IncorrectWorkoutSetIdError, IncorrectWorkoutTimesError


@dataclass
class WorkoutSet:
    _id: UUID = field(repr=False, init=False, default_factory=uuid7)
    workout_id: UUID
    exercise_id: UUID

    order: int
    planned_reps: int = field(default=0)
    planned_weight: float = field(default=0)
    actual_reps: int = field(default=0)
    actual_weight: float = field(default=0)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def planned_tonnage(self) -> float:
        if self.planned_weight < 1:
            return self.planned_reps
        return round(self.planned_reps * self.planned_weight, 2)

    @property
    def actual_tonnage(self) -> float:
        if self.actual_weight < 1:
            return self.actual_reps
        return round(self.actual_reps * self.actual_weight, 2)

    @property
    def completion_percentage(self) -> float:
        if self.planned_tonnage == 0:
            return 0
        return round((self.actual_tonnage / self.planned_tonnage) * 100, 2)

    def __repr__(self) -> str:
        return f"{__class__.__name__}({self.id=}, {self.workout_id=}, {self.exercise_id=})"

    def __setattr__(self, key: str, value: Any) -> None:
        match key:
            case "planned_reps":
                if value < 0:
                    raise ValueError("The value of reps cannot be negative")
                object.__setattr__(self, key, int(value))

            case "actual_reps":
                if value < 0:
                    raise ValueError("The value of reps cannot be negative")
                object.__setattr__(self, key, int(value))

            case "planned_weight":
                if value < 0:
                    raise ValueError("The value of weight cannot be negative")
                object.__setattr__(self, key, float(value))

            case "actual_weight":
                if value < 0:
                    raise ValueError("The value of weight cannot be negative")
                object.__setattr__(self, key, float(value))

            case "order":
                if value <= 0:
                    raise ValueError("The value of order cannot be negative or zero")
                object.__setattr__(self, key, int(value))

            case _:
                object.__setattr__(self, key, value)

    # Alternative path to create object of WorkoutSet (for mappers)
    @classmethod
    def reconstruct(
        cls,
        id: UUID,
        workout_id: UUID,
        exercise_id: UUID,
        order: int,
        planned_reps: int,
        planned_weight: float,
        actual_reps: int,
        actual_weight: float,
    ) -> "WorkoutSet":
        instance = cls.__new__(cls)
        instance._id = id
        instance.workout_id = workout_id
        instance.exercise_id = exercise_id
        instance.order = order
        instance.planned_reps = planned_reps
        instance.planned_weight = planned_weight
        instance.actual_reps = actual_reps
        instance.actual_weight = actual_weight
        return instance


@dataclass
class Workout:
    _id: UUID = field(repr=False, init=False, default_factory=uuid7)  # without 'as_type' always returns UUID

    planned_start_time: datetime | None = field(default=None)
    planned_end_time: datetime | None = field(default=None)
    actual_start_time: datetime | None = field(default=None)
    actual_end_time: datetime | None = field(default=None)

    _sets: list[WorkoutSet] = field(init=False, default_factory=list)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def sets(self) -> list[WorkoutSet]:
        return [*self._sets]

    @property
    def planned_tonnage(self) -> float:
        if not self.sets:
            return float(0)
        return round(sum(set.planned_tonnage for set in self.sets), 2)

    @property
    def actual_tonnage(self) -> float:
        if not self.sets:
            return float(0)
        return round(sum(set.actual_tonnage for set in self.sets), 2)

    @property
    def completion_percentage(self) -> float:
        if not self.sets:
            return float(0)
        return round(statistics.mean(set.completion_percentage for set in self.sets), 2)

    def __repr__(self) -> str:
        return f"{__class__.__name__}({self.id=})"

    def __setattr__(self, key: str, value: Any) -> None:
        match key:
            case "planned_start_time":
                if (
                    (value is not None)
                    and (getattr(self, "planned_end_time", None) is not None)
                    and (getattr(self, "planned_end_time") < value)
                ):
                    raise IncorrectWorkoutTimesError("'Planned start time' cannot be later than 'planned end time'")
                object.__setattr__(self, key, value)

            case "planned_end_time":
                if (
                    (value is not None)
                    and (getattr(self, "planned_start_time", None) is not None)
                    and (getattr(self, "planned_start_time") > value)
                ):
                    raise IncorrectWorkoutTimesError("'Planned start time' cannot be later than 'planned end time'")
                object.__setattr__(self, key, value)

            case "actual_start_time":
                if (
                    (value is not None)
                    and (getattr(self, "actual_end_time", None) is not None)
                    and (getattr(self, "actual_end_time") < value)
                ):
                    raise IncorrectWorkoutTimesError("'Actual start time' cannot be later than 'actual end time'")
                object.__setattr__(self, key, value)

            case "actual_end_time":
                if (
                    (value is not None)
                    and (getattr(self, "actual_start_time", None) is not None)
                    and (getattr(self, "actual_start_time") > value)
                ):
                    raise IncorrectWorkoutTimesError(
                        "'Actual workout start time' cannot be later than 'actual workout end time'"
                    )
                object.__setattr__(self, key, value)

            case _:
                object.__setattr__(self, key, value)

    def add_set(
        self,
        exercise_id: UUID,
        planned_reps: int = 0,
        planned_weight: float = 0,
        actual_reps: int = 0,
        actual_weight: float = 0,
    ) -> None:
        """
        Adds a WorkoutSet to the workout with automatic indication of it's order and workout_id
        """
        self._sets.append(
            WorkoutSet(
                workout_id=self.id,
                exercise_id=exercise_id,
                order=len(self.sets) + 1,
                planned_reps=planned_reps,
                planned_weight=planned_weight,
                actual_reps=actual_reps,
                actual_weight=actual_weight,
            )
        )

    def remove_set(self, set_id: UUID) -> None:
        for wset in self.sets:
            if wset.id == set_id:
                self._sets.remove(wset)
                break
        else:
            raise IncorrectWorkoutSetIdError()

        for i in range(len(self.sets)):
            self._sets[i].order = i + 1

    @classmethod
    def reconstruct(
        cls,
        id: UUID,
        planned_start_time: datetime | None,
        planned_end_time: datetime | None,
        actual_start_time: datetime | None,
        actual_end_time: datetime | None,
        sets: list[WorkoutSet],
    ) -> "Workout":
        """Alternative path to create object of Workout (for mappers)"""
        instance = cls.__new__(cls)
        instance._id = id
        instance.planned_start_time = planned_start_time
        instance.planned_end_time = planned_end_time
        instance.actual_start_time = actual_start_time
        instance.actual_end_time = actual_end_time
        instance._sets = [*sets]
        return instance
