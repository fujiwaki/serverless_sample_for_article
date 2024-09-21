"""Tests for the Project domain object."""

from __future__ import annotations

from typing import TYPE_CHECKING

from base.components.domain import EntityId
from core.application.project import CreateProjectCommand, GetProjectCommand, ProjectDTO, ProjectService
from core.application.task import TaskDTO
from core.domain.project import Project
from core.domain.task import Task

if TYPE_CHECKING:
    from tests.unit.core.conftest import InMemoryProjectRepository, InMemoryTaskRepository


def put_test_data(project_repository: InMemoryProjectRepository, task_repository: InMemoryTaskRepository) -> None:
    """Put test data to repositories."""
    project_id = EntityId(value="01DXF6DT000000000000000000")
    project_repository._projects = {project_id: Project(id=project_id, title="Test Project")}
    task_repository._tasks = {
        project_id: [
            Task(
                id=EntityId(value="01DXHRTH000000000000000000"),
                project_id=project_id,
                title="Test Task 1",
                description="Test Description 1",
            ),
            Task(
                id=EntityId(value="01DXMB78000000000000000000"),
                project_id=project_id,
                title="Test Task 2",
                description="Test Description 2",
            ),
        ]
    }


class TestProjectService:
    """Project Service tests."""

    def test_get_project(
        self, project_repository: InMemoryProjectRepository, task_repository: InMemoryTaskRepository
    ) -> None:
        """Test getting a project."""
        put_test_data(project_repository, task_repository)

        service = ProjectService(project_repository, task_repository)
        command = GetProjectCommand(id="01DXF6DT000000000000000000")
        actual = service.get(command)

        expected = ProjectDTO(
            id="01DXF6DT000000000000000000",
            title="Test Project",
            tasks=[
                TaskDTO(
                    id="01DXHRTH000000000000000000",
                    project_id="01DXF6DT000000000000000000",
                    title="Test Task 1",
                    description="Test Description 1",
                ),
                TaskDTO(
                    id="01DXMB78000000000000000000",
                    project_id="01DXF6DT000000000000000000",
                    title="Test Task 2",
                    description="Test Description 2",
                ),
            ],
        )

        assert actual == expected

    def test_create_project(
        self, project_repository: InMemoryProjectRepository, task_repository: InMemoryTaskRepository
    ) -> None:
        """Test creating a new project."""
        service = ProjectService(project_repository, task_repository)
        command = CreateProjectCommand(title="Test Project")
        project = service.create(command)

        assert project.id
        assert project.title == "Test Project"
