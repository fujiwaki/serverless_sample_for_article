"""Task infrastructure."""

from __future__ import annotations

from typing import TYPE_CHECKING

from base.aws.dynamodb import Item, Repository
from base.components.domain import EntityId
from core.domain.repositories import TaskRepository as AbstractTaskRepository
from core.domain.task import Task

from .table import table_schema

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import Table


class TaskItem(Item):
    """Task item for DynamoDB.

    Attributes:
        project_id: Project ID.
        item_name: Item name.
        title: Task title.
        description: Task description.
    """

    project_id: str
    item_name: str
    title: str
    description: str

    @classmethod
    def from_entity(cls, entity: Task) -> TaskItem:
        """Create an item from an entity.

        Args:
            entity: Task entity.
        """
        return cls(
            project_id=str(entity.project_id),
            item_name=f"Task#{entity.id}",
            title=entity.title,
            description=entity.description,
        )

    def to_entity(self) -> Task:
        """Create an entity from an item."""
        return Task(
            id=EntityId(value=self.item_name.removeprefix("Task#")),
            project_id=EntityId(value=self.project_id),
            title=self.title,
            description=self.description,
        )


class TaskRepository(AbstractTaskRepository, Repository):
    """Task repository implementation."""

    def __init__(self, table: Table) -> None:
        """Constructor.

        Args:
            table: DynamoDB table.
        """
        super().__init__(table, table_schema)

    def get_by_project_id(self, project_id: EntityId) -> list[Task]:
        """Get tasks.

        Args:
            project_id: Project ID.
        """
        items = self._query(TaskItem, hash_=str(project_id), range_=self._range_key().begins_with("Task#"))
        return [item.to_entity() for item in items]

    def save(self, task: Task) -> None:
        """Save a task.

        Args:
            task: Task.
        """
        item = TaskItem.from_entity(task)
        self._put(item=item)
