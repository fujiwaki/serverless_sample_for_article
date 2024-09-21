"""Tests for the Project domain object."""

from __future__ import annotations

from typing import TYPE_CHECKING

from core.application.task import CreateTaskCommand, TaskService

if TYPE_CHECKING:
    from tests.unit.core.conftest import InMemoryTaskRepository


class TestTaskService:
    """Task Service tests."""

    def test_create_task(self, task_repository: InMemoryTaskRepository) -> None:
        """Test creating a new task."""
        service = TaskService(task_repository)
        command = CreateTaskCommand(
            project_id="01DXF6DT000000000000000000", title="Test Task", description="Test Description"
        )
        task = service.create(command)

        assert task.id
        assert task.project_id == "01DXF6DT000000000000000000"
        assert task.title == "Test Task"
        assert task.description == "Test Description"
