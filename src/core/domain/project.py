"""Project model."""

from __future__ import annotations

from pydantic import Field

from base.components.domain import Entity, EntityId


class Project(Entity):
    """Project Entity.

    Attributes:
        id: Project ID.
        title: Project title.
    """

    id: EntityId = Field(default_factory=EntityId)
    title: str
