from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class AffiliateLink(Base):
    __tablename__ = "affiliate_links"
    __table_args__ = (
        UniqueConstraint(
            "product_source_id",
            "provider",
            name="uq_affiliate_links_source_provider",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_source_id: Mapped[int] = mapped_column(
        ForeignKey("product_sources.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    provider: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    affiliate_url: Mapped[str] = mapped_column(Text, nullable=False)
    short_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    tracking_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    last_generated: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_checked: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_valid: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    click_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    product_source = relationship("ProductSource", back_populates="affiliate_links")

