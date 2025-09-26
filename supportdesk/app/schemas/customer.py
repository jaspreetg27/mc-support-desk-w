"""Customer Pydantic schemas."""

import uuid
from typing import Optional

from pydantic import EmailStr, Field

from .common import BaseSchema, TimestampSchema, UUIDSchema


class CustomerBase(BaseSchema):
    """Base customer schema."""

    platform: str = Field(..., min_length=1, max_length=50, description="Platform identifier")
    platform_user_id: str = Field(..., min_length=1, max_length=255, description="Platform user ID")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    email: Optional[EmailStr] = Field(None, description="Email address")


class CustomerCreate(CustomerBase):
    """Schema for creating a customer."""

    tenant_id: uuid.UUID = Field(..., description="Tenant ID")


class CustomerUpdate(BaseSchema):
    """Schema for updating a customer."""

    phone: Optional[str] = Field(None, max_length=20, description="Phone number")
    email: Optional[EmailStr] = Field(None, description="Email address")


class CustomerResponse(CustomerBase, UUIDSchema, TimestampSchema):
    """Schema for customer responses."""

    tenant_id: uuid.UUID


class CustomerSummary(UUIDSchema):
    """Minimal customer schema for references."""

    platform: str
    platform_user_id: str
