import statistics
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from uuid_extensions.uuid7 import uuid7

from domain.exceptions import IncorrectWorkoutTimesError
from domain.workout_set import WorkoutSet


@dataclass
class Workout:
    _id: str = field(repr=False, init=False, default_factory=lambda: str(uuid7()))

    planned_start_time: datetime | None = field(default=None)
    planned_end_time: datetime | None = field(default=None)

    actual_start_time: datetime | None = field(default=None)
    actual_end_time: datetime | None = field(default=None)

    _sets: list[WorkoutSet] = field(init=False, default_factory=list)

    def __setattr__(self, key: str, value: Any) -> None:
        match key:
            case "planned_start_time":
                if ((value is not None) and (self.planned_end_time is not None)) and (
                    value > self.planned_end_time
                ):
                    raise IncorrectWorkoutTimesError(
                        "'Planned start time' cannot be later than 'planned end time'"
                    )
                object.__setattr__(self, key, value)

            case "planned_end_time":
                if ((self.planned_start_time is not None) and (value is not None)) and (
                    self.planned_start_time > value
                ):
                    raise IncorrectWorkoutTimesError(
                        "'Planned start time' cannot be later than 'planned end time'"
                    )
                object.__setattr__(self, key, value)

            case "actual_start_time":
                if ((value is not None) and (self.actual_end_time is not None)) and (
                    value > self.actual_end_time
                ):
                    raise IncorrectWorkoutTimesError(
                        "'Actual start time' cannot be later than 'actual end time'"
                    )
                object.__setattr__(self, key, value)

            case "actual_end_time":
                if ((self.actual_start_time is not None) and (value is not None)) and (
                    self.actual_start_time > value
                ):
                    raise IncorrectWorkoutTimesError(
                        "'Actual workout start time' cannot be later than 'actual workout end time'"
                    )
                object.__setattr__(self, key, value)

            case _:
                object.__setattr__(self, key, value)

    @property
    def id(self) -> str:
        return self._id

    @property
    def sets(self) -> list[WorkoutSet]:
        return self._sets

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

    def set_order_sets(self) -> None:
        """Set the value of order to each WorkoutSet of workout"""
        for index, workout_set in enumerate(self.sets):
            workout_set.order = index + 1

    def add_set(self, workout_set: WorkoutSet) -> None:
        """Adds a WorkoutSet to the workout with automatic indication of its order"""
        if isinstance(workout_set, WorkoutSet):
            workout_set.workout_id = self.id

            if workout_set.order is None:
                workout_set.order = len(self.sets) + 1

            self._sets.append(workout_set)
