"""Task model."""

from __future__ import annotations

from pydantic import Field

from base.components.domain import Entity, EntityId


class Task(Entity):
    """Task Entity.

    Attributes:
        id: Task ID.
        project_id: Project ID that the task belongs to.
        title: Task title.
        description: Task description.
    """

    id: EntityId = Field(default_factory=EntityId)
    project_id: EntityId
    title: str
    description: str
