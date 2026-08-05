from dataclasses import dataclass, field
from typing import Any

from uuid_extensions import uuid7


@dataclass
class Agonist:
    _id: str = field(repr=False, init=False, default_factory=lambda: str(uuid7()))
    name: str

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
    def id(self) -> str:
        return self._id
