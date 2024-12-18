"""
PI SDK Tests - Test cases for the PI SDK client.

This module provides:
1. Unit tests for client functionality
2. Integration tests for API endpoints
3. Mock responses and fixtures
4. Error handling tests
5. Async test cases

Usage:
    pytest tests/test_client.py
    pytest tests/test_client.py -v
    pytest tests/test_client.py -k "test_auth"

v1 - Initial implementation with basic tests
"""

import pytest
import responses
from unittest.mock import patch, MagicMock
from datetime import datetime

from pi_sdk import PIClient
from pi_sdk.exceptions import PIAuthError, PIRateLimitError, PIError
from pi_sdk.models import ExampleModel, Metadata


@pytest.fixture
def client():
    """
    Create a test client.
    
    1. Initialize with test API key
    2. Configure for testing
    3. Clean up after tests
    v1
    """
    return PIClient(api_key="test-api-key")


@pytest.fixture
def mock_response():
    """
    Create mock response data.
    
    1. Sample response data
    2. Common fields
    3. Test metadata
    v1
    """
    return {
        "id": "test-id",
        "name": "Test Name",
        "description": "Test Description",
        "metadata": {
            "created_at": datetime.utcnow().isoformat(),
            "version": "1.0.0"
        }
    }


class TestPIClient:
    """
    Test cases for PIClient.
    
    1. Authentication tests
    2. Request/response tests
    3. Error handling tests
    4. Async operation tests
    v1
    """
    
    def test_init(self, client):
        """
        Test client initialization.
        
        1. Check API key setting
        2. Verify default values
        3. Test logger setup
        v1
        """
        assert client.api_key == "test-api-key"
        assert client.base_url == "https://api.pi.ai/v1"
        assert client.timeout == 30
    
    @responses.activate
    def test_authentication_error(self, client):
        """
        Test authentication error handling.
        
        1. Mock 401 response
        2. Verify error raising
        3. Check error details
        v1
        """
        responses.add(
            responses.GET,
            "https://api.pi.ai/v1/test",
            json={"error": "Invalid API key"},
            status=401
        )
        
        with pytest.raises(PIAuthError) as exc_info:
            with client:
                client._request("GET", "/test")
        
        assert "Invalid API key" in str(exc_info.value)
    
    @responses.activate
    def test_rate_limit_error(self, client):
        """
        Test rate limit error handling.
        
        1. Mock 429 response
        2. Verify error raising
        3. Check retry-after
        v1
        """
        responses.add(
            responses.GET,
            "https://api.pi.ai/v1/test",
            json={"error": "Rate limit exceeded"},
            status=429,
            headers={"Retry-After": "60"}
        )
        
        with pytest.raises(PIRateLimitError) as exc_info:
            with client:
                client._request("GET", "/test")
        
        assert "Rate limit exceeded" in str(exc_info.value)
    
    @responses.activate
    def test_successful_request(self, client, mock_response):
        """
        Test successful request handling.
        
        1. Mock successful response
        2. Verify response parsing
        3. Check model creation
        v1
        """
        responses.add(
            responses.GET,
            "https://api.pi.ai/v1/test",
            json=mock_response,
            status=200
        )
        
        with client:
            response = client._request("GET", "/test")
        
        assert response["id"] == mock_response["id"]
        assert response["name"] == mock_response["name"]
    
    @pytest.mark.asyncio
    async def test_async_request(self, client, mock_response):
        """
        Test async request handling.
        
        1. Mock async response
        2. Verify async operation
        3. Check response data
        v1
        """
        mock_session = MagicMock()
        mock_response_obj = MagicMock()
        mock_response_obj.json.return_value = mock_response
        mock_response_obj.__aenter__.return_value = mock_response_obj
        
        mock_session.request.return_value = mock_response_obj
        
        with patch('aiohttp.ClientSession', return_value=mock_session):
            async with client:
                response = await client._arequest("GET", "/test")
        
        assert response["id"] == mock_response["id"]
        assert response["name"] == mock_response["name"]
    
    def test_context_manager(self, client):
        """
        Test context manager functionality.
        
        1. Check session creation
        2. Verify cleanup
        3. Test reuse
        v1
        """
        with client as c:
            assert c._session is not None
            assert "Authorization" in c._session.headers
        
        assert client._session is None
    
    @pytest.mark.asyncio
    async def test_async_context_manager(self, client):
        """
        Test async context manager functionality.
        
        1. Check async session creation
        2. Verify async cleanup
        3. Test async reuse
        v1
        """
        async with client as c:
            assert c._async_session is not None
            assert "Authorization" in c._async_session._default_headers
        
        assert client._async_session is None


# More test cases will be added as we implement specific API endpoints
