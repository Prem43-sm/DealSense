from abc import ABC, abstractmethod

from app.connectors.models import AffiliateLinkData, AvailabilityData, ConnectorHealth, PriceData, ProductData


class BaseConnector(ABC):
    provider_name: str
    display_name: str

    @abstractmethod
    def discover_products(self) -> list[ProductData]:
        raise NotImplementedError

    @abstractmethod
    def get_product(self, external_product_id: str) -> ProductData | None:
        raise NotImplementedError

    @abstractmethod
    def get_prices(self, external_product_id: str) -> PriceData | None:
        raise NotImplementedError

    @abstractmethod
    def get_availability(self, external_product_id: str) -> AvailabilityData | None:
        raise NotImplementedError

    @abstractmethod
    def generate_affiliate_url(self, product_url: str) -> AffiliateLinkData:
        raise NotImplementedError

    @abstractmethod
    def health_check(self) -> ConnectorHealth:
        raise NotImplementedError

