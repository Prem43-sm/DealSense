# Marketplace Connector Framework

Connectors are the single integration point for marketplace data. Product Discovery and Price Monitor should depend on `ConnectorManager`, not provider-specific imports.

## Structure

```text
connectors/
  base_connector.py
  manager.py
  models.py
  providers/
    amazon/
    flipkart/
    cuelinks/
    croma/
    reliance/
    ajio/
```

## Interface

Every connector implements:

- `discover_products()`
- `get_product(external_product_id)`
- `get_prices(external_product_id)`
- `get_availability(external_product_id)`
- `generate_affiliate_url(product_url)`
- `health_check()`

## Standard Models

All providers return Pydantic models from `models.py`: `ProductData`, `PriceData`, `AvailabilityData`, and `AffiliateLinkData`.

## Adding A Provider

Create `providers/<provider>/connector.py`, subclass `BaseConnector`, and expose a connector class. `ConnectorManager` discovers it automatically.

Real providers can later call Amazon PA API, Flipkart Affiliate API, Cuelinks, EarnKaro, Croma, Reliance Digital, AJIO, or other marketplaces without changing automation agents.
