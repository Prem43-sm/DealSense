# Product Discovery Agent

Discovers new products from configured product sources and inserts them into the existing DealSense product table.

## Scope

This worker only discovers products. It does not update prices, create affiliate links, generate AI descriptions, detect deals, scrape websites, or update availability.

## Workflow

```text
Scheduler or manual API
  -> ProductDiscoveryAgent
  -> ProductDiscoveryService
  -> ProductSource implementations
  -> Validator
  -> Normalizer
  -> DuplicateChecker
  -> ProductMapper
  -> Existing SQLAlchemy Product table
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

Create a class that implements `ProductSource` in `sources.py` or a dedicated source module. The source must return `SourceProduct` records with:

- `title`
- `brand`
- `category`
- `description`
- `image_url`
- `external_id`
- `store`
- `url`

No source should scrape pages in this phase. Future integrations should use official APIs or approved feeds.

## Validation

`validator.py` ignores products missing `title`, `brand`, or `category`.

## Normalization

`normalizer.py` trims whitespace, standardizes capitalization, and generates a URL-safe slug from the normalized title.

## Duplicate Detection

`duplicate_checker.py` checks the existing database for matching product title or slug. It also tracks duplicate `external_id` values within the current source batch because the current database schema intentionally has no `external_id` column.

## Future Roadmap

- Amazon PA API source
- Flipkart Affiliate API source
- Cuelinks feed source
- CSV and JSON feed sources
- Persistent external source identity if the product schema is extended later
