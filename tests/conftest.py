"""
Test configuration and fixtures for Rex AI Assistant.

This module provides common test configuration, fixtures, and utilities
for testing the Rex AI Assistant application.
"""

import pytest
import tempfile
import os
from pathlib import Path
import json

# Test configuration
TEST_CONFIG = {
    "TESTING": True,
    "WTF_CSRF_ENABLED": False,
    "SECRET_KEY": "test-secret-key",
}


@pytest.fixture
def app():
    """Create application instance for testing."""
    # Import here to avoid circular imports
    from main import app as flask_app

    flask_app.config.update(TEST_CONFIG)

    with flask_app.app_context():
        yield flask_app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test runner."""
    return app.test_cli_runner()


@pytest.fixture
def temp_storage():
    """Create temporary storage file for testing."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as f:
        test_data = {
            "conversation_history": [],
            "user_name": None,
            "analytics": {
                "total_tasks_created": 0,
                "total_tasks_completed": 0,
                "total_conversations": 0,
                "completion_rate": 0,
            },
        }
        json.dump(test_data, f)
        f.flush()

        yield f.name

        # Cleanup
        try:
            os.unlink(f.name)
        except OSError:
            pass


@pytest.fixture
def mock_api_response():
    """Mock API response for testing."""
    return {"choices": [{"message": {"content": "Test AI response from mock API"}}]}


class TestHelper:
    """Helper class for common test operations."""

    @staticmethod
    def create_test_todo(description="Test todo", priority="medium"):
        """Create a test todo item."""
        return {
            "description": description,
            "priority": priority,
            "created_at": "2024-01-01T00:00:00Z",
            "completed": False,
            "id": 1,
        }

    @staticmethod
    def create_test_user_data(name="Test User"):
        """Create test user data."""
        return {"name": name, "created_at": "2024-01-01T00:00:00Z"}
