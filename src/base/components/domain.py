"""Components for domain layer."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.ulid import ULID as PDULID  # noqa: TCH002
from ulid import ULID


class ValueObject(BaseModel):
    """Base class for value objects."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class EntityId(BaseModel):
    """Entity ID class."""

    value: PDULID = Field(default_factory=ULID)  # type: ignore[assignment]

    def __str__(self) -> str:
        """Return the string representation."""
        return str(self.value)

    def __hash__(self) -> int:
        """Return the hash value."""
        return hash(self.__str__())


class Entity(BaseModel):
    """Base class for entities."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class Repository:
    """Base class for repositories."""
