from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from uuid6 import uuid7

from domain.exceptions import DuplicateAgonistIdError, NonExistentAgonistIdError


@dataclass
class Exercise:
    _id: UUID = field(repr=False, init=False, default_factory=uuid7)
    name: str

    _agonist_ids: list[UUID] = field(init=False, default_factory=list)

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def agonist_ids(self) -> list[UUID]:
        return [*self._agonist_ids]

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

            case _:
                object.__setattr__(self, key, value)

    def add_agonist(self, agonist_id: UUID) -> None:
        if not isinstance(agonist_id, UUID):
            raise TypeError("Incorrect type of value 'agonist_id'")
        if agonist_id in self._agonist_ids:
            raise DuplicateAgonistIdError("This 'agonist_id' already added")
        self._agonist_ids.append(agonist_id)

    def remove_agonist(self, agonist_id: UUID) -> None:
        if not isinstance(agonist_id, UUID):
            raise TypeError("Incorrect type of value 'agonist_id'")
        if agonist_id not in self._agonist_ids:
            raise NonExistentAgonistIdError("This 'agonist_id' not added in exercise")
        self._agonist_ids.remove(agonist_id)

    @classmethod
    def reconstruct(
        cls,
        id: UUID,
        name: str,
        agonist_ids: list[UUID],
    ) -> "Exercise":
        """Alternative path to create object of Exercise (for mappers)"""
        instance = cls.__new__(cls)
        instance._id = id
        instance.name = name
        instance._agonist_ids = agonist_ids
        return instance
