"""API stack."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from aws_cdk import Duration, NestedStack
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_lambda_python_alpha as python
from pydantic import BaseModel

if TYPE_CHECKING:
    from aws_lambda_powertools.event_handler.openapi.models import OpenAPI
    from constructs import Construct


src_path = Path(__file__).parent.parent.parent / "src"
sys.path.append(src_path.as_posix())

os.environ["SERVICE_NAME"] = ""
os.environ["TABLE_NAME"] = ""

from index import app  # noqa: E402


class Resource(BaseModel):
    """Resource model."""

    name: str
    methods: list[str]
    sub_resources: list[Resource]

    @classmethod
    def _build(cls, resources: dict[Path, list[str]]) -> list[Resource]:
        builded = []

        names = {path.parts[0] for path in resources}
        for name in names:
            sub_resources = {
                path.relative_to(name): methods
                for path, methods in resources.items()
                if path.is_relative_to(name) and len(path.parts) != 1
            }
            resource = Resource(
                name=name, methods=resources.get(Path(name), []), sub_resources=cls._build(sub_resources)
            )
            builded.append(resource)

        return builded

    @classmethod
    def from_openapi(cls, openapi: OpenAPI) -> Resource:
        """Create resource from OpenAPI model."""
        resources = {
            Path(path): list(item.model_dump(exclude_none=True).keys())
            for path, item in openapi.paths.items()  # type: ignore[union-attr]
        }
        return cls._build(resources)[0]


class APIStack(NestedStack):
    """API stack."""

    def __init__(self, scope: Construct, id_: str, table: dynamodb.TableV2) -> None:
        """Initialize the stateless stack."""
        super().__init__(scope, id_)

        lambda_function = self.add_lambda("Sample", table)
        self.add_api(lambda_function)

    def add_lambda(self, service_name: str, table: dynamodb.TableV2) -> python.PythonFunction:
        """Add lambda."""
        project_dir_path = Path(__file__).parent.parent.parent
        src_dir_path = project_dir_path / "src"

        cmd = "uv pip compile pyproject.toml -o src/requirements.txt".split()
        subprocess.run(cmd, cwd=project_dir_path, check=True)  # noqa: S603

        lambda_function = python.PythonFunction(
            self,
            "Lambda",
            entry=src_dir_path.as_posix(),
            runtime=lambda_.Runtime.PYTHON_3_12,
            adot_instrumentation=lambda_.AdotInstrumentationConfig(
                exec_wrapper=lambda_.AdotLambdaExecWrapper.INSTRUMENT_HANDLER,
                layer_version=lambda_.AdotLayerVersion.from_python_sdk_layer_version(
                    lambda_.AdotLambdaLayerPythonSdkVersion.LATEST
                ),
            ),
            environment={"TABLE_NAME": table.table_name, "SERVICE_NAME": service_name},
            timeout=Duration.seconds(10),
        )

        cmd = "rm -r src/requirements.txt".split()
        subprocess.run(cmd, cwd=project_dir_path, check=True)  # noqa: S603

        table.grant_read_write_data(lambda_function)
        return lambda_function

    def _add_api_resource(self, target: apigateway.IResource, resource: Resource) -> None:
        """Add API resource."""
        for method in resource.methods:
            target.add_method(method)

        for sub_resource in resource.sub_resources:
            sub_target = target.add_resource(sub_resource.name)
            self._add_api_resource(sub_target, sub_resource)

    def add_api(self, handler: python.PythonFunction) -> None:
        """Add API."""
        api = apigateway.LambdaRestApi(self, "API", handler=handler)
        resource = Resource.from_openapi(app.get_openapi_schema(openapi_version="3.1.0"))
        self._add_api_resource(api.root, resource)
