"""Project infrastructure."""

from __future__ import annotations

from typing import TYPE_CHECKING

from base.aws.dynamodb import Item, Repository
from base.components.domain import EntityId
from core.domain.project import Project
from core.domain.repositories import ProjectRepository as AbstractProjectRepository

from .table import table_schema

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import Table


class ProjectItem(Item):
    """Project item for DynamoDB.

    Attributes:
        project_id: Project ID.
        item_name: Item name.
        title: Project title.
    """

    project_id: str
    item_name: str = "Project"
    title: str

    @classmethod
    def from_entity(cls, entity: Project) -> ProjectItem:
        """Create an item from an entity.

        Args:
            entity: Project entity.
        """
        return cls(project_id=str(entity.id), title=entity.title)

    def to_entity(self) -> Project:
        """Create an entity from an item."""
        return Project(id=EntityId(value=self.project_id), title=self.title)


class ProjectRepository(AbstractProjectRepository, Repository):
    """Project repository implementation."""

    def __init__(self, table: Table) -> None:
        """Constructor.

        Args:
            table: DynamoDB table.
        """
        super().__init__(table, table_schema)

    def get(self, project_id: EntityId) -> Project:
        """Get a project.

        Args:
            project_id: Project ID.
        """
        item = self._get(ProjectItem, hash_=str(project_id), range_="Project")
        return item.to_entity()

    def save(self, project: Project) -> None:
        """Save a project.

        Args:
            project: Project.
        """
        item = ProjectItem.from_entity(project)
        self._put(item=item)
