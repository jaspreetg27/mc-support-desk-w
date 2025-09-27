"""Message model."""

import uuid
from enum import Enum
from typing import Optional

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, TimestampMixin, UUIDMixin


class MessageDirection(str, Enum):
    inbound = "inbound"
    outbound = "outbound"


class Message(Base, UUIDMixin, TimestampMixin):
    """Message entity for threads."""

    __tablename__ = "messages"

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
    # platform used is deduced via thread.channel; still need uniqueness on platform_message_id per tenant+thread platform
    platform_message_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    direction: Mapped[MessageDirection] = mapped_column(String(10), nullable=False)
    text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    media: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    language: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # Relationships
    tenant = relationship("Tenant", lazy="select")
    thread = relationship("Thread", lazy="select")

    __table_args__ = (
        # Uniqueness per tenant + platform_message_id; platform uniqueness is implied by source systems
        UniqueConstraint("tenant_id", "platform_message_id", name="uq_message_platform_msg_per_tenant"),
    )

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, direction={self.direction}, thread_id={self.thread_id})>"
