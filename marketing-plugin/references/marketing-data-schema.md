# Marketing Data Schema

## Location

`marketing/marketing-data.json` — single source of truth for your marketing performance data.

## Top-Level Structure

```json
{
  "last_sync": "ISO 8601 timestamp of last Meta API pull",
  "meta_ad_account_id": "act_XXXXXXXXX — auto-discovered via /me/adaccounts",
  "sync_status": "synced | partial | error",
  "meta": { ... },
  "ga4": null,
  "funnel_links": []
}
```

| Field | Required | Description |
|-------|----------|-------------|
| last_sync | Yes | Timestamp of the most recent successful sync across all sources |
| meta_ad_account_id | Yes | The primary Meta ad account ID, auto-discovered on first pull |
| sync_status | Yes | `synced` = all data current, `partial` = some endpoints failed, `error` = sync failed entirely |
| meta | Yes | Meta Ads data (campaigns, ad sets, ads, insights) |
| ga4 | No | Google Analytics 4 data — reserved for Phase 2 |
| funnel_links | No | Funnel mapping entries linking ad clicks to conversions — reserved for Phase 2 |

## Meta Object

```json
{
  "last_sync": "ISO 8601 timestamp of last Meta-specific pull",
  "campaigns": [ ... ],
  "ad_sets": [ ... ],
  "ads": [ ... ],
  "insights": [ ... ]
}
```

### Campaigns

```json
{
  "campaign_id": "string — Meta campaign ID (dedup key)",
  "name": "string — campaign name",
  "objective": "string — CONVERSIONS, TRAFFIC, LEAD_GENERATION, etc.",
  "status": "ACTIVE | PAUSED | ARCHIVED | DELETED",
  "daily_budget": 0.00,
  "lifetime_budget": 0.00,
  "currency": "AUD",
  "created_time": "ISO 8601",
  "updated_time": "ISO 8601"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| campaign_id | Yes | Dedup key — prevents re-importing the same campaign |
| name | Yes | Human-readable campaign name |
| objective | Yes | Meta campaign objective type |
| status | Yes | Current campaign delivery status |
| daily_budget | No | Daily spend cap in minor units (0 if using lifetime budget) |
| lifetime_budget | No | Total lifetime spend cap (0 if using daily budget) |
| currency | Yes | 3-letter currency code |
| created_time | Yes | When the campaign was created in Meta |
| updated_time | Yes | Last modification timestamp |

### Ad Sets

```json
{
  "ad_set_id": "string — Meta ad set ID (dedup key)",
  "campaign_id": "string — parent campaign ID (FK → campaigns.campaign_id)",
  "name": "string — ad set name",
  "status": "ACTIVE | PAUSED | ARCHIVED | DELETED",
  "targeting_summary": "string — human-readable targeting description",
  "optimization_goal": "string — LINK_CLICKS, CONVERSIONS, IMPRESSIONS, etc.",
  "daily_budget": 0.00,
  "bid_strategy": "LOWEST_COST_WITHOUT_CAP | LOWEST_COST_WITH_BID_CAP | COST_CAP"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| ad_set_id | Yes | Dedup key — unique within account |
| campaign_id | Yes | Foreign key to parent campaign |
| name | Yes | Human-readable ad set name |
| status | Yes | Current delivery status |
| targeting_summary | No | Flattened targeting description (audiences, locations, demographics) |
| optimization_goal | Yes | What Meta optimizes delivery for |
| daily_budget | No | Ad-set-level daily budget (overrides campaign budget if set) |
| bid_strategy | No | Bid strategy controlling cost efficiency |

### Ads

```json
{
  "ad_id": "string — Meta ad ID (dedup key)",
  "ad_set_id": "string — parent ad set ID (FK → ad_sets.ad_set_id)",
  "campaign_id": "string — parent campaign ID (FK → campaigns.campaign_id)",
  "name": "string — ad name",
  "status": "ACTIVE | PAUSED | ARCHIVED | DELETED",
  "creative_id": "string — Meta creative asset ID"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| ad_id | Yes | Dedup key — unique within account |
| ad_set_id | Yes | Foreign key to parent ad set |
| campaign_id | Yes | Foreign key to parent campaign |
| name | Yes | Human-readable ad name |
| status | Yes | Current delivery status |
| creative_id | Yes | Reference to the creative asset used by this ad |

### Insights

Daily performance metrics. One entry per entity per day.

```json
{
  "entity_type": "campaign | ad_set | ad",
  "entity_id": "string — ID of the campaign, ad set, or ad",
  "date": "YYYY-MM-DD",
  "impressions": 0,
  "clicks": 0,
  "spend": 0.00,
  "currency": "AUD",
  "cpc": 0.00,
  "cpm": 0.00,
  "ctr": 0.00,
  "reach": 0,
  "frequency": 0.00,
  "conversions": 0,
  "cost_per_conversion": 0.00,
  "roas": 0.00,
  "actions": [
    {
      "action_type": "string — e.g. link_click, landing_page_view, lead, purchase",
      "value": 0
    }
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| entity_type | Yes | Which level this insight belongs to |
| entity_id | Yes | Foreign key to the relevant campaign, ad set, or ad |
| date | Yes | The calendar day this metric covers |
| impressions | Yes | Number of times the ad was shown |
| clicks | Yes | Total clicks (all types) |
| spend | Yes | Amount spent on this day in the account currency |
| currency | Yes | 3-letter currency code |
| cpc | No | Cost per click (spend / clicks) |
| cpm | No | Cost per 1,000 impressions |
| ctr | No | Click-through rate as a percentage |
| reach | No | Number of unique users who saw the ad |
| frequency | No | Average number of times each user saw the ad |
| conversions | No | Total conversion events |
| cost_per_conversion | No | spend / conversions |
| roas | No | Return on ad spend (conversion value / spend) |
| actions | No | Breakdown of specific action types and counts |

**Dedup key for insights:** composite of `entity_type` + `entity_id` + `date`. If a re-sync returns data for an existing day, the new record replaces the old one.

## Relationships

```
Campaign (1) ──→ (N) Ad Set (1) ──→ (N) Ad
    │                    │                 │
    └── insights[]       └── insights[]    └── insights[]
```

- Each **Ad Set** belongs to exactly one **Campaign** via `campaign_id`.
- Each **Ad** belongs to exactly one **Ad Set** via `ad_set_id` and one **Campaign** via `campaign_id`.
- **Insights** reference their parent entity via `entity_type` + `entity_id`.
- Campaign-level insights aggregate all child ad sets and ads. Do not double-count by summing campaign + ad set + ad insights.

## GA4 (Phase 2)

Reserved. Will hold Google Analytics 4 session and conversion data to connect ad clicks with on-site behavior.

## Funnel Links (Phase 2)

Reserved. Will map the journey from Meta ad click through landing page to conversion event, linking `meta.insights` entries to `ga4` sessions.
