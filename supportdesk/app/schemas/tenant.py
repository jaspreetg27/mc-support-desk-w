"""Tenant Pydantic schemas."""

import uuid
from typing import Optional

from pydantic import Field

from .common import BaseSchema, TimestampSchema, UUIDSchema


class TenantBase(BaseSchema):
    """Base tenant schema."""

    name: str = Field(..., min_length=1, max_length=255, description="Tenant name")


class TenantCreate(TenantBase):
    """Schema for creating a tenant."""

    pass


class TenantUpdate(BaseSchema):
    """Schema for updating a tenant."""

    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Tenant name")


class TenantResponse(TenantBase, UUIDSchema, TimestampSchema):
    """Schema for tenant responses."""

    pass


class TenantSummary(UUIDSchema):
    """Minimal tenant schema for references."""

    name: str
