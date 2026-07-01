from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.connectors.manager import ConnectorManager
from app.models.product_source import ProductSource as MarketplaceProductSource


class SourcePrice(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    product_id: int
    store: str
    price: Decimal
    currency: str = "INR"


class PriceSource:
    name: str

    def start_run(self) -> None:
        raise NotImplementedError

    def finish_run(self) -> None:
        raise NotImplementedError

    def fetch_price(self, product_source: MarketplaceProductSource) -> SourcePrice | None:
        raise NotImplementedError


class ConnectorPriceSource(PriceSource):
    name = "Connector Manager"

    def __init__(self, connector_manager: ConnectorManager | None = None) -> None:
        self.connector_manager = connector_manager or ConnectorManager()

    def start_run(self) -> None:
        return None

    def finish_run(self) -> None:
        return None

    def fetch_price(self, product_source: MarketplaceProductSource) -> SourcePrice | None:
        connector = self.connector_manager.get_connector(product_source.source_name)
        if connector is None:
            return None

        price = connector.get_prices(product_source.external_product_id)
        if price is None:
            return None

        return SourcePrice(
            product_id=product_source.product_id,
            store=product_source.source_name,
            price=price.price,
            currency=price.currency,
        )


def get_price_sources() -> list[PriceSource]:
    return [ConnectorPriceSource()]

