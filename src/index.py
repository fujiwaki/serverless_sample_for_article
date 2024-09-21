"""Lambda function entrypoint."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import ApiGatewayResolver
from aws_lambda_powertools.logging import correlation_paths

from core.config.container import Container
from routers import project, task

if TYPE_CHECKING:
    from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger(service=os.environ["SERVICE_NAME"])

app = ApiGatewayResolver(enable_validation=True)
app.include_router(project.router, prefix="/projects")
app.include_router(task.router, prefix="/projects/<project_id>/tasks")

container = Container(os.environ["TABLE_NAME"])


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
def handler(event: dict[str, Any], context: LambdaContext) -> dict[str, Any]:
    """Lambda function handler."""
    app.append_context(container=container)  # type: ignore[no-untyped-call]
    return app.resolve(event, context)
