from app.automation.agents.availability_checker.status_normalizer import AvailabilityState, normalize_status
from app.connectors.manager import ConnectorManager
from app.models.product_source import ProductSource


class NormalizedAvailability:
    def __init__(self, *, provider: str, status: AvailabilityState, quantity: int | None) -> None:
        self.provider = provider
        self.status = status
        self.quantity = quantity


class AvailabilityChecker:
    def __init__(self, connector_manager: ConnectorManager | None = None) -> None:
        self.connector_manager = connector_manager or ConnectorManager()

    def check(self, product_source: ProductSource) -> NormalizedAvailability | None:
        connector = self.connector_manager.get_connector(product_source.source_name)
        if connector is None:
            return None

        availability = connector.get_availability(product_source.external_product_id)
        if availability is None:
            return None

        status = normalize_status(availability.status)
        if status is None:
            return None

        return NormalizedAvailability(
            provider=availability.provider,
            status=status,
            quantity=availability.quantity,
        )

