# Marketing Data Schema — Quick Reference

## Location

`marketing/marketing-data.json`

## Key Fields for Analysis

### Campaigns

| Field | Description |
|-------|-------------|
| `campaign_id` | Unique campaign identifier (dedup key) |
| `name` | Human-readable campaign name |
| `objective` | CONVERSIONS, TRAFFIC, LEAD_GENERATION, etc. |
| `status` | ACTIVE, PAUSED, ARCHIVED, DELETED |
| `daily_budget` | Daily spend cap |
| `currency` | 3-letter currency code (e.g., AUD) |

### Ad Sets

| Field | Description |
|-------|-------------|
| `ad_set_id` | Unique ad set identifier |
| `campaign_id` | Parent campaign (FK) |
| `name` | Ad set name |
| `targeting_summary` | Human-readable targeting description |
| `optimization_goal` | LINK_CLICKS, CONVERSIONS, IMPRESSIONS, etc. |

### Insights (Daily Metrics)

| Field | Description |
|-------|-------------|
| `entity_type` | `campaign`, `ad_set`, or `ad` |
| `entity_id` | ID of the campaign, ad set, or ad |
| `date` | YYYY-MM-DD |
| `impressions` | Times the ad was shown |
| `clicks` | Total clicks (all types) |
| `spend` | Amount spent that day |
| `cpc` | Cost per click |
| `cpm` | Cost per 1,000 impressions |
| `ctr` | Click-through rate (%) |
| `conversions` | Total conversion events |
| `cost_per_conversion` | spend / conversions |
| `roas` | Return on ad spend |
| `actions[]` | Breakdown by action type (link_click, lead, purchase, etc.) |

## Relationships

```
Campaign (1) → (N) Ad Set (1) → (N) Ad
    │                    │                 │
    └── insights[]       └── insights[]    └── insights[]
```

**Do not double-count:** Campaign-level insights already aggregate child ad sets and ads.

## Dedup Key

Insights: `entity_type` + `entity_id` + `date`
