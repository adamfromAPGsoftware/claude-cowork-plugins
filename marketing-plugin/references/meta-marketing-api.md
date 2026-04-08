# Meta Marketing API Reference (Read-Only Subset)

## Authentication

Meta uses OAuth 2.0 with long-lived user access tokens:

1. **Obtain a short-lived token** — via the Meta Developer Tools page (`developers.facebook.com/tools/explorer`)
2. **Exchange for a long-lived token** — `GET /oauth/access_token?grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}&fb_exchange_token={short_lived_token}`
3. **Subsequent requests** — pass `access_token` as a query parameter

### Token Permissions

| Permission | Purpose |
|-----------|---------|
| `ads_read` | Read campaign structure (campaigns, ad sets, ads) |
| `read_insights` | Read performance metrics (impressions, clicks, spend, conversions) |

### Token Expiry

| Token Type | Lifespan |
|-----------|----------|
| Short-lived | ~1-2 hours |
| Long-lived | ~60 days |

Long-lived tokens must be refreshed before expiry. The pull script should check token validity before each sync and warn if expiry is within 7 days.

## Environment

| Environment | Base URL |
|-------------|----------|
| Production | `https://graph.facebook.com/v22.0` |

There is no sandbox environment for the Marketing API. Use a test ad account with minimal budget for development.

## Endpoints Used (GET only)

### 1. Discover Ad Accounts

```
GET /me/adaccounts
  ?fields=account_id,name,account_status,currency,timezone_name
```

Returns all ad accounts accessible to the authenticated user. Used on first run to auto-discover `meta_ad_account_id`.

**Fields:**

| Field | Description |
|-------|-------------|
| account_id | The ad account ID (format: `act_XXXXXXXXX`) |
| name | Human-readable account name |
| account_status | 1 = ACTIVE, 2 = DISABLED, 3 = UNSETTLED, etc. |
| currency | Account currency code (e.g. AUD) |
| timezone_name | Account timezone (e.g. Australia/Sydney) |

### 2. Campaigns

```
GET /{account_id}/campaigns
  ?fields=id,name,objective,status,daily_budget,lifetime_budget,created_time,updated_time
  &limit=100
```

Returns all campaigns in the ad account.

**Fields:**

| Field | Description |
|-------|-------------|
| id | Campaign ID |
| name | Campaign name |
| objective | CONVERSIONS, TRAFFIC, LEAD_GENERATION, BRAND_AWARENESS, etc. |
| status | ACTIVE, PAUSED, ARCHIVED, DELETED |
| daily_budget | Daily spend cap in account currency (in cents) |
| lifetime_budget | Total lifetime spend cap (in cents) |
| created_time | ISO 8601 creation timestamp |
| updated_time | ISO 8601 last modification timestamp |

### 3. Ad Sets

```
GET /{account_id}/adsets
  ?fields=id,campaign_id,name,status,targeting,optimization_goal,daily_budget,bid_strategy
  &limit=100
```

Returns all ad sets in the ad account.

**Fields:**

| Field | Description |
|-------|-------------|
| id | Ad set ID |
| campaign_id | Parent campaign ID |
| name | Ad set name |
| status | ACTIVE, PAUSED, ARCHIVED, DELETED |
| targeting | Targeting spec object (flatten to `targeting_summary` in marketing-data.json) |
| optimization_goal | LINK_CLICKS, CONVERSIONS, IMPRESSIONS, REACH, etc. |
| daily_budget | Ad-set-level daily budget in cents |
| bid_strategy | LOWEST_COST_WITHOUT_CAP, LOWEST_COST_WITH_BID_CAP, COST_CAP |

### 4. Ads

```
GET /{account_id}/ads
  ?fields=id,adset_id,campaign_id,name,status,creative{id}
  &limit=100
```

Returns all ads in the ad account.

**Fields:**

| Field | Description |
|-------|-------------|
| id | Ad ID |
| adset_id | Parent ad set ID |
| campaign_id | Parent campaign ID |
| name | Ad name |
| status | ACTIVE, PAUSED, ARCHIVED, DELETED |
| creative | Nested object containing `id` (the creative asset ID) |

### 5. Insights (Performance Metrics)

```
GET /{account_id}/insights
  ?fields=campaign_id,adset_id,ad_id,impressions,clicks,spend,cpc,cpm,ctr,reach,frequency,conversions,cost_per_action_type,actions
  &time_increment=1
  &date_preset=last_30d
  &level=ad
  &limit=500
```

Returns daily performance metrics. Use `time_increment=1` for day-by-day breakdown.

**Key parameters:**

| Parameter | Description |
|-----------|-------------|
| time_increment | `1` = daily, `7` = weekly, `monthly` = monthly |
| date_preset | `last_7d`, `last_30d`, `last_90d`, `this_month`, `last_month` |
| time_range | Alternative to date_preset: `{"since":"2026-01-01","until":"2026-03-31"}` |
| level | `campaign`, `adset`, or `ad` — granularity of the breakdown |

**Fields:**

| Field | Description |
|-------|-------------|
| impressions | Number of times ads were shown |
| clicks | Total clicks (all types) |
| spend | Amount spent in account currency |
| cpc | Cost per click |
| cpm | Cost per 1,000 impressions |
| ctr | Click-through rate (%) |
| reach | Unique users who saw the ad |
| frequency | Average impressions per unique user |
| conversions | Total conversion actions (derived from `actions` array) |
| cost_per_action_type | Cost per action broken down by type |
| actions | Array of `{ action_type, value }` — e.g. link_click, landing_page_view, lead, purchase |

## Pagination

Meta uses cursor-based pagination:

```json
{
  "data": [ ... ],
  "paging": {
    "cursors": {
      "before": "...",
      "after": "..."
    },
    "next": "https://graph.facebook.com/v22.0/..."
  }
}
```

To fetch the next page, append `&after={paging.cursors.after}` to the request. Continue until `paging.next` is absent from the response.

## Rate Limits

| Tier | Approximate Limit |
|------|-------------------|
| Development | ~200 calls/hour |
| Standard | ~200 calls/hour (shared across app users) |

Meta returns HTTP 429 when rate-limited. The pull script should implement exponential backoff and respect the `x-business-use-case-usage` header.

## Safety

**This integration is read-only.** The following are NEVER called:

- POST to create campaigns, ad sets, or ads
- POST to modify budgets, bids, or targeting
- DELETE to remove any ad objects
- Any write operation to the Meta Marketing API

The access token should only be granted `ads_read` and `read_insights` permissions. No write permissions are requested or used.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `META_ACCESS_TOKEN` | Long-lived user access token |
| `META_AD_ACCOUNT_ID` | Override for ad account ID (optional — auto-discovered if not set) |
| `META_APP_ID` | Meta app ID (for token exchange) |
| `META_APP_SECRET` | Meta app secret (for token exchange) |
