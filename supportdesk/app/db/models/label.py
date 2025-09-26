"""Label model for tagging and simple enums per tenant."""

import uuid

from sqlalchemy import String, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, TimestampMixin, UUIDMixin


class Label(Base, UUIDMixin, TimestampMixin):
    """Tenant-scoped label names for tagging threads/messages.

    This provides a canonical set of labels; threads may still store labels as
    JSONB array of strings for quick filtering, but this table allows UI-managed
    label vocabularies and future joins if needed.
    """

    __tablename__ = "labels"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    tenant = relationship("Tenant", lazy="select")

    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_label_name_per_tenant"),
    )

    def __repr__(self) -> str:
        return f"<Label(id={self.id}, name={self.name})>"
