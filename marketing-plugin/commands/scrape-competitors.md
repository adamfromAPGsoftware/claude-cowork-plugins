---
description: Scrape competitor Meta ads from the Ad Library via Apify
---

Run the competitor ad scraper against the full watchlist for the active campaign:

1. Read `{plugin_root}/data/campaigns/{active_campaign_id}/competitor-data.json` for the watchlist
2. Use Desktop Commander's `execute_command` (or Bash) to run:
   `python3 {plugin_root}/scripts/scrape-competitor-ads.py --campaign-id {active_campaign_id} --all --country AU`
3. Report: new ads found, existing ads updated, per-competitor breakdown

$ARGUMENTS
