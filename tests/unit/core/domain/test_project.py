"""Tests for the Project domain object."""

from __future__ import annotations

from base.components.domain import EntityId
from core.domain.project import Project


class TestProject:
    """Project tests."""

    def test_new_project(self) -> None:
        """Test creating a new project."""
        project = Project(title="Test Project")

        assert project.id
        assert project.title == "Test Project"

    def test_reconstruct_project(self) -> None:
        """Test reconstructing a project."""
        project = Project(id=EntityId(value="01DXF6DT000000000000000000"), title="Test Project")

        assert project.id == EntityId(value="01DXF6DT000000000000000000")
        assert project.title == "Test Project"
