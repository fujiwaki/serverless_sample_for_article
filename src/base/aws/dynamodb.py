"""Base model for DynamoDB."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from boto3.dynamodb.conditions import Key
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict

from base.components.domain import Repository as BaseRepository

from .exceptions import ItemNotFoundError, RangeKeyNotFoundError

if TYPE_CHECKING:
    from boto3.dynamodb.conditions import ConditionBase
    from mypy_boto3_dynamodb.service_resource import Table
    from mypy_boto3_dynamodb.type_defs import TableAttributeValueTypeDef


class BaseModel(PydanticBaseModel):
    """Base model."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class AttributeType(Enum):
    """Attribute type."""

    STRING = "S"
    NUMBER = "N"
    BINARY = "B"


class Attribute(BaseModel):
    """Attribute."""

    name: str
    type: AttributeType


class KeySchema(BaseModel):
    """Key schema."""

    hash: Attribute
    range: Attribute | None = None


class TableSchema(BaseModel):
    """Table schema."""

    primary: KeySchema
    global_secondary_indexes: dict[str, KeySchema]


class Item(PydanticBaseModel):
    """Item."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class Repository(BaseRepository):
    """Base repository for DynamoDB."""

    def __init__(self, table: Table, schema: TableSchema) -> None:
        """Initialize DynamoDBRepository."""
        self._table = table
        self._schema = schema

    def _hash_key(self, index: str | None = None) -> Key:
        """Get hash key."""
        key_schema = self._schema.primary if not index else self._schema.global_secondary_indexes[index]
        return Key(key_schema.hash.name)

    def _range_key(self, index: str | None = None) -> Key:
        """Get range key."""
        key_schema = self._schema.primary if not index else self._schema.global_secondary_indexes[index]

        if not key_schema.range:
            raise RangeKeyNotFoundError

        return Key(key_schema.range.name)

    def _get[T: Item](
        self, item_type: type[T], hash_: TableAttributeValueTypeDef, range_: TableAttributeValueTypeDef | None = None
    ) -> T:
        """Get item."""
        key_schema = self._schema.primary
        key = (
            {key_schema.hash.name: hash_, key_schema.range.name: range_}
            if key_schema.range
            else {key_schema.hash.name: hash_}
        )
        result = self._table.get_item(Key=key)

        if "Item" not in result:
            raise ItemNotFoundError(item_type, hash_, range_)

        return item_type(**result["Item"])

    def _query[T: Item](
        self,
        item_type: type[T],
        hash_: TableAttributeValueTypeDef,
        range_: ConditionBase | None = None,
        index: str | None = None,
    ) -> list[T]:
        """Query items."""
        key_condition_expression = (
            self._hash_key(index).eq(hash_) & range_ if range_ else self._hash_key(index).eq(hash_)
        )

        if not index:
            result = self._table.query(KeyConditionExpression=key_condition_expression)
        else:
            result = self._table.query(IndexName=index, KeyConditionExpression=key_condition_expression)

        return [item_type(**item) for item in result["Items"]]

    def _put[T: Item](self, item: T) -> None:
        """Put item."""
        self._table.put_item(Item=item.model_dump())
