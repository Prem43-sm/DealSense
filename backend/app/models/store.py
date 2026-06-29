from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    prices = relationship("Price", back_populates="store", cascade="all, delete-orphan")
    price_history = relationship("PriceHistory", back_populates="store", cascade="all, delete-orphan")
