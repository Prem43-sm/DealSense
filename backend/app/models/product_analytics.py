from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class ProductAnalytics(Base):
    __tablename__ = "product_analytics"
    __table_args__ = (
        UniqueConstraint("product_id", "date", name="uq_product_analytics_product_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    views: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    searches: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    affiliate_clicks: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    wishlist_adds: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    compare_adds: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    detail_page_visits: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    product = relationship("Product", back_populates="analytics")
