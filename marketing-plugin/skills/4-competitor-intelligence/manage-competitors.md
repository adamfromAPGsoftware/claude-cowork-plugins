---
name: manage-competitors
description: Add or remove competitor Page IDs from the watchlist
menu-code: MC
---

# Manage Competitors

Add or remove competitor Facebook Page IDs from the watchlist in competitor-data.json.

## Process

1. **Load competitor-data.json** — Read `{project-root}/marketing-plugin/data/competitor-data.json`

2. **Show current watchlist:**
   ```
   Current watchlist ({count} competitors):
   - {name} — Page ID: {page_id} — Ads tracked: {ad_count}
   - ...
   (empty — no competitors on watchlist yet)
   ```

3. **Ask user what they want to do:**
   - **Add** — Ask for the Facebook Page ID and a display name for the competitor
   - **Remove** — Show numbered list, ask which to remove

4. **For adding:**
   - Validate the Page ID format (numeric string)
   - Check it's not already on the watchlist
   - Add to `watchlist` array in competitor-data.json:
     ```json
     {
       "page_id": "{page_id}",
       "name": "{name}",
       "added_date": "{today}",
       "total_ads": 0
     }
     ```
   - Save competitor-data.json

5. **For removing:**
   - Confirm with user before removing
   - Remove from `watchlist` array
   - Optionally: ask if they want to keep or delete associated ads and assets
   - Save competitor-data.json

## Output

Confirm the change:

```
Watchlist updated.
  {action}: {name} ({page_id})
  Total competitors: {count}

Run [SC] to scrape ads for the updated watchlist.
```
