"""Event Pydantic schemas."""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import Field

from ..db.models.event import EventType
from .common import BaseSchema, UUIDSchema
from .thread import ThreadSummary


class EventBase(BaseSchema):
    """Base event schema."""

    type: EventType = Field(..., description="Event type")
    meta: Optional[Dict[str, Any]] = Field(None, description="Event metadata")


class EventCreate(EventBase):
    """Schema for creating an event."""

    tenant_id: uuid.UUID = Field(..., description="Tenant ID")
    thread_id: uuid.UUID = Field(..., description="Thread ID")


class EventResponse(EventBase, UUIDSchema):
    """Schema for event responses."""

    tenant_id: uuid.UUID
    thread_id: uuid.UUID
    ts: datetime = Field(..., description="Event timestamp")
    thread: Optional[ThreadSummary] = None


class EventSummary(UUIDSchema):
    """Minimal event schema for references."""

    type: EventType
    ts: datetime
