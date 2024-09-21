"""Project router."""

from http import HTTPStatus
from typing import TYPE_CHECKING

from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import Response
from aws_lambda_powertools.event_handler.router import APIGatewayRouter

from core.application.project import CreateProjectCommand, GetProjectCommand

from .models.project import NewProjectRequest, ProjectResponse

if TYPE_CHECKING:
    from core.config.container import Container


logger = Logger(child=True)
router = APIGatewayRouter()  # type: ignore[no-untyped-call]


@router.get("/<project_id>")  # type: ignore[misc]
def get_project(project_id: str) -> ProjectResponse:
    """GET /projects/{project_id} handler."""
    container: Container = router.context["container"]
    command = GetProjectCommand(id=project_id)
    project = container.project_service.get(command)
    return ProjectResponse.from_dto(project)


@router.post("/")  # type: ignore[misc]
def post_project(request: NewProjectRequest) -> Response[ProjectResponse]:
    """POST /projects handler."""
    container: Container = router.context["container"]
    command = CreateProjectCommand(title=request.title)
    project = container.project_service.create(command)
    return Response(status_code=HTTPStatus.CREATED.value, body=ProjectResponse.from_dto(project).model_dump_json())  # type: ignore[arg-type]
