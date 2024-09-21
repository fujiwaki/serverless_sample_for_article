"""Components for application layer."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Command(BaseModel):
    """Base class for commands."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class DTO(BaseModel):
    """Base class for DTOs."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class Service:
    """Base class for services."""
