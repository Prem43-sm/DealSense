from app.connectors.providers.mock_base import BaseMockConnector
from app.connectors.providers.reliance.config import DISPLAY_NAME, EXTERNAL_PREFIX, PRICE_OFFSET, PROVIDER_NAME


class MockConnector(BaseMockConnector):
    provider_name = PROVIDER_NAME
    display_name = DISPLAY_NAME
    external_prefix = EXTERNAL_PREFIX
    price_offset = PRICE_OFFSET

