# Meta Marketing API — Campaign Creation (Write Endpoints)

This reference documents the Meta Marketing API write endpoints used by the Campaign Launcher for creating campaigns, uploading creatives, and managing ad status.

## Authentication

All requests require a valid `access_token` with `ads_management` permission.

```
Authorization: Bearer {META_ACCESS_TOKEN}
```

Or as query parameter: `?access_token={META_ACCESS_TOKEN}`

### Required Permissions

| Permission | Purpose |
|-----------|---------|
| `ads_management` | Create and manage campaigns, ad sets, ads, and creatives |
| `ads_read` | Read campaign structure and performance data |
| `pages_read_engagement` | Required for ad creative object_story_spec |

## Base URL

```
https://graph.facebook.com/v22.0
```

## Budget Format

**All budgets are in cents (minor currency units), not dollars.**

- $50/day = `daily_budget: 5000`
- $100/day = `daily_budget: 10000`

Always multiply dollar amounts by 100 before sending to the API.

---

## 1. Create Campaign

```
POST /{ad_account_id}/campaigns
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Campaign name |
| `objective` | enum | Yes | Campaign objective |
| `special_ad_categories` | array | Yes | Empty array `[]` unless housing/credit/employment |
| `status` | enum | Yes | Always `PAUSED` on creation |
| `buying_type` | string | No | Default `AUCTION` |

### Objectives

| Objective | Use Case |
|-----------|----------|
| `OUTCOME_LEADS` | Lead generation campaigns |
| `OUTCOME_TRAFFIC` | Drive traffic to landing page |
| `OUTCOME_AWARENESS` | Brand awareness |
| `OUTCOME_ENGAGEMENT` | Post engagement |
| `OUTCOME_SALES` | Conversions / purchases |

### Example Request

```json
{
  "name": "Go Enhance - Lead Gen - April 2026",
  "objective": "OUTCOME_LEADS",
  "special_ad_categories": [],
  "status": "PAUSED",
  "access_token": "{token}"
}
```

### Response

```json
{
  "id": "120212345678901234"
}
```

---

## 2. Create Ad Set

```
POST /{ad_account_id}/adsets
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `campaign_id` | string | Yes | Parent campaign ID |
| `name` | string | Yes | Ad set name |
| `targeting` | object | Yes | Targeting specification |
| `daily_budget` | integer | Yes* | Daily budget in cents |
| `lifetime_budget` | integer | Yes* | Lifetime budget in cents (*one of daily/lifetime required) |
| `optimization_goal` | enum | Yes | What to optimise for |
| `billing_event` | enum | Yes | Always `IMPRESSIONS` |
| `bid_strategy` | enum | No | Default `LOWEST_COST_WITHOUT_CAP` |
| `status` | enum | Yes | Always `PAUSED` on creation |
| `start_time` | datetime | No | ISO 8601 format |
| `end_time` | datetime | No | ISO 8601 format |

### Targeting Spec Format

```json
{
  "targeting": {
    "geo_locations": {
      "countries": ["AU"],
      "regions": [
        {"key": "3847", "name": "Queensland"},
        {"key": "3856", "name": "New South Wales"}
      ],
      "cities": [
        {"key": "2490299", "name": "Brisbane", "radius": 50, "distance_unit": "kilometer"}
      ]
    },
    "age_min": 25,
    "age_max": 55,
    "genders": [0],
    "flexible_spec": [
      {
        "interests": [
          {"id": "6003139266461", "name": "Small business"},
          {"id": "6003384248805", "name": "Entrepreneurship"}
        ]
      }
    ],
    "publisher_platforms": ["facebook", "instagram"],
    "facebook_positions": ["feed", "reels"],
    "instagram_positions": ["stream", "reels", "explore"]
  }
}
```

### Optimization Goals

| Goal | Use With Objective |
|------|--------------------|
| `LEAD_GENERATION` | OUTCOME_LEADS |
| `LINK_CLICKS` | OUTCOME_TRAFFIC |
| `IMPRESSIONS` | OUTCOME_AWARENESS |
| `OFFSITE_CONVERSIONS` | OUTCOME_SALES |

### Example Request

```json
{
  "campaign_id": "120212345678901234",
  "name": "Go Enhance - AU SMB Owners 25-55",
  "targeting": {
    "geo_locations": {"countries": ["AU"]},
    "age_min": 25,
    "age_max": 55,
    "flexible_spec": [{"interests": [{"id": "6003139266461", "name": "Small business"}]}],
    "publisher_platforms": ["facebook", "instagram"]
  },
  "daily_budget": 5000,
  "optimization_goal": "LEAD_GENERATION",
  "billing_event": "IMPRESSIONS",
  "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
  "status": "PAUSED",
  "access_token": "{token}"
}
```

### Response

```json
{
  "id": "120212345678905678"
}
```

---

## 3. Upload Ad Image

```
POST /{ad_account_id}/adimages
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `filename` | file | Yes | Image file (multipart/form-data) |

### Supported Formats

- PNG, JPG, GIF (non-animated)
- Max file size: 30MB
- Recommended: 1080x1080 (1:1), 1080x1920 (9:16), 1200x628 (1.91:1)

### Example Request

```bash
curl -F "filename=@/path/to/ad-image.png" \
  "https://graph.facebook.com/v22.0/{ad_account_id}/adimages?access_token={token}"
```

### Response

```json
{
  "images": {
    "ad-image.png": {
      "hash": "abc123def456...",
      "url": "https://scontent.xx.fbcdn.net/..."
    }
  }
}
```

---

## 4. Upload Ad Video

```
POST /{ad_account_id}/advideos
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source` | file | Yes | Video file (multipart/form-data) |
| `title` | string | No | Video title |

Video upload is **asynchronous**. Poll for completion:

```
GET /{video_id}?fields=status
```

Status values: `processing`, `ready`, `error`

### Supported Formats

- MP4, MOV
- Max file size: 4GB
- Max duration: 240 minutes
- Recommended: 1080x1080 (1:1), 1080x1920 (9:16)

---

## 5. Create Ad Creative

```
POST /{ad_account_id}/adcreatives
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Creative name |
| `object_story_spec` | object | Yes | Ad content specification |

### Image Ad Creative (object_story_spec)

```json
{
  "name": "Go Enhance - Drowning in Admin - 1:1",
  "object_story_spec": {
    "page_id": "{facebook_page_id}",
    "link_data": {
      "image_hash": "abc123def456...",
      "link": "https://go-enhance.com.au",
      "message": "Primary text — the main ad copy that appears above the image.",
      "name": "Headline — short, punchy, appears below the image.",
      "description": "Description — appears below the headline.",
      "call_to_action": {
        "type": "LEARN_MORE",
        "value": {
          "link": "https://go-enhance.com.au"
        }
      }
    }
  }
}
```

### Video Ad Creative (object_story_spec)

```json
{
  "name": "Go Enhance - Drowning in Admin - Video 9:16",
  "object_story_spec": {
    "page_id": "{facebook_page_id}",
    "video_data": {
      "video_id": "{video_id}",
      "image_hash": "abc123def456...",
      "message": "Primary text.",
      "title": "Headline.",
      "link_description": "Description.",
      "call_to_action": {
        "type": "LEARN_MORE",
        "value": {
          "link": "https://go-enhance.com.au"
        }
      }
    }
  }
}
```

### CTA Types

| Type | Display |
|------|---------|
| `LEARN_MORE` | Learn More |
| `SIGN_UP` | Sign Up |
| `GET_QUOTE` | Get Quote |
| `CONTACT_US` | Contact Us |
| `BOOK_NOW` | Book Now |
| `APPLY_NOW` | Apply Now |

### Response

```json
{
  "id": "120212345678909012"
}
```

---

## 6. Create Ad

```
POST /{ad_account_id}/ads
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `adset_id` | string | Yes | Parent ad set ID |
| `name` | string | Yes | Ad name |
| `creative` | object | Yes | `{"creative_id": "{creative_id}"}` |
| `status` | enum | Yes | Always `PAUSED` on creation |
| `tracking_specs` | array | No | Pixel/conversion tracking |

### Example Request

```json
{
  "adset_id": "120212345678905678",
  "name": "Go Enhance - Drowning in Admin - 1:1 - V1",
  "creative": {
    "creative_id": "120212345678909012"
  },
  "status": "PAUSED",
  "tracking_specs": [
    {
      "action.type": ["offsite_conversion"],
      "fb_pixel": ["{pixel_id}"]
    }
  ],
  "access_token": "{token}"
}
```

### Response

```json
{
  "id": "120212345678903456"
}
```

---

## 7. Update Ad Status (Pause / Activate)

```
POST /{ad_id}
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | enum | Yes | `PAUSED` or `ACTIVE` |

### Example — Pause an Ad

```json
{
  "status": "PAUSED",
  "access_token": "{token}"
}
```

### Example — Activate a Campaign (same endpoint pattern)

```
POST /{campaign_id}
POST /{adset_id}
POST /{ad_id}
```

Each entity must be activated individually: campaign, then ad sets, then ads.

---

## Rate Limits

| Limit | Value |
|-------|-------|
| Standard | 200 calls per hour per ad account |
| Batch | Up to 50 operations per batch request |
| Backoff | Exponential backoff on HTTP 429 |

### Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 1 | Unknown error | Retry with backoff |
| 2 | Temporary error | Retry after 5 minutes |
| 4 | Too many calls | Exponential backoff |
| 17 | Rate limit hit | Wait and retry |
| 100 | Invalid parameter | Check request payload |
| 190 | Invalid access token | Refresh token |
| 368 | Temporarily blocked | Wait 1-24 hours |
| 2615 | Ad account disabled | Contact Meta support |

### Batch Requests

For efficiency, multiple operations can be batched:

```
POST /
{
  "batch": [
    {"method": "POST", "relative_url": "{account_id}/campaigns", "body": "..."},
    {"method": "POST", "relative_url": "{account_id}/adsets", "body": "..."}
  ],
  "access_token": "{token}"
}
```

---

## Meta Conversions API (Server-Side Events)

Used by the lead capture webhook to send conversion events server-side.

```
POST /{pixel_id}/events
```

### Lead Event Payload

```json
{
  "data": [
    {
      "event_name": "Lead",
      "event_time": 1712448000,
      "event_source_url": "https://go-enhance.com.au",
      "action_source": "website",
      "user_data": {
        "em": ["SHA256 hash of lowercase email"],
        "ph": ["SHA256 hash of phone (E.164 format, no +)"],
        "client_ip_address": "203.0.113.1",
        "client_user_agent": "Mozilla/5.0...",
        "fbc": "{click_id from _fbc cookie}",
        "fbp": "{browser_id from _fbp cookie}"
      }
    }
  ],
  "access_token": "{token}"
}
```

### Hashing Requirements

- All PII fields must be SHA256 hashed before sending
- Email: lowercase, trim whitespace, then hash
- Phone: E.164 format without +, then hash (e.g., "61400000000")
- First/last name: lowercase, trim, then hash
