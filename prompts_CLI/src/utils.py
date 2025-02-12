
import os
from typing import Optional


def get_secret(secret_name: str, default: Optional[str] = None) -> Optional[str]:
    """Get secret from Replit Secrets or environment variable."""
    # Try Replit Secrets first (available as environment variables)
    value = os.environ.get(secret_name)
    if value:
        return value
    return default
