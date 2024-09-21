"""Tests for the ProjectRepository class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from base.components.domain import EntityId
from core.domain.project import Project
from core.infrastructure.project import ProjectRepository

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import Table


class TestProjectRepository:
    """Tests for the ProjectRepository class."""

    def test_get(self, table: Table) -> None:
        """Test the get method."""
        table.put_item(
            Item={"project_id": "01DXF6DT000000000000000000", "item_name": "Project", "title": "Test Project"}
        )

        repository = ProjectRepository(table)
        actual = repository.get(EntityId(value="01DXF6DT000000000000000000"))

        expected = Project(id=EntityId(value="01DXF6DT000000000000000000"), title="Test Project")

        assert actual == expected

    def test_save(self, table: Table) -> None:
        """Test the save method."""
        project = Project(id=EntityId(value="01DXF6DT000000000000000000"), title="Test Project")

        repository = ProjectRepository(table)
        repository.save(project)

        actual = table.get_item(Key={"project_id": "01DXF6DT000000000000000000", "item_name": "Project"})["Item"]
        expected = {"project_id": "01DXF6DT000000000000000000", "item_name": "Project", "title": "Test Project"}

        assert actual == expected
