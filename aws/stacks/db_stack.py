"""DB stack."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from aws_cdk import NestedStack
from aws_cdk import aws_dynamodb as dynamodb

if TYPE_CHECKING:
    from constructs import Construct

sys.path.append((Path(__file__).parent.parent.parent / "src").as_posix())

from base.aws.dynamodb import Attribute, AttributeType
from core.infrastructure.table import table_schema


class DBStack(NestedStack):
    """Stack for the database resources."""

    table: dynamodb.TableV2

    def __init__(self, scope: Construct, construct_id: str) -> None:
        """Initialize the stack.

        Args:
            scope: The parent construct.
            construct_id: The construct ID.
        """
        super().__init__(scope, construct_id)

        self.table = dynamodb.TableV2(
            self,
            "Table",
            partition_key=self._convert_attribute(table_schema.primary.hash),
            sort_key=self._convert_attribute(table_schema.primary.range) if table_schema.primary.range else None,
            global_secondary_indexes=[
                dynamodb.GlobalSecondaryIndexPropsV2(
                    index_name=index_name,
                    partition_key=self._convert_attribute(index.hash),
                    sort_key=self._convert_attribute(index.range) if index.range else None,
                )
                for index_name, index in table_schema.global_secondary_indexes.items()
            ],
        )

    @staticmethod
    def _convert_attribute(attribute: Attribute) -> dynamodb.Attribute:
        """Convert an attribute."""
        match attribute.type:
            case AttributeType.STRING:
                attribute_type = dynamodb.AttributeType.STRING
            case AttributeType.NUMBER:
                attribute_type = dynamodb.AttributeType.NUMBER
            case AttributeType.BINARY:
                attribute_type = dynamodb.AttributeType.BINARY

        return dynamodb.Attribute(name=attribute.name, type=attribute_type)
