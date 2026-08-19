from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from uuid6 import uuid7

from domain.exceptions import IncorrectAgonistNameError


@dataclass
class Agonist:
    _id: UUID = field(repr=False, init=False, default_factory=uuid7)
    name: str

    @property
    def id(self) -> UUID:
        return self._id

    def __repr__(self) -> str:
        return f"{__class__.__name__}({self.id=}, {self.name=})"

    def __setattr__(self, key: str, value: Any) -> None:
        match key:
            case "name":
                if not isinstance(value, str) or not value.strip():
                    raise IncorrectAgonistNameError("Agonist name must be non-empty string value")

                cleaned_value = value.strip()

                if len(cleaned_value) > 100:
                    raise IncorrectAgonistNameError("Agonist name length exceeding 100 characters.")

                object.__setattr__(self, key, cleaned_value)

            case _:
                object.__setattr__(self, key, value)

    @classmethod
    def reconstract(
        cls,
        id: UUID,
        name: str,
    ) -> "Agonist":
        """Alternative path to create object of Agonist (for mappers)"""
        instance = cls.__new__(cls)
        instance._id = id
        instance.name = name
        return instance
