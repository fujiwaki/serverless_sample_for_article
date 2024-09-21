"""DI Container."""

from __future__ import annotations

from typing import TYPE_CHECKING

import boto3

from core.application.project import ProjectService
from core.application.task import TaskService
from core.infrastructure.project import ProjectRepository
from core.infrastructure.task import TaskRepository

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import Table


class Container:
    """DI Container."""

    def __init__(self, table_name: str) -> None:
        """Constructor."""
        self._table_name = table_name

    @property
    def table(self) -> Table:
        """The DynamoDB table instance."""
        if not hasattr(self, "_table"):
            self._table = boto3.resource("dynamodb").Table(self._table_name)
        return self._table

    @property
    def project_repository(self) -> ProjectRepository:
        """The project repository."""
        if not hasattr(self, "_project_repository"):
            self._project_repository = ProjectRepository(self.table)
        return self._project_repository

    @property
    def task_repository(self) -> TaskRepository:
        """The task repository."""
        if not hasattr(self, "_task_repository"):
            self._task_repository = TaskRepository(self.table)
        return self._task_repository

    @property
    def project_service(self) -> ProjectService:
        """The project service."""
        if not hasattr(self, "_project_service"):
            self._project_service = ProjectService(self.project_repository, self.task_repository)
        return self._project_service

    @property
    def task_service(self) -> TaskService:
        """The task service."""
        if not hasattr(self, "_task_service"):
            self._task_service = TaskService(self.task_repository)
        return self._task_service
