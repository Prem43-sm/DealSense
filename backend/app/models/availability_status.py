from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class AvailabilityStatus(Base):
    __tablename__ = "availability_status"
    __table_args__ = (
        UniqueConstraint(
            "product_source_id",
            "provider",
            name="uq_availability_status_source_provider",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_source_id: Mapped[int] = mapped_column(
        ForeignKey("product_sources.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    provider: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    quantity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    last_checked: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_changed: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    product_source = relationship("ProductSource", back_populates="availability_statuses")
