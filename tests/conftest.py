"""
Test configuration and fixtures for Rex AI Assistant
"""
import pytest
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main


@pytest.fixture
def app():
    """Create Flask test app"""
    app = main.app
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test-secret-key"
    })
    
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """Create Flask test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create Flask CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def sample_message():
    """Sample chat message for testing"""
    return {
        "message": "Hello, how are you today?"
    }


@pytest.fixture
def sample_todo():
    """Sample todo item for testing"""
    return {
        "task": "Test todo item",
        "completed": False
    }
