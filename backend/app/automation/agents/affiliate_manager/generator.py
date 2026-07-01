from app.connectors.manager import ConnectorManager
from app.connectors.models import AffiliateLinkData
from app.models.product_source import ProductSource


class AffiliateGenerator:
    def __init__(self, connector_manager: ConnectorManager | None = None) -> None:
        self.connector_manager = connector_manager or ConnectorManager()

    def generate(self, product_source: ProductSource) -> AffiliateLinkData | None:
        connector = self.connector_manager.get_connector(product_source.source_name)
        if connector is None:
            return None

        product_url = product_source.product_url or product_source.canonical_url
        if not product_url:
            product = connector.get_product(product_source.external_product_id)
            product_url = product.product_url if product else None

        if not product_url:
            return None

        return connector.generate_affiliate_url(product_url)

    def regenerate(self, product_source: ProductSource) -> AffiliateLinkData | None:
        return self.generate(product_source)

    def bulk_generate(self, product_sources: list[ProductSource]) -> list[AffiliateLinkData]:
        links: list[AffiliateLinkData] = []
        for product_source in product_sources:
            link = self.generate(product_source)
            if link is not None:
                links.append(link)
        return links

