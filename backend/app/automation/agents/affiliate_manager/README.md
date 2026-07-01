# Affiliate Manager Agent

Generates, validates, and stores affiliate links for every active `ProductSource`.

## Scope

This worker manages affiliate links only. It does not discover products, monitor prices, check availability, or call real affiliate APIs yet.

## Workflow

```text
AffiliateManagerAgent
  -> ProductSource mappings
  -> ConnectorManager
  -> connector.generate_affiliate_url()
  -> AffiliateLinkValidator
  -> AffiliateLinkRepository
  -> affiliate_links
```

## Manual Run

```text
GET /automation/affiliate-manager/run
```

Response:

```json
{
  "status": "success",
  "summary": {
    "sources_checked": 60,
    "links_generated": 60,
    "duplicates": 0,
    "failed": 0
  }
}
```

## Affiliate Lifecycle

Each `ProductSource` can have one or more affiliate providers. The current framework creates one provider link per source using the matching marketplace connector. Re-running updates existing rows and does not create duplicates because of the `(product_source_id, provider)` unique constraint.

## Validation

`validator.py` checks that the URL exists, uses HTTPS, and looks related to the provider. Real HTTP validation can be added later.

## Future Roadmap

- Amazon Associates tag management
- Flipkart Affiliate tracking
- Cuelinks deep links
- EarnKaro, Admitad, and Impact adapters
- URL shortening
- Click analytics and scheduled validity checks
