"""
PI SDK Models - Pydantic models for the PI SDK.

This module provides:
1. Base model with common functionality
2. Request/Response models for API endpoints
3. Data validation and serialization
4. Type safety and conversion
5. JSON schema generation

Usage:
    from pi_sdk.models import SomeModel
    
    model = SomeModel(field="value")
    json_data = model.model_dump_json()

v1 - Initial implementation with base models
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field, validator


class BaseModel(PydanticBaseModel):
    """
    Base model with common functionality.
    
    1. JSON serialization
    2. Validation methods
    3. Helper functions
    v1
    """
    
    class Config:
        """
        Pydantic configuration.
        
        1. Allow extra fields
        2. Use enum values
        3. Arbitrary type allowed
        v1
        """
        arbitrary_types_allowed = True
        use_enum_values = True
        populate_by_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }


class ErrorResponse(BaseModel):
    """
    Error response model.
    
    1. Error message
    2. Error code
    3. Additional context
    v1
    """
    message: str
    code: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)


class Metadata(BaseModel):
    """
    Common metadata model.
    
    1. Timestamps
    2. Version info
    3. Request context
    v1
    """
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    version: str = Field(default="1.0.0")
    request_id: Optional[str] = None


class PaginationParams(BaseModel):
    """
    Pagination parameters.
    
    1. Page size
    2. Page number/cursor
    3. Sort options
    v1
    """
    page_size: int = Field(default=50, ge=1, le=100)
    cursor: Optional[str] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = Field(default="desc", pattern="^(asc|desc)$")


class PaginatedResponse(BaseModel):
    """
    Paginated response wrapper.
    
    1. Results list
    2. Pagination info
    3. Total count
    v1
    """
    items: List[Any]
    total: int
    next_cursor: Optional[str] = None
    prev_cursor: Optional[str] = None
    has_more: bool = False


# Example model - we'll add more specific models once we have the API documentation
class ExampleModel(BaseModel):
    """
    Example model for demonstration.
    
    1. Basic fields
    2. Validation
    3. Relationships
    v1
    """
    id: str = Field(description="Unique identifier")
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    metadata: Metadata = Field(default_factory=Metadata)
    
    @validator('name')
    def name_must_be_valid(cls, v):
        """Validate name field."""
        if not v.strip():
            raise ValueError("Name cannot be empty or whitespace")
        return v.strip()
