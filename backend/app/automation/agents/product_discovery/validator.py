from app.automation.agents.product_discovery.sources import SourceProduct


def validate_source_product(product: SourceProduct) -> bool:
    return bool(
        product.title
        and product.title.strip()
        and product.brand
        and product.brand.strip()
        and product.category
        and product.category.strip()
    )

