"""Table configuration."""

from __future__ import annotations

from base.aws.dynamodb import Attribute, AttributeType, KeySchema, TableSchema

_primary_key = KeySchema(
    hash=Attribute(name="project_id", type=AttributeType.STRING),
    range=Attribute(name="item_name", type=AttributeType.STRING),
)

table_schema = TableSchema(primary=_primary_key, global_secondary_indexes={})
