# Product Discovery Agent

Discovers new products from configured product sources and sends every incoming product through the identity layer.

## Scope

This worker only discovers products. It does not update prices, create affiliate links, generate AI descriptions, detect deals, scrape websites, or update availability.

## Workflow

```text
Scheduler or manual API
  -> ProductDiscoveryAgent
  -> ProductDiscoveryService
  -> ConnectorManager
  -> marketplace connectors
  -> Validator
  -> IdentityMappingService
  -> products
  -> product_sources
```

## Manual Run

```text
GET /automation/product-discovery/run
```

The endpoint returns:

```json
{
  "status": "success",
  "summary": {
    "fetched": 10,
    "inserted": 8,
    "duplicates": 2,
    "failed": 0
  }
}
```

## Adding New Sources

Create a marketplace connector under `backend/app/connectors/providers/<provider>/`. Product Discovery reads connector `ProductData` through `ConnectorManager` and adapts it to `SourceProduct` records with:

- `title`
- `brand`
- `category`
- `description`
- `image_url`
- `external_id`
- `store`
- `url`

No connector should scrape pages in this phase. Future integrations should use official APIs or approved feeds.

## Validation

`validator.py` ignores products missing `title`, `brand`, or `category`.

## Normalization

The identity layer trims whitespace, standardizes capitalization, and generates a URL-safe slug from the normalized title.

## Duplicate Detection

Product Discovery no longer inserts products directly. `IdentityMappingService` prevents duplicates through exact marketplace mappings, exact slug, normalized title, and brand plus title similarity.

## Future Roadmap

- Amazon PA API source
- Flipkart Affiliate API source
- Cuelinks feed source
- CSV and JSON feed sources
- Marketplace-specific source identifiers through `product_sources`
