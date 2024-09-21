"""Task router."""

from http import HTTPStatus
from typing import TYPE_CHECKING

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import Response
from aws_lambda_powertools.event_handler.router import APIGatewayRouter

from core.application.task import CreateTaskCommand

from .models.task import NewTaskRequest, TaskResponse

if TYPE_CHECKING:
    from core.config.container import Container


logger = Logger(child=True)
router = APIGatewayRouter()  # type: ignore[no-untyped-call]


@router.post("/")  # type: ignore[misc]
def post_task(project_id: str, request: NewTaskRequest) -> Response[TaskResponse]:
    """POST /projects/<project_id>/tasks handler."""
    container: Container = router.context["container"]
    command = CreateTaskCommand(project_id=project_id, title=request.title, description=request.description)
    task = container.task_service.create(command)
    return Response(status_code=HTTPStatus.CREATED.value, body=TaskResponse.from_dto(task).model_dump_json())  # type: ignore[arg-type]
