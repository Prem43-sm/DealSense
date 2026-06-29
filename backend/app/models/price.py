from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Price(Base):
    __tablename__ = "prices"
    __table_args__ = (UniqueConstraint("product_id", "store_id", name="uq_prices_product_store"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, index=True)
    current_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    availability: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    affiliate_url: Mapped[str] = mapped_column(Text, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    product = relationship("Product", back_populates="prices")
    store = relationship("Store", back_populates="prices")
