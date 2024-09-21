"""Repository interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from base.components.domain import EntityId, Repository

if TYPE_CHECKING:
    from .project import Project
    from .task import Task


class ProjectRepository(Repository, ABC):
    """Project repository interface."""

    @abstractmethod
    def get(self, project_id: EntityId) -> Project:
        """Get a project."""
        raise NotImplementedError

    @abstractmethod
    def save(self, project: Project) -> None:
        """Save a project."""
        raise NotImplementedError


class TaskRepository(Repository, ABC):
    """Task repository interface."""

    @abstractmethod
    def get_by_project_id(self, project_id: EntityId) -> list[Task]:
        """Get tasks by project ID."""
        raise NotImplementedError

    @abstractmethod
    def save(self, task: Task) -> None:
        """Save a task."""
        raise NotImplementedError
