# Commerce Intelligence Engine

The analytics layer records anonymous product activity and turns it into daily product popularity signals.

## Data Model

```text
products
  id
  title
  ...
   |
   | 1:N
   v
product_analytics
  product_id
  date
  views
  searches
  affiliate_clicks
  wishlist_adds
  compare_adds
  detail_page_visits
  score
```

Each product gets at most one analytics row per day through the `(product_id, date)` unique constraint.

## Event Flow

```text
Frontend / backend event
  -> analytics API or service event function
  -> ProductAnalyticsRepository.get_or_create()
  -> increment metric
  -> recalculate score
  -> commit daily row
```

## Score Formula

Version 1 is a weighted sum:

```text
score =
  views * 1
  + detail_page_visits * 2
  + affiliate_clicks * 5
  + wishlist_adds * 4
  + compare_adds * 3
  + searches * 2
```

The formula lives in `scoring.py` so it can be tuned without changing event capture.

## APIs

- `GET /analytics/trending`
- `GET /analytics/popular`
- `GET /analytics/top-clicked`
- `GET /analytics/top-searches`
- `GET /analytics/dashboard`
- `POST /analytics/events/view`
- `POST /analytics/events/search`
- `POST /analytics/events/affiliate-click`
- `POST /analytics/events/compare`
- `POST /analytics/events/wishlist`
- `POST /analytics/events/detail-visit`

## Scheduler

`run_analytics_score_recalculation()` is a nightly job placeholder. It is intentionally not scheduled yet.

## Future Roadmap

- Replace homepage Trending Products with `GET /analytics/trending`.
- Add authenticated user segments.
- Add Redis/Celery buffering for high-volume events.
- Add AI recommendations using analytics, price history, identity mappings, and availability.
- Add bot filtering, deduplication windows, and rate limits before production traffic.
