from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.affiliate_link import AffiliateLink
from app.models.product_source import ProductSource


class AffiliateLinkRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_product_sources(self) -> list[ProductSource]:
        return list(
            self.db.scalars(
                select(ProductSource)
                .where(ProductSource.active.is_(True))
                .options(selectinload(ProductSource.affiliate_links))
                .order_by(ProductSource.id)
            )
        )

    def get_link(self, product_source_id: int, provider: str) -> AffiliateLink | None:
        return self.db.scalar(
            select(AffiliateLink).where(
                AffiliateLink.product_source_id == product_source_id,
                AffiliateLink.provider == provider,
            )
        )

    def save_link(
        self,
        *,
        product_source_id: int,
        provider: str,
        affiliate_url: str,
        status: str,
        tracking_id: str | None = None,
        short_url: str | None = None,
    ) -> tuple[AffiliateLink, bool]:
        now = datetime.now(UTC)
        link = self.get_link(product_source_id, provider)
        created = link is None
        if link is None:
            link = AffiliateLink(
                product_source_id=product_source_id,
                provider=provider,
                affiliate_url=affiliate_url,
                short_url=short_url,
                tracking_id=tracking_id,
                status=status,
                last_generated=now,
                last_checked=now,
                last_valid=now if status == "VALID" else None,
            )
            self.db.add(link)
            self.db.flush()
            return link, created

        link.affiliate_url = affiliate_url
        link.short_url = short_url
        link.tracking_id = tracking_id
        link.status = status
        link.last_generated = now
        link.last_checked = now
        if status == "VALID":
            link.last_valid = now
        self.db.flush()
        return link, created

    def list_links(self) -> list[AffiliateLink]:
        return list(
            self.db.scalars(
                select(AffiliateLink)
                .options(selectinload(AffiliateLink.product_source))
                .order_by(AffiliateLink.id)
            )
        )

    def list_links_for_source(self, product_source_id: int) -> list[AffiliateLink]:
        return list(
            self.db.scalars(
                select(AffiliateLink)
                .where(AffiliateLink.product_source_id == product_source_id)
                .order_by(AffiliateLink.id)
            )
        )

