# Availability Checker Agent

Monitors stock status for active `ProductSource` mappings through marketplace connectors.

## Scope

This worker only checks availability. It does not discover products, update prices, generate affiliate links, or create content.

## Availability States

- `IN_STOCK`
- `LIMITED_STOCK`
- `PREORDER`
- `OUT_OF_STOCK`
- `DISCONTINUED`
- `UNKNOWN`

## Workflow

```text
AvailabilityCheckerAgent
  -> ProductSource mappings
  -> ConnectorManager
  -> connector.get_availability()
  -> status_normalizer.py
  -> AvailabilityRepository
  -> availability_status
```

## Manual Run

```text
GET /automation/availability/run
```

Response:

```json
{
  "status": "success",
  "summary": {
    "checked": 60,
    "updated": 12,
    "unchanged": 48,
    "failed": 0
  }
}
```

## API

- `GET /availability`
- `GET /availability/{product_source_id}`

## Normalization

Provider responses are normalized into the standard DealSense states. Unknown or invalid values are rejected by the checker and counted as failed.

## Future Roadmap

- Amazon PA API availability
- Flipkart stock feeds
- Croma, Reliance Digital, and AJIO status APIs
- Notification triggers when stock changes
