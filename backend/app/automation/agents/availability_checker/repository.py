from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.availability_status import AvailabilityStatus
from app.models.product_source import ProductSource


class AvailabilityRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_product_sources(self) -> list[ProductSource]:
        return list(
            self.db.scalars(
                select(ProductSource)
                .where(ProductSource.active.is_(True))
                .options(selectinload(ProductSource.availability_statuses))
                .order_by(ProductSource.id)
            )
        )

    def get_status(self, product_source_id: int, provider: str) -> AvailabilityStatus | None:
        return self.db.scalar(
            select(AvailabilityStatus).where(
                AvailabilityStatus.product_source_id == product_source_id,
                AvailabilityStatus.provider == provider,
            )
        )

    def save_status(
        self,
        *,
        product_source_id: int,
        provider: str,
        status: str,
        quantity: int | None,
    ) -> tuple[AvailabilityStatus, bool]:
        now = datetime.now(UTC)
        current = self.get_status(product_source_id, provider)
        if current is None:
            current = AvailabilityStatus(
                product_source_id=product_source_id,
                provider=provider,
                status=status,
                quantity=quantity,
                last_checked=now,
                last_changed=now,
            )
            self.db.add(current)
            self.db.flush()
            return current, True

        changed = current.status != status
        current.status = status
        current.quantity = quantity
        current.last_checked = now
        if changed:
            current.last_changed = now
        self.db.flush()
        return current, changed

    def list_statuses(self) -> list[AvailabilityStatus]:
        return list(
            self.db.scalars(
                select(AvailabilityStatus)
                .options(selectinload(AvailabilityStatus.product_source))
                .order_by(AvailabilityStatus.id)
            )
        )

    def list_statuses_for_source(self, product_source_id: int) -> list[AvailabilityStatus]:
        return list(
            self.db.scalars(
                select(AvailabilityStatus)
                .where(AvailabilityStatus.product_source_id == product_source_id)
                .order_by(AvailabilityStatus.id)
            )
        )

