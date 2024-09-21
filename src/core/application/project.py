"""Project application service."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from base.components.application import DTO, Command, Service
from base.components.domain import EntityId
from core.domain.project import Project

from .task import TaskDTO

if TYPE_CHECKING:
    from core.domain.repositories import ProjectRepository, TaskRepository
    from core.domain.task import Task


class ProjectDTO(DTO):
    """Project DTO.

    Attributes:
        id: Project ID.
        title: Project title.
        tasks: Tasks of the project.
    """

    id: str
    title: str
    tasks: list[TaskDTO]

    @classmethod
    def from_entity(cls, project: Project, tasks: list[Task]) -> Self:
        """Create a DTO from an entity.

        Args:
            project: Project entity.
            tasks: Tasks of the project.
        """
        task_dtos = [TaskDTO.from_entity(task) for task in tasks]
        return cls(id=str(project.id), title=project.title, tasks=task_dtos)


class CreateProjectCommand(Command):
    """Create project command.

    Attributes:
        title: Project title.
    """

    title: str


class GetProjectCommand(Command):
    """Get project command.

    Attributes:
        id: Project ID.
    """

    id: str


class ProjectService(Service):
    """Project service."""

    def __init__(self, project_repository: ProjectRepository, task_repository: TaskRepository) -> None:
        """Constructor.

        Args:
            project_repository: Project repository.
            task_repository: Task repository.
        """
        self._project_repository = project_repository
        self._task_repository = task_repository

    def get(self, command: GetProjectCommand) -> ProjectDTO:
        """Get a project.

        Args:
            command: Command to get a project.
        """
        project = self._project_repository.get(EntityId(value=command.id))
        tasks = self._task_repository.get_by_project_id(EntityId(value=command.id))
        return ProjectDTO.from_entity(project, tasks)

    def create(self, command: CreateProjectCommand) -> ProjectDTO:
        """Create a project.

        Args:
            command: Command to create a project.
        """
        project = Project(title=command.title)
        self._project_repository.save(project)
        return ProjectDTO.from_entity(project, [])
