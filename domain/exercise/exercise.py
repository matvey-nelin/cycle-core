from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from uuid6 import uuid7


@dataclass
class Exercise:
    _id: UUID = field(repr=False, init=False, default_factory=uuid7)  # without 'as_type' always returns UUID
    name: str

    agonist_ids: list[UUID] | None = field(default_factory=list)

    def __repr__(self) -> str:
        return f"{__class__.__name__}({self.id=}, {self.name=})"

    def __setattr__(self, key: str, value: Any) -> None:
        match key:
            case "name":
                if not isinstance(value, str) or not value.strip():
                    raise ValueError("Exercise name must be non-empty string value")

                cleaned_value = value.strip()

                if len(cleaned_value) > 100:
                    raise ValueError("Exercise name length exceeding 100 characters.")

                object.__setattr__(self, key, cleaned_value)

            case "agonist_ids":
                if not isinstance(value, list) or not all(isinstance(item, UUID) for item in value):
                    raise ValueError("'agonist_ids' must be list of the UUID values")

                object.__setattr__(self, key, value)

            case _:
                object.__setattr__(self, key, value)

    @property
    def id(self) -> UUID:
        return self._id
