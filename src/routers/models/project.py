"""Project model."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from pydantic import BaseModel

if TYPE_CHECKING:
    from core.application.project import ProjectDTO
    from core.application.task import TaskDTO


class NewProjectRequest(BaseModel):
    """Request model for creating a new project."""

    title: str


class ProjectResponseTask(BaseModel):
    """Response model for a task in a project."""

    id: str
    title: str
    description: str

    @classmethod
    def from_dto(cls, dto: TaskDTO) -> Self:
        """Converts a DTO to a response model."""
        return cls(id=dto.id, title=dto.title, description=dto.description)


class ProjectResponse(BaseModel):
    """Response model for a post."""

    id: str
    title: str
    tasks: list[ProjectResponseTask]

    @classmethod
    def from_dto(cls, dto: ProjectDTO) -> Self:
        """Converts a DTO to a response model."""
        tasks = [ProjectResponseTask.from_dto(task) for task in dto.tasks]
        return cls(id=dto.id, title=dto.title, tasks=tasks)
