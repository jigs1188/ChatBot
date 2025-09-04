"""
Unit tests for the main Flask application.

This module tests the main application routes, error handling,
and core functionality of Rex AI Assistant.
"""

import pytest
import json
from unittest.mock import patch, MagicMock


class TestMainApplication:
    """Test cases for main application functionality."""

    def test_index_route(self, client):
        """Test that index route returns successfully."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Rex AI Assistant" in response.data

    def test_static_files_served(self, client):
        """Test that static files are served correctly."""
        response = client.get("/static/style.css")
        assert response.status_code == 200

    def test_manifest_route(self, client):
        """Test PWA manifest route."""
        response = client.get("/manifest.json")
        assert response.status_code == 200

        # Verify it's valid JSON
        data = json.loads(response.data)
        assert "name" in data
        assert "icons" in data

    @patch("main.requests.post")
    def test_chat_endpoint_success(self, mock_post, client):
        """Test successful chat API call."""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello! I'm Rex AI Assistant."}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        response = client.post(
            "/chat",
            data=json.dumps({"message": "Hello"}),
            content_type="application/json",
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "response" in data
        assert data["response"] == "Hello! I'm Rex AI Assistant."

    def test_chat_endpoint_invalid_request(self, client):
        """Test chat endpoint with invalid request."""
        response = client.post(
            "/chat", data=json.dumps({}), content_type="application/json"
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    @patch("main.requests.post")
    def test_chat_endpoint_api_error(self, mock_post, client):
        """Test chat endpoint when API fails."""
        # Mock API error
        mock_post.side_effect = Exception("API Error")

        response = client.post(
            "/chat",
            data=json.dumps({"message": "Hello"}),
            content_type="application/json",
        )

        assert response.status_code == 500
        data = json.loads(response.data)
        assert "error" in data


class TestApplicationConfig:
    """Test application configuration and setup."""

    def test_app_config(self, app):
        """Test application configuration."""
        assert app.config["TESTING"] is True
        assert "SECRET_KEY" in app.config

    def test_storage_initialization(self, temp_storage):
        """Test storage file initialization."""
        # This should be covered by the storage manager tests
        pass


class TestErrorHandling:
    """Test error handling across the application."""

    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get("/nonexistent-route")
        assert response.status_code == 404

    def test_405_method_not_allowed(self, client):
        """Test 405 method not allowed."""
        response = client.put("/")  # PUT not allowed on index
        assert response.status_code == 405
