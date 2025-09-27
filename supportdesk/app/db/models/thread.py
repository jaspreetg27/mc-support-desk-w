"""Thread model."""

import uuid
from enum import Enum
from typing import List, Optional

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, TimestampMixin, UUIDMixin


class ThreadChannel(str, Enum):
    wa = "wa"
    ig = "ig"
    fb = "fb"


class ThreadStatus(str, Enum):
    open = "open"
    paused = "paused"
    closed = "closed"


class Thread(Base, UUIDMixin, TimestampMixin):
    """Conversation thread."""

    __tablename__ = "threads"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    channel: Mapped[ThreadChannel] = mapped_column(String(10), nullable=False)
    platform_thread_id: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    status: Mapped[ThreadStatus] = mapped_column(String(10), default=ThreadStatus.open, nullable=False)
    labels: Mapped[Optional[List[str]]] = mapped_column(JSON, default=list)

    # Relationships
    tenant = relationship("Tenant", lazy="select")
    customer = relationship("Customer", lazy="select")

    __table_args__ = (
        UniqueConstraint("tenant_id", "channel", "platform_thread_id", name="uq_thread_platform"),
    )

    def __repr__(self) -> str:
        return f"<Thread(id={self.id}, channel={self.channel}, status={self.status})>"
