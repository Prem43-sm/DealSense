# Product Identity System

The identity system keeps one DealSense master product while mapping marketplace listings to that product.

## Architecture

```text
Marketplace Product
  -> normalizer.py
  -> matcher.py
  -> mapper.py
  -> product_sources
       |
       +-- products
       +-- prices
       +-- price_history
       +-- deals
```

## Master Product

The existing `products` table remains the master product table. Product pages, search, prices, price history, and deals continue to reference the master product.

## Marketplace Mapping

The new `product_sources` table stores marketplace identity:

- `product_id`
- `source_name`
- `external_product_id`
- `product_url`
- `canonical_url`
- `last_seen`
- `active`

The unique constraint on `(source_name, external_product_id)` prevents the same marketplace listing from being mapped twice.

## Matching Rules

Incoming products are matched in this order:

1. Existing external mapping
2. Exact slug
3. Normalized title
4. Brand plus title similarity
5. Create new master product

## Mapping Flow

```text
Normalize incoming marketplace product
  -> find existing master
  -> attach mapping when found
  -> create master product when not found
  -> create or refresh marketplace mapping
```

## Future API Integrations

Amazon PA API, Flipkart Affiliate API, Cuelinks, Croma, Reliance Digital, AJIO, and other providers can pass their marketplace identifiers into `IdentityMappingService.map_product()` without changing the identity layer.

## Future AI Matching

AI matching can be added after rule-based matching as a confidence-scored fallback. It should never bypass the exact external mapping rule or the unique database constraint.

