from pydantic import BaseModel, ConfigDict

from app.connectors.manager import ConnectorManager


class SourceProduct(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None
    brand: str | None
    category: str | None
    description: str | None = None
    image_url: str | None = None
    external_id: str | None = None
    store: str | None = None
    url: str | None = None


class ProductSource:
    name: str

    def fetch_products(self) -> list[SourceProduct]:
        raise NotImplementedError


class ConnectorProductSource(ProductSource):
    name = "Connector Manager"

    def __init__(self, connector_manager: ConnectorManager | None = None) -> None:
        self.connector_manager = connector_manager or ConnectorManager()

    def fetch_products(self) -> list[SourceProduct]:
        products: list[SourceProduct] = []
        for connector in self.connector_manager.all_connectors():
            for product in connector.discover_products():
                products.append(
                    SourceProduct(
                        title=product.title,
                        brand=product.brand,
                        category=product.category,
                        description=product.description,
                        image_url=product.image_url,
                        external_id=product.external_id,
                        store=product.provider,
                        url=product.product_url,
                    )
                )
        return products


def get_product_sources() -> list[ProductSource]:
    return [ConnectorProductSource()]

