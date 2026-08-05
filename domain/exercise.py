from dataclasses import dataclass, field
from typing import Any

from uuid_extensions import uuid7


@dataclass
class Exercise:
    _id: str = field(repr=False, init=False, default_factory=lambda: str(uuid7()))
    name: str

    agonist_ids: list[str] | None = field(default_factory=list)

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
                if not isinstance(value, list) or not all(
                    isinstance(item, str) for item in value
                ):
                    raise ValueError("'agonist_ids' must be list of the integer values")

                object.__setattr__(self, key, value)

            case _:
                object.__setattr__(self, key, value)

    @property
    def id(self) -> str:
        return self._id
