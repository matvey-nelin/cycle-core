from dataclasses import dataclass, field
from typing import Any

from uuid_extensions.uuid7 import uuid7


@dataclass
class WorkoutSet:
    _id: str = field(repr=False, init=False, default_factory=lambda: str(uuid7()))

    order: int | None = field(init=False, default=None)

    workout_id: str | None = field(init=False, default=None)
    exercise_id: str

    planned_reps: int = field(default=0)
    planned_weight: float = field(default=0)

    actual_reps: int = field(default=0)
    actual_weight: float = field(default=0)

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

    @property
    def id(self) -> str:
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
