"""Root stack."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aws_cdk import Stack

from .api_stack import APIStack
from .db_stack import DBStack

if TYPE_CHECKING:
    from constructs import Construct


class RootStack(Stack):
    """Root stack."""

    def __init__(self, scope: Construct, construct_id: str) -> None:
        """Initialize the stack.

        Args:
            scope: The parent construct.
            construct_id: The construct ID.
        """
        super().__init__(scope, construct_id)

        db_stack = DBStack(self, "DBStack")
        APIStack(self, "APIStack", db_stack.table)
