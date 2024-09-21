"""Task model."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from pydantic import BaseModel

if TYPE_CHECKING:
    from core.application.task import TaskDTO


class NewTaskRequest(BaseModel):
    """Request model for creating a new task."""

    title: str
    description: str


class TaskResponse(BaseModel):
    """Response model for a post."""

    id: str
    project_id: str
    title: str
    description: str

    @classmethod
    def from_dto(cls, dto: TaskDTO) -> Self:
        """Converts a DTO to a response model."""
        return cls(id=dto.id, project_id=dto.project_id, title=dto.title, description=dto.description)
