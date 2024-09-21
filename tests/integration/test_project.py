"""Integration tests for the project router."""

from __future__ import annotations

import json
from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from aws_lambda_powertools.utilities.typing import LambdaContext
    from mypy_boto3_dynamodb.service_resource import Table

from src import index


class TestProject:
    """Tests for project router."""

    def test_get_project(self, context: LambdaContext, table: Table) -> None:
        """Test getting a project."""
        items = [
            {
                "project_id": "01DXF6DT000000000000000000",
                "item_name": "Project",
                "title": "Test Project",
            },
            {
                "project_id": "01DXF6DT000000000000000000",
                "item_name": "Task#01DXHRTH000000000000000000",
                "title": "Test Task",
                "description": "Test Description",
            },
        ]
        for item in items:
            table.put_item(Item=item)

        event = {
            "path": "/projects/01DXF6DT000000000000000000",
            "httpMethod": "GET",
            "requestContext": {"requestId": "227b78aa-779d-47d4-a48e-ce62120393b8"},
            "queryStringParameters": {},
        }

        actual = index.handler(event, context)
        body = json.loads(actual["body"])

        expected_body = {
            "id": "01DXF6DT000000000000000000",
            "title": "Test Project",
            "tasks": [{"id": "01DXHRTH000000000000000000", "title": "Test Task", "description": "Test Description"}],
        }

        assert actual["statusCode"] == HTTPStatus.OK.value
        assert body == expected_body

    @pytest.mark.usefixtures("_create_table")
    def test_post_project(self, context: LambdaContext) -> None:
        """Test creating a project."""
        event = {
            "path": "/projects",
            "httpMethod": "POST",
            "requestContext": {"requestId": "227b78aa-779d-47d4-a48e-ce62120393b8"},
            "queryStringParameters": {},
            "body": json.dumps({"title": "Test Project"}),
        }

        actual = index.handler(event, context)
        body = json.loads(actual["body"])

        assert actual["statusCode"] == HTTPStatus.CREATED.value
        assert body["id"]
        assert body["title"] == "Test Project"
