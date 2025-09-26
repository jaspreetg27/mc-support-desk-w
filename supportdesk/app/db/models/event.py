"""Event model."""

import uuid
from enum import Enum
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from ..base import Base, UUIDMixin


class EventType(str, Enum):
    ack_sent = "ack_sent"
    debounce_start = "debounce_start"
    debounce_end = "debounce_end"
    answer_sent = "answer_sent"
    clarify_sent = "clarify_sent"
    needs_review_created = "needs_review_created"
    urgent_flagged = "urgent_flagged"


class Event(Base, UUIDMixin):
    """Event audit log entries for threads."""

    __tablename__ = "events"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    thread_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("threads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    type: Mapped[EventType] = mapped_column(String(50), nullable=False)
    meta: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Single timestamp as per spec
    ts: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    tenant = relationship("Tenant", lazy="select")
    thread = relationship("Thread", lazy="select")

    def __repr__(self) -> str:
        return f"<Event(id={self.id}, type={self.type}, thread_id={self.thread_id})>"
