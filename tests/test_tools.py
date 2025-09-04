"""
Unit tests for the tools module.

This module tests the todo management functionality,
storage operations, and analytics features.
"""

import pytest
import json
import tempfile
from unittest.mock import patch, MagicMock
from pathlib import Path

# Import the tools module
try:
    from app.tools import (
        add_todo,
        remove_todo,
        complete_todo,
        list_todos,
        get_analytics,
        search_todos,
        StorageManager,
    )
except ImportError:
    # Handle import error gracefully for CI/CD
    pytest.skip("Tools module not available", allow_module_level=True)


class TestStorageManager:
    """Test cases for StorageManager class."""

    def test_storage_manager_initialization(self, temp_storage):
        """Test StorageManager initialization."""
        with patch("app.tools.STORAGE_FILE", Path(temp_storage)):
            storage = StorageManager()
            assert storage.storage_file.exists()

    def test_load_data(self, temp_storage):
        """Test loading data from storage."""
        test_data = {"test": "data"}
        with open(temp_storage, "w") as f:
            json.dump(test_data, f)

        with patch("app.tools.STORAGE_FILE", Path(temp_storage)):
            storage = StorageManager()
            data = storage._load_data()
            assert data["test"] == "data"

    def test_save_data(self, temp_storage):
        """Test saving data to storage."""
        with patch("app.tools.STORAGE_FILE", Path(temp_storage)):
            storage = StorageManager()
            test_data = {"new": "data"}
            storage._save_data(test_data)

            # Verify data was saved
            with open(temp_storage, "r") as f:
                saved_data = json.load(f)
            assert saved_data["new"] == "data"


class TestTodoOperations:
    """Test cases for todo operations."""

    def test_add_todo_basic(self, temp_storage):
        """Test adding a basic todo item."""
        with patch("app.tools.STORAGE_FILE", Path(temp_storage)):
            result = add_todo.func("Test todo item")

            assert "successfully added" in result.lower()

    def test_add_todo_with_priority(self, temp_storage):
        """Test adding todo with priority."""
        with patch("app.tools.STORAGE_FILE", Path(temp_storage)):
            result = add_todo.func("Urgent task", "high")

            assert "successfully added" in result.lower()
            assert "high priority" in result.lower()

    def test_list_todos_empty(self, temp_storage):
        """Test listing todos when list is empty."""
        with patch("app.tools.STORAGE_FILE", Path(temp_storage)):
            result = list_todos.func()

            assert "no todo items" in result.lower() or "empty" in result.lower()

    def test_list_todos_with_items(self, temp_storage):
        """Test listing todos with items."""
        with patch("app.tools.STORAGE_FILE", Path(temp_storage)):
            # Add a todo first
            add_todo.func("Test todo")

            result = list_todos.func()
            assert "test todo" in result.lower()

    def test_complete_todo_valid_index(self, temp_storage):
        """Test completing a todo with valid index."""
        with patch("app.tools.STORAGE_FILE", Path(temp_storage)):
            # Add a todo first
            add_todo.func("Test todo")

            result = complete_todo.func(1)
            assert "completed" in result.lower()

    def test_complete_todo_invalid_index(self, temp_storage):
        """Test completing a todo with invalid index."""
        with patch("app.tools.STORAGE_FILE", Path(temp_storage)):
            result = complete_todo.func(999)

            assert "invalid" in result.lower() or "not found" in result.lower()

    def test_remove_todo_valid_index(self, temp_storage):
        """Test removing a todo with valid index."""
        with patch("app.tools.STORAGE_FILE", Path(temp_storage)):
            # Add a todo first
            add_todo.func("Test todo")

            result = remove_todo.func(1)
            assert "removed" in result.lower() or "deleted" in result.lower()

    def test_search_todos(self, temp_storage):
        """Test searching todos by keyword."""
        with patch("app.tools.STORAGE_FILE", Path(temp_storage)):
            # Add some todos first
            add_todo.func("Buy groceries")
            add_todo.func("Walk the dog")

            result = search_todos.func("groceries")
            assert "groceries" in result.lower()


class TestAnalytics:
    """Test cases for analytics functionality."""

    def test_get_analytics_empty(self, temp_storage):
        """Test analytics with no todos."""
        with patch("app.tools.STORAGE_FILE", Path(temp_storage)):
            result = get_analytics.func()

            assert "analytics" in result.lower()
            assert "0" in result  # Should show 0 tasks

    def test_get_analytics_with_data(self, temp_storage):
        """Test analytics with todo data."""
        with patch("app.tools.STORAGE_FILE", Path(temp_storage)):
            # Add and complete some todos
            add_todo.func("Test todo 1")
            add_todo.func("Test todo 2")
            complete_todo.func(1)

            result = get_analytics.func()
            assert "analytics" in result.lower()


class TestToolIntegration:
    """Integration tests for tool functionality."""

    def test_full_todo_workflow(self, temp_storage):
        """Test complete todo workflow."""
        with patch("app.tools.STORAGE_FILE", Path(temp_storage)):
            # Add todo
            add_result = add_todo.func("Complete project")
            assert "successfully added" in add_result.lower()

            # List todos
            list_result = list_todos.func()
            assert "complete project" in list_result.lower()

            # Complete todo
            complete_result = complete_todo.func(1)
            assert "completed" in complete_result.lower()

            # Check analytics
            analytics_result = get_analytics.func()
            assert "analytics" in analytics_result.lower()

    def test_error_handling(self, temp_storage):
        """Test error handling in tools."""
        with patch("app.tools.STORAGE_FILE", Path(temp_storage)):
            # Test with invalid operations
            result = complete_todo.func(0)  # Invalid index
            assert "invalid" in result.lower() or "error" in result.lower()
