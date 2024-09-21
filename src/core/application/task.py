"""Task application service."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from base.components.application import DTO, Command, Service
from base.components.domain import EntityId
from core.domain.task import Task

if TYPE_CHECKING:
    from core.domain.repositories import TaskRepository


class TaskDTO(DTO):
    """Task DTO.

    Attributes:
        id: Task ID.
        project_id: Project ID that the task belongs to.
        title: Task title.
        description: Task description.
    """

    id: str
    project_id: str
    title: str
    description: str

    @classmethod
    def from_entity(cls, entity: Task) -> Self:
        """Create a DTO from an entity.

        Args:
            entity: Task entity.
        """
        return cls(
            id=str(entity.id), project_id=str(entity.project_id), title=entity.title, description=entity.description
        )


class CreateTaskCommand(Command):
    """Create task command.

    Attributes:
        project_id: Project ID that the task belongs to.
        title: Task title.
        description: Task description.
    """

    project_id: str
    title: str
    description: str


class TaskService(Service):
    """Task service."""

    def __init__(self, task_repository: TaskRepository) -> None:
        """Constructor.

        Args:
            task_repository: Task repository
        """
        self._task_repository = task_repository

    def create(self, command: CreateTaskCommand) -> TaskDTO:
        """Create a project.

        Args:
            command: Create task command.
        """
        task = Task(project_id=EntityId(value=command.project_id), title=command.title, description=command.description)
        self._task_repository.save(task)
        return TaskDTO.from_entity(task)
