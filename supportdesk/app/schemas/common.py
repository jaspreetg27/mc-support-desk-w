"""Common Pydantic schemas and base classes."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        validate_assignment=True,
    )


class TimestampSchema(BaseSchema):
    """Schema mixin for created_at and updated_at timestamps."""

    created_at: datetime
    updated_at: datetime


class UUIDSchema(BaseSchema):
    """Schema mixin for UUID primary key."""

    id: uuid.UUID


class PaginationParams(BaseModel):
    """Common pagination parameters."""

    skip: int = 0
    limit: int = 100

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
    )


class PaginatedResponse(BaseSchema):
    """Generic paginated response wrapper."""

    items: list
    total: int
    skip: int
    limit: int
    has_more: bool

    @classmethod
    def create(
        cls,
        items: list,
        total: int,
        skip: int = 0,
        limit: int = 100,
    ) -> "PaginatedResponse":
        """Create paginated response."""
        return cls(
            items=items,
            total=total,
            skip=skip,
            limit=limit,
            has_more=(skip + len(items)) < total,
        )
