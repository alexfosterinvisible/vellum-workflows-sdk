"""
PI SDK Test Configuration - Shared fixtures and configuration for tests.

This module provides:
1. Shared test fixtures
2. Mock data and helpers
3. Test configuration
4. Common test utilities
5. Environment setup

Usage:
    # In any test file:
    def test_something(mock_client, mock_data):
        ...

v1 - Initial implementation with basic fixtures
"""

import pytest
import responses
from unittest.mock import MagicMock
from datetime import datetime, timezone

from pi_sdk import PIClient
from pi_sdk.models import Metadata


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    """
    Mock environment variables.
    
    1. Set test API key
    2. Configure test environment
    3. Clean up after tests
    v1
    """
    monkeypatch.setenv("PI_API_KEY", "test-api-key")
    monkeypatch.setenv("PI_ENVIRONMENT", "test")


@pytest.fixture
def mock_client():
    """
    Create a mock client with pre-configured responses.
    
    1. Initialize mock client
    2. Set up common responses
    3. Configure error scenarios
    v1
    """
    with responses.RequestsMock() as rsps:
        client = PIClient(api_key="test-api-key")
        # Add common mock responses here
        yield client


@pytest.fixture
def mock_data():
    """
    Create mock data for testing.
    
    1. Generate test data
    2. Set up relationships
    3. Include metadata
    v1
    """
    return {
        "id": "test-id-123",
        "name": "Test Object",
        "description": "Test Description",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "metadata": {
            "version": "1.0.0",
            "environment": "test"
        }
    }


@pytest.fixture
def mock_metadata():
    """
    Create mock metadata.
    
    1. Set timestamps
    2. Add version info
    3. Include request context
    v1
    """
    return Metadata(
        created_at=datetime.now(timezone.utc),
        version="1.0.0",
        request_id="test-request-123"
    )


@pytest.fixture
def mock_response():
    """
    Create mock HTTP response.
    
    1. Set status code
    2. Add headers
    3. Include response data
    v1
    """
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "data": {
            "id": "test-id-123",
            "type": "test_object",
            "attributes": {
                "name": "Test Object",
                "description": "Test Description"
            }
        },
        "meta": {
            "request_id": "test-request-123"
        }
    }
    return mock_resp


@pytest.fixture
def mock_error_response():
    """
    Create mock error response.
    
    1. Set error status
    2. Add error details
    3. Include debug info
    v1
    """
    mock_resp = MagicMock()
    mock_resp.status_code = 400
    mock_resp.json.return_value = {
        "error": {
            "code": "validation_error",
            "message": "Invalid input",
            "details": ["Field 'name' is required"]
        },
        "meta": {
            "request_id": "test-error-123"
        }
    }
    return mock_resp


@pytest.fixture
def mock_async_client():
    """
    Create a mock async client.
    
    1. Set up async mock
    2. Configure responses
    3. Handle cleanup
    v1
    """
    client = PIClient(api_key="test-api-key")
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "success"}
    mock_response.__aenter__.return_value = mock_response
    mock_session.request.return_value = mock_response
    client._async_session = mock_session
    return client


def pytest_configure(config):
    """
    Configure pytest.
    
    1. Set up markers
    2. Configure plugins
    3. Set test environment
    v1
    """
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers",
        "async_test: mark test as async test"
    )


def pytest_collection_modifyitems(items):
    """
    Modify test items.
    
    1. Add markers
    2. Skip tests
    3. Reorder tests
    v1
    """
    for item in items:
        if "async" in item.nodeid:
            item.add_marker(pytest.mark.async_test)
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
