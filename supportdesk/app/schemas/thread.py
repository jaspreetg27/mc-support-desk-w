"""Thread Pydantic schemas."""

import uuid
from typing import List, Optional

from pydantic import Field

from ..db.models.thread import ThreadChannel, ThreadStatus
from .common import BaseSchema, TimestampSchema, UUIDSchema
from .customer import CustomerSummary


class ThreadBase(BaseSchema):
    """Base thread schema."""

    channel: ThreadChannel = Field(..., description="Communication channel")
    platform_thread_id: str = Field(..., min_length=1, max_length=255, description="Platform thread ID")
    status: ThreadStatus = Field(default=ThreadStatus.open, description="Thread status")
    labels: List[str] = Field(default_factory=list, description="Thread labels")


class ThreadCreate(ThreadBase):
    """Schema for creating a thread."""

    tenant_id: uuid.UUID = Field(..., description="Tenant ID")
    customer_id: Optional[uuid.UUID] = Field(None, description="Customer ID")


class ThreadUpdate(BaseSchema):
    """Schema for updating a thread."""

    status: Optional[ThreadStatus] = Field(None, description="Thread status")
    labels: Optional[List[str]] = Field(None, description="Thread labels")


class ThreadResponse(ThreadBase, UUIDSchema, TimestampSchema):
    """Schema for thread responses."""

    tenant_id: uuid.UUID
    customer_id: Optional[uuid.UUID]
    customer: Optional[CustomerSummary] = None


class ThreadSummary(UUIDSchema):
    """Minimal thread schema for references."""

    channel: ThreadChannel
    platform_thread_id: str
    status: ThreadStatus
