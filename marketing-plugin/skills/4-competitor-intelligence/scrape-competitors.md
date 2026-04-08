---
name: scrape-competitors
description: Scrape competitor Meta ad libraries via Apify for all Page IDs on the watchlist
menu-code: SC
---

# Scrape Competitors

Scrape competitor Meta ad libraries via Apify for all Page IDs on the watchlist. Merge new/updated ads into competitor-data.json.

## Process

1. **Load competitor-data.json** — Read `{project-root}/marketing-plugin/data/competitor-data.json`

2. **Verify watchlist is not empty:**
   - If empty, tell the user to add competitors first with [MC] and stop
   - If populated, list competitors being scraped

3. **Run scrape script** using Bash (or Desktop Commander's `execute_command` in Cowork):
   ```
   python3 {project-root}/marketing-plugin/scripts/scrape-competitor-ads.py --all --country AU
   ```

   **Modes:**
   - `--all` — Scrape all watchlist pages (default usage)
   - `--pages 123,456` — Scrape specific page IDs
   - `--search "keyword"` — Discovery mode: find new competitors by keyword
   - `--max-items N` — Limit results (lower = cheaper, default 500)

   **Cost:** ~$5 per 1,000 ads. Use `--max-items` to control cost.

4. **Review script output:**
   - Note how many new ads were discovered per competitor
   - Note how many existing ads had their `last_seen` date updated
   - Note any errors (auth failure, rate limit, invalid Page ID)

5. **Load the updated competitor-data.json** and verify:
   - Total ads tracked
   - New ads this scrape
   - Updated ads (last_seen refreshed)
   - Per-competitor breakdown

6. **Update scrape metadata:**
   - Set `meta.last_scrape` to current timestamp
   - Set `meta.scrape_status` to `success` (or `partial` if errors occurred)
   - Update `meta.total_ads_tracked` count

## API Details

The Apify `apify/facebook-ads-scraper` actor takes `startUrls` — actual Meta Ad Library URLs:

**Page scrape (watchlist):**
```json
{
  "startUrls": [
    {"url": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&view_all_page_id={PAGE_ID}&search_type=page"}
  ],
  "maxItems": 500
}
```

**Keyword discovery:**
```json
{
  "startUrls": [
    {"url": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AU&q={KEYWORD}&search_type=keyword_unordered"}
  ],
  "maxItems": 200
}
```

Results are fetched via the dataset endpoint (not the run endpoint):
```
GET /v2/datasets/{datasetId}/items?token={TOKEN}
```

See `references/apify-facebook-ads-library.md` for full schema.

## Output

Report summary:

```
Scrape complete.
  Competitors scraped: {count}
  New ads found: {new_count}
  Existing ads updated: {updated_count}

  Per competitor:
  - {competitor_name} ({page_id}): {new} new, {updated} updated, {total} total
  - ...

  Total ads tracked: {total_ads}

Recommended next: [DA] to download new creative assets.
```
