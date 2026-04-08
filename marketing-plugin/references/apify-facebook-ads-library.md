# Apify Facebook Ads Scraper API Reference

## Overview

We use the Apify `apify/facebook-ads-scraper` actor to scrape competitor ads from Meta's Ad Library. This is necessary because Meta's official Ad Library API only returns commercial ads targeted to EU/UK — it does not serve Australian or US commercial ads via the API.

The Ad Library website (facebook.com/ads/library) shows all ads globally. Apify scrapes this public web UI.

## Actor Details

- **Actor ID:** `apify/facebook-ads-scraper`
- **API path:** `apify~facebook-ads-scraper` (tilde separator in URLs)
- **Marketplace:** https://apify.com/apify/facebook-ads-scraper
- **Pricing:** Pay-per-event, ~$5 per 1,000 results (varies by plan)

## REST API

### Start a Run

The actor takes `startUrls` — actual Meta Ad Library URLs. It does NOT use the old structured input (`searchType`, `pageIds`, etc.).

#### Keyword Search (discovery)

```
POST https://api.apify.com/v2/acts/apify~facebook-ads-scraper/runs?token={APIFY_API_TOKEN}
Content-Type: application/json

{
  "startUrls": [
    {"url": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&q=business%20automation&search_type=keyword_unordered"}
  ],
  "maxItems": 500
}
```

#### Page ID Search (watchlist scrape)

```
POST https://api.apify.com/v2/acts/apify~facebook-ads-scraper/runs?token={APIFY_API_TOKEN}
Content-Type: application/json

{
  "startUrls": [
    {"url": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&view_all_page_id=114251326619158&search_type=page"},
    {"url": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&view_all_page_id=174222572763185&search_type=page"}
  ],
  "maxItems": 500
}
```

### Input Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| startUrls | array | Array of `{"url": "..."}` objects with Meta Ad Library URLs |
| maxItems | int | Maximum ads to return (default 100). **Cost scales with this.** |

### Ad Library URL Parameters

These go in the `startUrls[].url` query string:

| Parameter | Values | Description |
|-----------|--------|-------------|
| active_status | `active`, `inactive`, `all` | Filter by ad status |
| ad_type | `all`, `political_and_issue_ads` | Type of ads |
| country | `AU`, `US`, `GB`, etc. | ISO country code |
| q | URL-encoded search term | Keyword search |
| search_type | `keyword_unordered`, `page` | Search mode |
| view_all_page_id | Facebook Page ID | Filter to specific page |

### Poll for Completion

```
GET https://api.apify.com/v2/acts/apify~facebook-ads-scraper/runs/{runId}?token={APIFY_API_TOKEN}
```

Response includes `status`: `READY`, `RUNNING`, `SUCCEEDED`, `FAILED`, `ABORTED`.

Poll every 5 seconds until `SUCCEEDED` or `FAILED`.

### Fetch Results

Use the dataset ID from the run info (more reliable than the run endpoint):

```
# Get dataset ID
GET https://api.apify.com/v2/acts/apify~facebook-ads-scraper/runs/{runId}?token={APIFY_API_TOKEN}
# → data.defaultDatasetId

# Fetch items
GET https://api.apify.com/v2/datasets/{datasetId}/items?token={APIFY_API_TOKEN}
```

### Output Fields

Each ad object contains (note: different from old actor schema):

| Field | Type | Description |
|-------|------|-------------|
| adArchiveID | string | Meta Ad Library ID (use for ad_library_url) |
| pageId / pageID | string | Facebook Page ID of the advertiser |
| pageName | string | Advertiser page name |
| isActive | boolean | Whether the ad is currently active |
| startDate | int | Unix timestamp when ad started running |
| endDate | int | Unix timestamp when ad stopped (0 if still active) |
| publisherPlatform | array | `["FACEBOOK"]`, `["INSTAGRAM"]`, etc. |
| categories | array | Ad categories |
| snapshot | object | Contains all creative content (see below) |

### Snapshot Object

The `snapshot` field contains the ad creative:

| Field | Type | Description |
|-------|------|-------------|
| snapshot.body | object | `{"text": "...", "markup": {"__html": "..."}}` — ad copy |
| snapshot.title | string | Ad headline |
| snapshot.ctaType | string | CTA type (LEARN_MORE, SIGN_UP, etc.) |
| snapshot.ctaText | string | CTA button text |
| snapshot.linkUrl | string | Landing page URL |
| snapshot.linkDescription | string | Link description text |
| snapshot.displayFormat | string | Format: `video`, `image`, `carousel`, etc. |
| snapshot.images | array | Array of image objects |
| snapshot.videos | array | Array of video objects |
| snapshot.cards | array | Carousel cards (each has own images/videos/copy) |

### Image Object

```json
{
  "originalImageUrl": "https://...",
  "resizedImageUrl": "https://...",
  "watermarkedResizedImageUrl": "https://...",
  "imageCrops": {}
}
```

### Video Object

```json
{
  "videoHdUrl": "https://...",
  "videoSdUrl": "https://...",
  "videoPreviewImageUrl": "https://...",
  "watermarkedVideoHdUrl": "https://...",
  "watermarkedVideoSdUrl": "https://..."
}
```

### Card Object (Carousel)

Each card has all the fields of both image and video objects plus its own copy:

```json
{
  "title": "Card headline",
  "body": "Card body text",
  "ctaType": "LEARN_MORE",
  "ctaText": "Learn More",
  "linkUrl": "https://...",
  "originalImageUrl": "https://...",
  "resizedImageUrl": "https://...",
  "videoHdUrl": "https://...",
  "videoSdUrl": "https://..."
}
```

## Cost Management

- ~$5 per 1,000 ads scraped (pay-per-event pricing)
- Use `maxItems` to control cost per run
- For watchlist re-scrapes, use lower maxItems (50-100 per page)
- For discovery searches, 100-200 is usually enough to identify competitors
- Avoid broad keyword searches with high maxItems — gets expensive fast

## Environment

```
APIFY_API_TOKEN=apify_api_xxxxxxxxxx
```

Get your token at: https://console.apify.com/account/integrations

## Safety

- Read-only scraping of publicly available data
- Assets downloaded locally for analysis, never redistributed
- Respect Apify's terms of service and rate limits
