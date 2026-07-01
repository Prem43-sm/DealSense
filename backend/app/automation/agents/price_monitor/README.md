# Price Monitor Agent

Monitors active marketplace mappings for DealSense master products, fetches latest source prices, compares them with current stored prices, writes price history only for changed values, and reuses the existing deal service for price drops.

## Scope

This worker only monitors prices. It does not discover products, create affiliate links, generate AI content, write product descriptions, scrape websites, or update availability.

## Workflow

```text
Manual API or future scheduler
  -> PriceMonitorAgent
  -> PriceMonitorService
  -> product_sources
  -> ConnectorManager
  -> marketplace connectors
  -> Price normalizer
  -> Price comparator
  -> Price updater
  -> History writer
  -> Existing deal service
```

## Manual Run

```text
GET /automation/price-monitor/run
```

The endpoint returns:

```json
{
  "status": "success",
  "summary": {
    "products_checked": 10,
    "prices_updated": 3,
    "unchanged": 7,
    "failed": 0
  }
}
```

## Price Source Interface

`sources.py` defines a connector-backed `PriceSource` adapter with:

- `start_run()`
- `fetch_price(product_source)`
- `finish_run()`

Marketplace connectors return standardized `PriceData`, which the adapter converts into `SourcePrice`. Future providers should keep returning the common connector models.

## Comparison Process

`price_comparator.py` compares the current database price with the normalized source price and returns:

- whether the price changed
- old price
- new price
- absolute difference
- percentage change

## History Writing

`history_writer.py` inserts a `price_history` row only when the price changed or a monitored store receives its first current price. Repeated runs with unchanged prices do not create duplicate history entries.

## Deal Recalculation

When a product has an existing old price and the new price is lower, the monitor calls `create_deal_if_discounted()` from the existing deal service. No new deal engine is implemented here.

## Future Roadmap

- Amazon PA API source
- Flipkart Affiliate API source
- Cuelinks source
- JSON feed source
- CSV feed source
- Marketplace-specific rate limits and retry policies
