# Competitor Data Schema

## Location

`marketing-plugin/data/competitor-data.json` — single source of truth for competitor Meta ad intelligence.

## Top-Level Structure

```json
{
  "last_scrape": "ISO 8601 timestamp of last Apify scrape",
  "scrape_status": "scraped | partial | error | pending",
  "watchlist": [ ... ],
  "ads": [ ... ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| last_scrape | Yes | Timestamp of the most recent successful scrape (null if never scraped) |
| scrape_status | Yes | `scraped` = all competitors pulled, `partial` = some failed, `error` = scrape failed, `pending` = never scraped |
| watchlist | Yes | Array of competitor Facebook Pages being tracked |
| ads | Yes | Array of all competitor ads discovered |

## Watchlist

```json
{
  "page_id": "string — Facebook Page ID",
  "page_name": "string — competitor display name",
  "category": "direct | indirect | aspirational",
  "added_at": "ISO 8601",
  "last_scraped": "ISO 8601 | null"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| page_id | Yes | Facebook Page ID (dedup key) — found via Meta Ad Library URL |
| page_name | Yes | Human-readable competitor name |
| category | No | `direct` = same market, `indirect` = adjacent, `aspirational` = larger player to learn from |
| added_at | Yes | When this competitor was added to the watchlist |
| last_scraped | No | Timestamp of last successful scrape for this competitor (null if never scraped) |

## Ads

```json
{
  "ad_id": "string — Meta Ad Library ID (dedup key)",
  "page_id": "string — FK to watchlist.page_id",
  "page_name": "string — competitor name",
  "ad_copy": "string — primary text / body",
  "headline": "string | null",
  "description": "string | null",
  "cta_type": "string — LEARN_MORE, SIGN_UP, SHOP_NOW, etc.",
  "creative_url": "string — URL to image or video asset",
  "creative_type": "image | video | carousel",
  "landing_page_url": "string | null — destination URL",
  "platforms": ["facebook", "instagram"],
  "started_running": "YYYY-MM-DD | null — Meta's reported start date",
  "first_seen": "YYYY-MM-DD — first scrape that found this ad",
  "last_seen": "YYYY-MM-DD — most recent scrape that found this ad",
  "days_active": 0,
  "status": "new | testing | winner | super_winner | stopped",
  "local_path": "string | null — path to downloaded asset",
  "analysis": null
}
```

| Field | Required | Description |
|-------|----------|-------------|
| ad_id | Yes | Meta Ad Library ID — unique across all ads. **Dedup key.** |
| page_id | Yes | Foreign key to the competitor watchlist entry |
| page_name | Yes | Denormalized competitor name for quick display |
| ad_copy | Yes | The primary text body of the ad |
| headline | No | Ad headline (may not exist for all ad types) |
| description | No | Link description text |
| cta_type | No | Call-to-action button type |
| creative_url | No | URL to the image or video creative on Meta's servers |
| creative_type | Yes | Type of creative asset |
| landing_page_url | No | Where the ad sends traffic |
| platforms | No | Which Meta platforms the ad runs on |
| started_running | No | Meta's reported start date (may differ from first_seen) |
| first_seen | Yes | Date our scraper first discovered this ad |
| last_seen | Yes | Date of most recent scrape that still returned this ad |
| days_active | Yes | Calculated: last_seen - first_seen (in days) |
| status | Yes | Derived from days_active (see Status Rules below) |
| local_path | No | Relative path to downloaded creative file (null until downloaded) |
| analysis | No | Structured analysis object (null until analysed) |

## Status Rules

Status is derived from `days_active` and recency of `last_seen`:

| Status | Rule |
|--------|------|
| `new` | days_active < 7 |
| `testing` | days_active 7–29 |
| `winner` | days_active 30–59 |
| `super_winner` | days_active 60+ |
| `stopped` | last_seen is more than 7 days ago |

## Analysis Object

Populated by Gemini Pro vision analysis of the downloaded creative:

```json
{
  "hook_type": "question | statistic | story | pain-point | testimonial | curiosity | shock",
  "angle": "string — the persuasion angle being used",
  "offer_description": "string — what's being offered",
  "visual_style": "UGC | polished | text-overlay | lifestyle | before-after | talking-head | animation",
  "cta_text": "string — the actual CTA text shown",
  "emotional_trigger": "fear | aspiration | curiosity | urgency | social-proof | authority",
  "target_audience_guess": "string — estimated target audience",
  "unique_elements": "string — what makes this creative stand out",
  "analysed_at": "ISO 8601"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| hook_type | Yes | Category of opening hook |
| angle | Yes | The persuasion strategy |
| offer_description | Yes | What the ad is offering |
| visual_style | Yes | Creative format/style category |
| cta_text | No | Specific call-to-action text visible in the creative |
| emotional_trigger | Yes | Primary emotional lever |
| target_audience_guess | No | Best estimate of intended audience |
| unique_elements | No | Notable or distinctive creative elements |
| analysed_at | Yes | When the analysis was performed |

## Relationships

```
Watchlist (1) ──→ (N) Ads
                       │
                       └── analysis (0..1)
```

- Each **Ad** belongs to one **Watchlist** competitor via `page_id`.
- Each **Ad** has at most one **Analysis** (populated after Gemini vision review).
- Downloaded assets are stored at `data/competitor-assets/{page_id}/{ad_id}.{ext}` and referenced via `local_path`.
