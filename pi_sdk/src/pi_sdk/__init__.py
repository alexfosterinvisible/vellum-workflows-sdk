"""
PI SDK - Python SDK for the PI API.

This package provides:
1. Easy-to-use client interface
2. Type-safe models and validation
3. Comprehensive error handling
4. Both sync and async support
5. Automatic retries and rate limiting

Usage:
    from pi_sdk import PIClient
    
    client = PIClient(api_key="your-api-key")
    result = client.some_method()

v1 - Initial implementation
"""

from .client import PIClient
from .exceptions import PIAuthError, PIConnectionError, PIError, PIRateLimitError, PIServerError, PITimeoutError, PIValidationError
from .models import BaseModel, ErrorResponse, ExampleModel, Metadata, PaginatedResponse, PaginationParams

__version__ = "0.1.0"
__author__ = "Alex Foster"
__email__ = "alexfosterinvisible@gmail.com"

__all__ = [
    "PIClient",
    "PIError",
    "PIAuthError",
    "PIRateLimitError",
    "PIValidationError",
    "PITimeoutError",
    "PIConnectionError",
    "PIServerError",
    "BaseModel",
    "ErrorResponse",
    "Metadata",
    "PaginationParams",
    "PaginatedResponse",
    "ExampleModel"
]
