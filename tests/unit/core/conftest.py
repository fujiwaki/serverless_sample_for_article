"""Conftest for the core module."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from core.domain.repositories import ProjectRepository, TaskRepository

if TYPE_CHECKING:
    from base.components.domain import EntityId
    from core.domain.project import Project
    from core.domain.task import Task


class InMemoryProjectRepository(ProjectRepository):
    """In-memory implementation of the ProjectRepository interface."""

    def __init__(self) -> None:
        """Initialize the repository."""
        self._projects: dict[EntityId, Project] = {}

    def get(self, project_id: EntityId) -> Project:
        """Get a project by its ID.

        Args:
            project_id: The ID of the project to get.
        """
        return self._projects[project_id]

    def save(self, project: Project) -> None:
        """Save a project.

        Args:
            project: The project to save.
        """
        self._projects[project.id] = project


@pytest.fixture
def project_repository() -> InMemoryProjectRepository:
    """Fixture for an in-memory project repository."""
    return InMemoryProjectRepository()


class InMemoryTaskRepository(TaskRepository):
    """In-memory implementation of the ProjectRepository interface."""

    def __init__(self) -> None:
        """Initialize the repository."""
        self._tasks: dict[EntityId, list[Task]] = {}

    def get_by_project_id(self, project_id: EntityId) -> list[Task]:
        """Get a project by its ID.

        Args:
            project_id: The project_id to get.
        """
        return self._tasks[project_id]

    def save(self, task: Task) -> None:
        """Save a project.

        Args:
            task: The task to save.
        """
        if self._tasks.get(task.project_id):
            self._tasks[task.project_id].append(task)
        else:
            self._tasks[task.project_id] = [task]


@pytest.fixture
def task_repository() -> InMemoryTaskRepository:
    """Fixture for an in-memory task repository."""
    return InMemoryTaskRepository()
