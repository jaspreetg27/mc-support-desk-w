"""Label Pydantic schemas."""

import uuid
from typing import Optional

from pydantic import Field

from .common import BaseSchema, TimestampSchema, UUIDSchema


class LabelBase(BaseSchema):
    """Base label schema."""

    name: str = Field(..., min_length=1, max_length=64, description="Label name")
    description: Optional[str] = Field(None, max_length=255, description="Label description")


class LabelCreate(LabelBase):
    """Schema for creating a label."""

    tenant_id: uuid.UUID = Field(..., description="Tenant ID")


class LabelUpdate(BaseSchema):
    """Schema for updating a label."""

    name: Optional[str] = Field(None, min_length=1, max_length=64, description="Label name")
    description: Optional[str] = Field(None, max_length=255, description="Label description")


class LabelResponse(LabelBase, UUIDSchema, TimestampSchema):
    """Schema for label responses."""

    tenant_id: uuid.UUID


class LabelSummary(UUIDSchema):
    """Minimal label schema for references."""

    name: str
