"""Tests for the TasktRepository class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from base.components.domain import EntityId
from core.domain.task import Task
from core.infrastructure.task import TaskRepository

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import Table


class TestTaskRepository:
    """Tests for the TaskRepository class."""

    def test_get_by_project_id(self, table: Table) -> None:
        """Test the get method."""
        table.put_item(
            Item={
                "project_id": "01DXF6DT000000000000000000",
                "item_name": "Task#01DXHRTH000000000000000000",
                "title": "Test Project",
                "description": "Test Description",
            }
        )

        repository = TaskRepository(table)
        actual = repository.get_by_project_id(EntityId(value="01DXF6DT000000000000000000"))

        expected = [
            Task(
                id=EntityId(value="01DXHRTH000000000000000000"),
                project_id=EntityId(value="01DXF6DT000000000000000000"),
                title="Test Project",
                description="Test Description",
            )
        ]

        assert actual == expected

    def test_save(self, table: Table) -> None:
        """Test the save method."""
        task = Task(
            id=EntityId(value="01DXHRTH000000000000000000"),
            project_id=EntityId(value="01DXF6DT000000000000000000"),
            title="Test Project",
            description="Test Description",
        )

        repository = TaskRepository(table)
        repository.save(task)

        actual = table.get_item(
            Key={"project_id": "01DXF6DT000000000000000000", "item_name": "Task#01DXHRTH000000000000000000"}
        )["Item"]
        expected = {
            "project_id": "01DXF6DT000000000000000000",
            "item_name": "Task#01DXHRTH000000000000000000",
            "title": "Test Project",
            "description": "Test Description",
        }

        assert actual == expected
