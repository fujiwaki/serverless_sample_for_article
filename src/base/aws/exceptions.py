"""Exceptions for aws module."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.type_defs import TableAttributeValueTypeDef


class ItemNotFoundError(Exception):
    """Item not found error."""

    def __init__(
        self, item_type: type, hash_: TableAttributeValueTypeDef, range_: TableAttributeValueTypeDef | None = None
    ) -> None:
        """Initialize ItemNotFoundError."""
        super().__init__(f"Item {item_type}(hash: {hash_!s}, range: {range_!s}) was not found.")


class RangeKeyNotFoundError(Exception):
    """Range key not found error."""

    def __init__(self) -> None:
        """Initialize RangeKeyNotFoundError."""
        super().__init__("Range key was not found.")
