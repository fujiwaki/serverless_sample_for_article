"""Tests for the Task domain object."""

from __future__ import annotations

from base.components.domain import EntityId
from core.domain.task import Task


class TestTask:
    """Task tests."""

    def test_new_task(self) -> None:
        """Test creating a new task."""
        task = Task(
            project_id=EntityId(value="01DXF6DT000000000000000000"), title="Test Task", description="Test Description"
        )

        assert task.id
        assert task.project_id == EntityId(value="01DXF6DT000000000000000000")
        assert task.title == "Test Task"
        assert task.description == "Test Description"

    def test_reconstruct_task(self) -> None:
        """Test reconstructing a task."""
        task = Task(
            id=EntityId(value="01DXHRTH000000000000000000"),
            project_id=EntityId(value="01DXF6DT000000000000000000"),
            title="Test Task",
            description="Test Description",
        )

        assert task.id == EntityId(value="01DXHRTH000000000000000000")
        assert task.project_id == EntityId(value="01DXF6DT000000000000000000")
        assert task.title == "Test Task"
        assert task.description == "Test Description"
