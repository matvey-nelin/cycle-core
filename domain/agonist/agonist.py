from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from uuid6 import uuid7


@dataclass
class Agonist:
    _id: UUID = field(repr=False, init=False, default_factory=uuid7)  # without 'as_type' always returns UUID
    name: str

    def __repr__(self) -> str:
        return f"{__class__.__name__}({self.id=}, {self.name=})"

    def __setattr__(self, key: str, value: Any) -> None:
        match key:
            case "name":
                if not isinstance(value, str) or not value.strip():
                    raise ValueError("Agonist name must be non-empty string value")

                cleaned_value = value.strip()

                if len(cleaned_value) > 100:
                    raise ValueError("Agonist name length exceeding 100 characters.")

                object.__setattr__(self, key, cleaned_value)

            case _:
                object.__setattr__(self, key, value)

    @property
    def id(self) -> UUID:
        return self._id
