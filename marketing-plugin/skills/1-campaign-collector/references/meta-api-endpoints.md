# Meta Marketing API Endpoints — Campaign Collector

## Base URL

```
https://graph.facebook.com/v22.0
```

## Authentication

All requests include the access token as a query parameter or header:
```
?access_token={META_ACCESS_TOKEN}
```

Required permissions: `ads_read`, `ads_management` (read-only usage only)

## Endpoints Used

### 1. Discover Ad Accounts
```
GET /me/adaccounts
Fields: account_id, name, account_status, currency, business_name, amount_spent
Response:
  {
    "data": [
      {
        "account_id": "123456789",
        "id": "act_123456789",
        "name": "Main",
        "account_status": 1,
        "currency": "AUD",
        "business_name": "{YOUR_COMPANY_LEGAL}",
        "amount_spent": "50000"
      }
    ],
    "paging": { "cursors": { "before": "...", "after": "..." }, "next": "..." }
  }
```

Account status codes: 1 = ACTIVE, 2 = DISABLED, 3 = UNSETTLED, 7 = PENDING_RISK_REVIEW, 101 = CLOSED

### 2. Campaigns
```
GET /{ad_account_id}/campaigns
Fields: id, name, objective, status, daily_budget, lifetime_budget, start_time, stop_time, created_time, updated_time
Response:
  {
    "data": [
      {
        "id": "123456789",
        "name": "Brand Awareness - AU",
        "objective": "OUTCOME_AWARENESS",
        "status": "ACTIVE",
        "daily_budget": "5000",
        "start_time": "2026-01-01T00:00:00+0000",
        "created_time": "2025-12-15T10:30:00+0000"
      }
    ],
    "paging": { ... }
  }
```

### 3. Ad Sets
```
GET /{ad_account_id}/adsets
Fields: id, name, campaign_id, status, daily_budget, lifetime_budget, targeting, optimization_goal, billing_event, start_time, end_time, created_time
Response:
  {
    "data": [
      {
        "id": "234567890",
        "name": "AU 25-44 Interest",
        "campaign_id": "123456789",
        "status": "ACTIVE",
        "optimization_goal": "OFFSITE_CONVERSIONS",
        "billing_event": "IMPRESSIONS"
      }
    ],
    "paging": { ... }
  }
```

### 4. Ads
```
GET /{ad_account_id}/ads
Fields: id, name, adset_id, campaign_id, status, creative, created_time, updated_time
Response:
  {
    "data": [
      {
        "id": "345678901",
        "name": "Video Ad - Variant A",
        "adset_id": "234567890",
        "campaign_id": "123456789",
        "status": "ACTIVE"
      }
    ],
    "paging": { ... }
  }
```

### 5. Insights (Performance Metrics)
```
GET /{ad_account_id}/insights
Fields: campaign_id, campaign_name, adset_id, adset_name, ad_id, ad_name, impressions, clicks, spend, cpc, cpm, ctr, reach, frequency, conversions, cost_per_conversion, actions
Params:
  time_range: {"since": "2026-03-01", "until": "2026-03-31"}
  time_increment: 1 (daily breakdown)
  level: ad (or adset, campaign)
  limit: 500
Response:
  {
    "data": [
      {
        "campaign_id": "123456789",
        "campaign_name": "Brand Awareness - AU",
        "impressions": "15000",
        "clicks": "450",
        "spend": "75.50",
        "cpc": "0.168",
        "cpm": "5.033",
        "ctr": "3.0",
        "date_start": "2026-03-01",
        "date_stop": "2026-03-01"
      }
    ],
    "paging": { ... }
  }
```

## Pagination

All list endpoints use cursor-based pagination:
```json
{
  "paging": {
    "cursors": {
      "before": "abc123",
      "after": "def456"
    },
    "next": "https://graph.facebook.com/v22.0/..."
  }
}
```

Follow `paging.next` URL until it no longer appears.

## Rate Limits

- Business Use Case rate limiting: ~200 calls per hour per ad account
- If `error.code` is 17 or 32 → rate limited, back off and retry
- Use `limit` param to reduce number of API calls (fetch more per page)

## Safety Reminder

**These are the ONLY endpoints this skill uses. All are GET requests.**

Never call:
- POST endpoints (create campaigns, ads, etc.)
- DELETE endpoints
- Any endpoint that modifies ad account state
