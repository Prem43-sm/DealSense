import re

from pydantic import BaseModel

from app.automation.agents.product_discovery.sources import SourceProduct


class NormalizedProduct(BaseModel):
    title: str
    brand: str
    category: str
    slug: str
    description: str | None = None
    image_url: str | None = None
    external_id: str | None = None
    store: str | None = None
    url: str | None = None


def standardize_text(value: str) -> str:
    return " ".join(value.strip().split()).title()


def generate_slug(value: str) -> str:
    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    return normalized.strip("-")


def normalize_product(product: SourceProduct) -> NormalizedProduct:
    title = standardize_text(product.title or "")
    brand = standardize_text(product.brand or "")
    category = standardize_text(product.category or "")
    return NormalizedProduct(
        title=title,
        brand=brand,
        category=category,
        slug=generate_slug(title),
        description=" ".join((product.description or "").strip().split()) or None,
        image_url=(product.image_url or "").strip() or None,
        external_id=(product.external_id or "").strip() or None,
        store=(product.store or "").strip() or None,
        url=(product.url or "").strip() or None,
    )

