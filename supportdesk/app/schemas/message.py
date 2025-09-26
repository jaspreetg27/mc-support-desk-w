"""Message Pydantic schemas."""

import uuid
from typing import Any, Dict, Optional

from pydantic import Field

from ..db.models.message import MessageDirection
from .common import BaseSchema, TimestampSchema, UUIDSchema
from .thread import ThreadSummary


class MessageBase(BaseSchema):
    """Base message schema."""

    direction: MessageDirection = Field(..., description="Message direction")
    text: Optional[str] = Field(None, description="Message text content")
    media: Optional[Dict[str, Any]] = Field(None, description="Media attachments")
    language: Optional[str] = Field(None, max_length=10, description="Detected language code")


class MessageCreate(MessageBase):
    """Schema for creating a message."""

    tenant_id: uuid.UUID = Field(..., description="Tenant ID")
    thread_id: uuid.UUID = Field(..., description="Thread ID")
    platform_message_id: Optional[str] = Field(None, max_length=255, description="Platform message ID")


class MessageUpdate(BaseSchema):
    """Schema for updating a message."""

    text: Optional[str] = Field(None, description="Message text content")
    language: Optional[str] = Field(None, max_length=10, description="Detected language code")


class MessageResponse(MessageBase, UUIDSchema, TimestampSchema):
    """Schema for message responses."""

    tenant_id: uuid.UUID
    thread_id: uuid.UUID
    platform_message_id: Optional[str]
    thread: Optional[ThreadSummary] = None


class MessageSummary(UUIDSchema):
    """Minimal message schema for references."""

    direction: MessageDirection
    text: Optional[str]
