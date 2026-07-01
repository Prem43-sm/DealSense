import re

from pydantic import BaseModel, ConfigDict

from app.services.price_service import slugify


class IncomingMarketplaceProduct(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str
    brand: str | None = None
    category: str | None = None
    description: str | None = None
    image_url: str | None = None
    source_name: str
    external_product_id: str
    product_url: str | None = None
    canonical_url: str | None = None


class NormalizedMarketplaceProduct(BaseModel):
    title: str
    brand: str | None = None
    category: str | None = None
    description: str | None = None
    image_url: str | None = None
    slug: str
    normalized_title: str
    source_name: str
    external_product_id: str
    product_url: str | None = None
    canonical_url: str | None = None


def normalize_text(value: str | None) -> str | None:
    if value is None:
        return None
    collapsed = " ".join(value.strip().split())
    return collapsed.title() if collapsed else None


def normalize_for_match(value: str) -> str:
    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", " ", normalized)
    return " ".join(normalized.split())


def normalize_marketplace_product(product: IncomingMarketplaceProduct) -> NormalizedMarketplaceProduct:
    title = normalize_text(product.title) or product.title.strip()
    brand = normalize_text(product.brand)
    category = normalize_text(product.category)
    source_name = normalize_text(product.source_name) or product.source_name.strip()
    return NormalizedMarketplaceProduct(
        title=title,
        brand=brand,
        category=category,
        description=" ".join((product.description or "").strip().split()) or None,
        image_url=(product.image_url or "").strip() or None,
        slug=slugify(title),
        normalized_title=normalize_for_match(title),
        source_name=source_name,
        external_product_id=product.external_product_id.strip(),
        product_url=(product.product_url or "").strip() or None,
        canonical_url=(product.canonical_url or product.product_url or "").strip() or None,
    )

