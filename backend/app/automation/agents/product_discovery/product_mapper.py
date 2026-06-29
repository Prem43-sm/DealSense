from app.automation.agents.product_discovery.normalizer import NormalizedProduct
from app.models.product import Product


def map_to_product(product: NormalizedProduct) -> Product:
    return Product(
        title=product.title,
        slug=product.slug,
        brand=product.brand,
        category=product.category,
        image_url=product.image_url,
        description=product.description,
    )

