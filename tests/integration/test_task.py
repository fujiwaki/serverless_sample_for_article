"""Integration tests for the task router."""

from __future__ import annotations

import json
from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from aws_lambda_powertools.utilities.typing import LambdaContext

from src import index


class TestTask:
    """Tests for task router."""

    @pytest.mark.usefixtures("_create_table")
    def test_post_task(self, context: LambdaContext) -> None:
        """Test getting a task."""
        event = {
            "path": "/projects/01DXF6DT000000000000000000/tasks",
            "httpMethod": "POST",
            "requestContext": {"requestId": "227b78aa-779d-47d4-a48e-ce62120393b8"},
            "queryStringParameters": {},
            "body": json.dumps({"title": "Test Task", "description": "Test Description"}),
        }

        actual = index.handler(event, context)
        body = json.loads(actual["body"])

        assert actual["statusCode"] == HTTPStatus.CREATED.value
        assert body["id"]
        assert body["project_id"] == "01DXF6DT000000000000000000"
        assert body["title"] == "Test Task"
        assert body["description"] == "Test Description"
