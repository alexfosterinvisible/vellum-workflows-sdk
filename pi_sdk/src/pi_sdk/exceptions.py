"""
PI SDK Exceptions - Custom exceptions for the PI SDK.

This module provides:
1. Base exception class for all PI errors
2. Specific error types for common API issues
3. Detailed error messages and context
4. Error code mapping and handling

Usage:
    try:
        client.some_method()
    except PIAuthError:
        # Handle authentication error
    except PIRateLimitError:
        # Handle rate limit error
    except PIError as e:
        # Handle general error

v1 - Initial implementation with basic exceptions
"""


class PIError(Exception):
    """
    Base exception for all PI SDK errors.

    1. Provides common error interface
    2. Includes error code and message
    3. Optional context data
    v1
    """

    def __init__(self, message: str, code: str = None, context: dict = None):
        """
        Initialize the error.

        1. Set error message
        2. Set error code if provided
        3. Set context data if provided
        v1
        """
        self.message = message
        self.code = code
        self.context = context or {}
        super().__init__(self.message)


class PIAuthError(PIError):
    """
    Authentication error.

    1. Invalid API key
    2. Expired credentials
    3. Missing authentication
    v1
    """

    def __init__(self, message: str = "Authentication failed", context: dict = None):
        super().__init__(message, code="auth_error", context=context)


class PIRateLimitError(PIError):
    """
    Rate limit exceeded error.

    1. Too many requests
    2. Quota exceeded
    3. Includes retry-after info
    v1
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: int = None,
        context: dict = None
    ):
        context = context or {}
        if retry_after:
            context['retry_after'] = retry_after
        super().__init__(message, code="rate_limit_error", context=context)


class PIValidationError(PIError):
    """
    Input validation error.

    1. Invalid parameters
    2. Missing required fields
    3. Type mismatches
    v1
    """

    def __init__(self, message: str = "Validation failed", context: dict = None):
        super().__init__(message, code="validation_error", context=context)


class PITimeoutError(PIError):
    """
    Request timeout error.

    1. Network timeout
    2. API timeout
    3. Long-running operation timeout
    v1
    """

    def __init__(self, message: str = "Request timed out", context: dict = None):
        super().__init__(message, code="timeout_error", context=context)


class PIConnectionError(PIError):
    """
    Connection error.

    1. Network connectivity issues
    2. DNS failures
    3. SSL/TLS errors
    v1
    """

    def __init__(self, message: str = "Connection failed", context: dict = None):
        super().__init__(message, code="connection_error", context=context)


class PIServerError(PIError):
    """
    Server-side error.

    1. Internal server errors
    2. Service unavailable
    3. Maintenance mode
    v1
    """

    def __init__(self, message: str = "Server error", context: dict = None):
        super().__init__(message, code="server_error", context=context)
