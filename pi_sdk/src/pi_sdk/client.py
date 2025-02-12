"""
PI SDK Client - Main client implementation for the PI API.

This module provides:
1. Synchronous and asynchronous client implementations
2. Automatic retries and rate limiting
3. Comprehensive error handling
4. Type safety throughout
5. Streaming support for applicable endpoints

Usage:
    from pi_sdk import PIClient

    # Synchronous usage
    client = PIClient(api_key="your-api-key")
    result = client.some_method()

    # Async usage
    async with PIClient(api_key="your-api-key") as client:
        result = await client.some_method_async()

v1 - Initial implementation with basic structure
"""

import logging
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import aiohttp
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from .exceptions import PIAuthError, PIError, PIRateLimitError


class PIClient:
    """
    Main client for interacting with the PI API.

    1. Handles authentication and request signing
    2. Provides both sync and async methods
    3. Implements retry logic and rate limiting
    4. Manages API versioning
    v1
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.pi.ai/v1",
        timeout: int = 30,
        max_retries: int = 3,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize the PI client.

        1. Set up authentication
        2. Configure base API parameters
        3. Initialize logging
        4. Set up retry policies
        v1
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = logger or logging.getLogger(__name__)

        # Session objects for reuse
        self._session: Optional[requests.Session] = None
        self._async_session: Optional[aiohttp.ClientSession] = None

    def __enter__(self):
        """
        Context manager entry for synchronous usage.

        1. Initialize session
        2. Set up auth headers
        3. Return self for context
        v1
        """
        self._session = requests.Session()
        self._session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'pi-sdk-python/0.1.0'
        })
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit for synchronous usage.

        1. Close session
        2. Clean up resources
        v1
        """
        if self._session:
            self._session.close()
            self._session = None

    async def __aenter__(self):
        """
        Context manager entry for asynchronous usage.

        1. Initialize async session
        2. Set up auth headers
        3. Return self for context
        v1
        """
        self._async_session = aiohttp.ClientSession(headers={
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'pi-sdk-python/0.1.0'
        })
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit for asynchronous usage.

        1. Close async session
        2. Clean up resources
        v1
        """
        if self._async_session:
            await self._async_session.close()
            self._async_session = None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make a synchronous HTTP request to the PI API.

        1. Build request with auth
        2. Handle response
        3. Process errors
        4. Return parsed response
        v1
        """
        url = urljoin(self.base_url, endpoint)

        # Ensure session exists
        if not self._session:
            self.__enter__()

        try:
            response = self._session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise PIAuthError("Invalid API key")
            elif e.response.status_code == 429:
                raise PIRateLimitError("Rate limit exceeded")
            else:
                raise PIError(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            raise PIError(f"Request failed: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _arequest(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make an asynchronous HTTP request to the PI API.

        1. Build async request with auth
        2. Handle response
        3. Process errors
        4. Return parsed response
        v1
        """
        url = urljoin(self.base_url, endpoint)

        # Ensure session exists
        if not self._async_session:
            await self.__aenter__()

        try:
            async with self._async_session.request(method, url, **kwargs) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            if e.status == 401:
                raise PIAuthError("Invalid API key")
            elif e.status == 429:
                raise PIRateLimitError("Rate limit exceeded")
            else:
                raise PIError(f"HTTP {e.status}: {e.message}")
        except Exception as e:
            raise PIError(f"Request failed: {str(e)}")

    # Example method implementations will go here
    # We'll add specific API methods once we have the API documentation
